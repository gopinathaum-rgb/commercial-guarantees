#!/usr/bin/env python3
"""Find public ERP implementation lifecycle signals and append them to one review queue.

This job does not infer buying intent, contact issue authors, or comment on third-party
repositories. It only collects public issue links and short, redacted excerpts for review.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.github.com"
OWNER = os.environ.get("GITHUB_REPOSITORY", "gopinathaum-rgb/commercial-guarantees").split("/")[0]
REPO = os.environ.get("GITHUB_REPOSITORY", "gopinathaum-rgb/commercial-guarantees").split("/")[1]
TOKEN = os.environ["GITHUB_TOKEN"]
QUEUE_TITLE = "GitHub channel — customer discovery queue"
TARGET_REPOS = ("frappe/erpnext", "frappe/frappe", "odoo/odoo")
SIGNAL_TERMS = (
    "implementation", "migration", "go live", "go-live", "cutover",
    "acceptance", "uat", "rollout", "deployment", "production",
    "customer", "client", "project", "integration", "data import",
    "delayed", "delay", "blocked", "failed", "handover", "training",
)
LIFECYCLE_TERMS = (
    "implementation", "migration", "go live", "go-live", "cutover",
    "acceptance", "uat", "rollout", "deployment", "handover",
)


def request(path: str, method: str = "GET", payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API + path,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "commercial-guarantees-github-discovery",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            raw = response.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:1200]
        raise RuntimeError(f"GitHub API {exc.code} for {path}: {detail}") from exc


def redact(text: str) -> str:
    text = re.sub(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", "[email redacted]", text, flags=re.I)
    text = re.sub(r"https?://[^\s)]+", lambda m: m.group(0)[:180], text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:850]


def search_candidates():
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=45)).date().isoformat()
    found = {}
    for target in TARGET_REPOS:
        query = (
            f'repo:{target} is:issue is:open updated:>={since} '
            '(implementation OR migration OR "go live" OR "go-live" OR UAT '
            'OR acceptance OR rollout OR deployment OR cutover)'
        )
        params = urllib.parse.urlencode({"q": query, "sort": "updated", "order": "desc", "per_page": 50})
        result = request("/search/issues?" + params)
        for item in result.get("items", []):
            if item.get("pull_request"):
                continue
            author = (item.get("user") or {}).get("login", "")
            if author.endswith("[bot]") or author in {"github-actions", "dependabot"}:
                continue
            title = item.get("title") or ""
            body = item.get("body") or ""
            corpus = (title + " " + body).lower()
            score = sum(1 for term in SIGNAL_TERMS if term in corpus)
            lifecycle = [term for term in LIFECYCLE_TERMS if term in corpus]
            if score < 3 or not lifecycle:
                continue
            url = item.get("html_url")
            if not url:
                continue
            found[url] = {
                "url": url,
                "repo": target,
                "title": title,
                "updated": item.get("updated_at", ""),
                "comments": item.get("comments", 0),
                "score": score,
                "signals": lifecycle[:5],
                "excerpt": redact(body or title),
            }
    return sorted(found.values(), key=lambda x: (x["score"], x["updated"]), reverse=True)[:12]


def get_or_create_queue():
    issues = request(f"/repos/{OWNER}/{REPO}/issues?state=open&per_page=100")
    for issue in issues:
        if not issue.get("pull_request") and issue.get("title") == QUEUE_TITLE:
            return issue["number"]
    body = (
        "## Purpose\n"
        "A durable review queue for public GitHub issue threads that describe ERP implementation, "
        "migration, deployment, acceptance, cutover, or handover problems.\n\n"
        "## Evidence boundary\n"
        "- A public technical or operational problem is **not** evidence of buying intent, budget, or authority.\n"
        "- This queue is for human review of whether we can contribute a genuinely useful, technically accurate answer.\n"
        "- The automation does not contact authors, infer private intent, post promotional comments, or request confidential records.\n"
        "- Any public contribution must stand on its own and must not be a disguised sales pitch.\n"
        "- A prospect becomes qualified only after a real decision owner, current consequential situation, permission, scope, and willingness to pay are established separately.\n\n"
        "New source threads are appended as comments only when first discovered."
    )
    created = request(f"/repos/{OWNER}/{REPO}/issues", "POST", {"title": QUEUE_TITLE, "body": body})
    return created["number"]


def main():
    candidates = search_candidates()
    queue_number = get_or_create_queue()
    comments = request(f"/repos/{OWNER}/{REPO}/issues/{queue_number}/comments?per_page=100")
    already_seen = set()
    for comment in comments:
        already_seen.update(re.findall(r"https://github\.com/[^\s)]+/issues/\d+", comment.get("body") or ""))
    fresh = [item for item in candidates if item["url"] not in already_seen]

    print(f"Scanned {len(TARGET_REPOS)} public ERP repositories; {len(candidates)} candidates passed the text filter; {len(fresh)} are new.")
    if not fresh:
        print("No new candidate links. No GitHub comment created.")
        return

    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    lines = [
        f"## New public ERP implementation signals — {today}",
        "",
        f"New links: **{len(fresh)}**. These are problem-context signals only, not buyer leads or buying intent.",
        "",
    ]
    for item in fresh:
        lines.extend([
            f"### [{item['repo']}] {item['title']}",
            f"- Source: {item['url']}",
            f"- Last updated: {item['updated'] or 'unknown'} · Existing comments: {item['comments']}",
            f"- Text signals: {', '.join(item['signals'])}",
            f"- Public excerpt: {item['excerpt'] or '[no description]'}",
            "",
        ])
    lines.extend([
        "## Review protocol",
        "1. Open the source and read the full issue plus discussion before forming a view.",
        "2. Decide whether it describes a real implementation lifecycle problem rather than an isolated product bug.",
        "3. If useful, prepare a technically substantive answer that helps the author even if they never become a customer.",
        "4. Do not add a promotional link or offer unless the author explicitly invites relevant services or asks for help.",
        "5. Record any actual inbound interest separately; do not count views, comments, stars, or issue authors as qualified buyers.",
    ])
    request(
        f"/repos/{OWNER}/{REPO}/issues/{queue_number}/comments",
        "POST",
        {"body": "\n".join(lines)},
    )
    print(f"Appended {len(fresh)} new source links to {OWNER}/{REPO}#{queue_number}.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
