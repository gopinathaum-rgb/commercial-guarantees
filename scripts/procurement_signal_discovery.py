#!/usr/bin/env python3
"""Discover formal ERP procurement notices from an allowlisted set of official pages.

A tender is evidence of a published procurement process, not proof that the
brokerage can lawfully or commercially intermediate it. No buyer is qualified
and no contact, bid, introduction or negotiation is initiated by this script.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

API = "https://api.github.com"
REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "gopinathaum-rgb/commercial-guarantees")
OWNER, REPO = REPOSITORY.split("/", 1)
TOKEN = os.environ["GITHUB_TOKEN"]
QUEUE_TITLE = "Formal procurement signals — ERP implementation and transformation"
SOURCE_PAGES = (
    {
        "organisation": "Foundation for Science Innovation & Development (IISc)",
        "url": "https://www.fsid-iisc.in/tenders/",
        "source_kind": "official_buyer_tender_page",
    },
    {
        "organisation": "Indian Institute of Management Kozhikode (IIMK)",
        "url": "https://www.iimk.ac.in/tender/",
        "source_kind": "official_buyer_tender_page",
    },
)
RELEVANT = re.compile(
    r"\b(ERP|SAP|enterprise resource planning|system integrator|"
    r"implementation partner|ERP implementation|ERP migration|"
    r"software implementation|business application implementation)\b",
    re.I,
)
PROCUREMENT = re.compile(r"\b(tenders?|RFP|NIT|bids?|procurement|EOI|request for proposal|invitation for bids|deadline for submission)\b", re.I)
MAX_PAGE_BYTES = 3_000_000


def request(url: str, method: str = "GET", payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "commercial-guarantees-procurement-discovery",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(url if url.startswith(API) else API + url,
                                 data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:1000]
        raise RuntimeError(f"GitHub API {exc.code}: {detail}") from exc


def fetch_page(url: str) -> str:
    host = urllib.parse.urlparse(url).hostname or ""
    if host not in {"www.fsid-iisc.in", "fsid-iisc.in", "www.iimk.ac.in", "iimk.ac.in"}:
        raise ValueError(f"Source host is not allowlisted: {host}")
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; CommercialProcurementResearch/1.0)",
        "Accept": "text/html,application/xhtml+xml",
    })
    with urllib.request.urlopen(req, timeout=30) as response:
        raw = response.read(MAX_PAGE_BYTES + 1)
    if len(raw) > MAX_PAGE_BYTES:
        raise ValueError(f"Source page exceeds {MAX_PAGE_BYTES} bytes: {url}")
    return raw.decode("utf-8", "replace")


class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.text_parts = []
        self._anchor = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a":
            self._anchor = [attrs.get("href", ""), []]

    def handle_data(self, data):
        self.text_parts.append(data)
        if self._anchor is not None:
            self._anchor[1].append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._anchor is not None:
            href, parts = self._anchor
            label = re.sub(r"\s+", " ", " ".join(parts)).strip()
            if href and label:
                self.links.append((href, label))
            self._anchor = None


def extract_procurement_signals(html: str, source: dict) -> list[dict]:
    parser = PageLinks()
    parser.feed(html)
    page_text = re.sub(r"\\s+", " ", " ".join(parser.text_parts)).strip()
    if not RELEVANT.search(page_text) or not PROCUREMENT.search(page_text[:20000]):
        return []

    found = {}
    source_host = urllib.parse.urlparse(source["url"]).hostname
    for href, label in parser.links:
        title = re.sub(r"\\s+", " ", label).strip()
        if not RELEVANT.search(title):
            continue
        url = urllib.parse.urljoin(source["url"], href)
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme != "https" or parsed.hostname != source_host:
            continue
        found[url] = title

    # Institutional tender pages often show the notice title in a heading and
    # label the linked PDF simply "Download". In that case retain the official
    # page itself as the source record rather than guessing which PDF link fits.
    if not found:
        match = RELEVANT.search(page_text)
        left = max(0, match.start() - 180)
        right = min(len(page_text), match.end() + 260)
        title = page_text[left:right].strip(" .|:-")
        found[source["url"]] = title

    rows = []
    for url, title in found.items():
        rows.append({
            "organisation": source["organisation"],
            "title": title,
            "notice_url": url,
            "source_page_url": source["url"],
            "source_kind": source["source_kind"],
            "signal_type": "formal_procurement_signal_unqualified",
            "buyer_status": "not_qualified",
            "deadline_status": "manual_check_required",
            "procurement_route_status": "blocked_pending_document_and_legal_review",
            "provider_side_route": "possible_only_after_provider_consent_and_written_terms",
            "captured_page_excerpt": page_text[:700],
        })
    return rows

def discover() -> tuple[list[dict], list[str]]:
    rows, errors = [], []
    for source in SOURCE_PAGES:
        try:
            html = fetch_page(source["url"])
            rows.extend(extract_procurement_signals(html, source))
        except Exception as exc:
            errors.append(f"{source['organisation']} ({source['url']}): {exc}")
    unique = {row["notice_url"]: row for row in rows}
    return sorted(unique.values(), key=lambda row: (row["organisation"], row["title"])), errors


def get_or_create_queue() -> int:
    for page in range(1, 6):
        issues = request(f"/repos/{OWNER}/{REPO}/issues?state=open&per_page=100&page={page}")
        for issue in issues:
            if not issue.get("pull_request") and issue.get("title") == QUEUE_TITLE:
                return issue["number"]
        if len(issues) < 100:
            break
    body = (
        "## Purpose\nCapture formal ERP implementation and transformation procurement notices "
        "from explicitly allowlisted official buyer pages.\n\n"
        "## Non-negotiable boundary\nA public tender is a procurement signal, not a qualified buyer "
        "for this brokerage. Verify current status, deadline, scope, buyer identity and procurement "
        "rules manually. Determine whether any paid intermediary/referral arrangement is permitted. "
        "Do not contact the buyer, bid, introduce a provider, or imply endorsement automatically. "
        "Where buyer-side brokerage is prohibited or unsuitable, investigate provider-side teaming "
        "only with provider consent and written, disclosed terms. No rate is presumed."
    )
    created = request(f"/repos/{OWNER}/{REPO}/issues", "POST",
                      {"title": QUEUE_TITLE, "body": body})
    return created["number"]


def main():
    candidates, errors = discover()
    queue_number = get_or_create_queue()
    comments = request(f"/repos/{OWNER}/{REPO}/issues/{queue_number}/comments?per_page=100")
    seen = set()
    for comment in comments:
        seen.update(re.findall(r"https://[^\s)]+", comment.get("body") or ""))
    fresh = [item for item in candidates if item["notice_url"] not in seen]
    print(f"official_sources={len(SOURCE_PAGES)} procurement_signals={len(candidates)} new={len(fresh)}")
    for error in errors:
        print(f"SOURCE_ERROR: {error}", file=sys.stderr)
    if not fresh:
        print("No new official procurement notices. No outreach or buyer qualification performed.")
        return
    lines = [
        "## Official procurement review batch",
        "",
        f"New notices captured: **{len(fresh)}**. These are formal procurement signals, not qualified brokerage buyers.",
        "",
    ]
    for item in fresh:
        lines.extend([
            f"### {item['organisation']} — {item['title']}",
            f"- Notice: {item['notice_url']}",
            f"- Official source page: {item['source_page_url']}",
            f"- Source type: {item['source_kind']}",
            "- Status: **formal procurement signal; current status and deadline require manual verification**",
            "- Buyer qualification: **not qualified**",
            "- Brokerage eligibility: **unknown; check tender/procurement rules before any intervention**",
            "- Provider-side route: **not approved; requires provider consent and written terms**",
            f"- Page excerpt: {item['captured_page_excerpt']}",
            "",
        ])
    lines.extend([
        "## Required intervention sequence",
        "1. Open the official notice and all corrigenda; verify whether it is current, open and within deadline.",
        "2. Extract scope, eligibility, geography, contract model, estimated value if disclosed, and acceptance/payment milestones.",
        "3. Check the notice and applicable procurement rules for restrictions on intermediaries, commissions, conflicts and bidder communications.",
        "4. If buyer-side brokerage is not permitted or commercially credible, do not approach the buyer as a broker. Assess provider-side teaming only with provider consent.",
        "5. Verify provider fit, references and capacity before proposing any introduction.",
        "6. Obtain owner approval for any deal-specific commission, introduction, disclosure or commitment.",
        "",
        "No outreach, bid submission, provider introduction, qualification or revenue is created by this run.",
    ])
    request(f"/repos/{OWNER}/{REPO}/issues/{queue_number}/comments", "POST",
            {"body": "\n".join(lines)})
    print(f"Appended {len(fresh)} official notices to {OWNER}/{REPO}#{queue_number}.")


if __name__ == "__main__":
    main()
