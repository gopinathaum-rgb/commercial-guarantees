#!/usr/bin/env python3
"""Collect public ERP implementation threads as ecosystem/problem research only.

These discussions are not commercial demand or buyer leads. This collector is
secondary to official procurement discovery and never contacts issue authors.
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
REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "gopinathaum-rgb/commercial-guarantees")
OWNER, REPO = REPOSITORY.split("/", 1)
TOKEN = os.environ["GITHUB_TOKEN"]
QUEUE_TITLE = "GitHub channel — customer discovery queue"
TARGET_REPOS = ("frappe/erpnext", "frappe/frappe", "odoo/odoo")
SEARCH_TERMS = ("implementation", "migration", "deployment", "acceptance")
LIFECYCLE_TERMS = (
    "implementation", "migration", "go live", "go-live", "cutover",
    "acceptance", "uat", "rollout", "deployment", "handover",
    "data migration", "production launch",
)
CONTEXT_TERMS = (
    "customer", "client", "project", "integration", "data import",
    "delayed", "delay", "blocked", "failed", "handover", "training",
    "vendor", "consultant", "partner",
)
DECISION_TERMS = (
    "sign-off", "signoff", "acceptance test", "user acceptance",
    "milestone payment", "payment withheld", "invoice", "holdback",
    "go-live approval", "production approval", "handover accepted",
    "customer approval", "rejected delivery", "delivery acceptance",
    "contract", "statement of work", "scope dispute",
)

def request(path: str, method: str = "GET", payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(API + path, data=data, method=method, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "commercial-guarantees-github-discovery",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            raw = response.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:1200]
        raise RuntimeError(f"GitHub API {exc.code} for {path}: {detail}") from exc

def paginated(path: str, max_pages: int = 10):
    rows = []
    for page in range(1, max_pages + 1):
        separator = "&" if "?" in path else "?"
        batch = request(f"{path}{separator}per_page=100&page={page}")
        if not isinstance(batch, list):
            raise RuntimeError(f"Expected list response while paging {path}")
        rows.extend(batch)
        if len(batch) < 100:
            break
    return rows

def redact(text: str, limit: int = 650) -> str:
    text = re.sub(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", "[email redacted]", text, flags=re.I)
    text = re.sub(r"(?i)(token|password|secret|api[_ -]?key)\s*[:=]\s*[^\s,;]+", r"\1=[redacted]", text)
    text = re.sub(r"https?://[^\s)]+", lambda m: m.group(0)[:180], text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]

def analyse_text(title: str, body: str, comments: list[dict] | None = None):
    comments = comments or []
    comment_text = " ".join((c.get("body") or "") for c in comments)
    corpus = f"{title} {body} {comment_text}".lower()
    lifecycle = [term for term in LIFECYCLE_TERMS if term in corpus]
    context = [term for term in CONTEXT_TERMS if term in corpus]
    decision = [term for term in DECISION_TERMS if term in corpus]
    if decision and lifecycle:
        classification = "decision_evidence_review"
    elif lifecycle and context:
        classification = "implementation_lifecycle_context"
    elif lifecycle:
        classification = "lifecycle_signal_only"
    else:
        classification = "insufficient_lifecycle_evidence"
    return {
        "classification": classification,
        "lifecycle_signals": lifecycle[:8],
        "context_signals": context[:8],
        "decision_signals": decision[:8],
        "comment_count_read": len(comments),
        "discussion_excerpt": redact(comment_text, 500) if comment_text else "[no comments]",
    }

def search_candidates():
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=45)).date().isoformat()
    found = {}
    for target in TARGET_REPOS:
        for term in SEARCH_TERMS:
            query = f'repo:{target} is:issue is:open updated:>={since} "{term}"'
            params = urllib.parse.urlencode({"q": query, "sort": "updated", "order": "desc", "per_page": 100})
            for page in range(1, 11):
                page_params = params + "&page=" + str(page)
                batch = request("/search/issues?" + page_params).get("items", [])
                for item in batch:
                    if item.get("pull_request"):
                        continue
                    author = (item.get("user") or {}).get("login", "")
                    if author.endswith("[bot]") or author in {"github-actions", "dependabot"}:
                        continue
                    url = item.get("html_url")
                    if url:
                        found[url] = item
                if len(batch) < 100:
                    break
    candidates = []
    for url, item in found.items():
        title, body = item.get("title") or "", item.get("body") or ""
        repo_path = item.get("repository_url", "").split("/repos/")[-1]
        comments = paginated(
            f"/repos/{repo_path}/issues/{item['number']}/comments", max_pages=5
        ) if item.get("comments", 0) else []
        analysis = analyse_text(title, body, comments)
        if not analysis["lifecycle_signals"]:
            continue
        score = (4 * len(analysis["decision_signals"])
                 + 2 * len(analysis["lifecycle_signals"])
                 + len(analysis["context_signals"])
                 + min(len(comments), 5))
        candidates.append({
            "url": url, "repo": repo_path, "number": item.get("number"),
            "title": title, "updated": item.get("updated_at", ""),
            "author": (item.get("user") or {}).get("login", "[unknown]"),
            "score": score, "analysis": analysis, "excerpt": redact(body or title),
        })
    return sorted(candidates, key=lambda x: (x["score"], x["updated"]), reverse=True)[:15]

def get_or_create_queue():
    issues = paginated(f"/repos/{OWNER}/{REPO}/issues?state=open", max_pages=5)
    for issue in issues:
        if not issue.get("pull_request") and issue.get("title") == QUEUE_TITLE:
            return issue["number"]
    body = (
        "## Purpose\nA low-priority research queue for public ERP implementation discussions. This is not a buyer or demand queue.\n\n"
        "## Evidence boundary — research only\n"
        "- A technical problem is not proof of buying intent, budget, authority, or a customer.\n"
        "- Decision-language matches are prioritization signals only; read the source thread before interpreting them.\n"
        "- The automation does not contact authors, infer private intent, post promotional comments, or request confidential records.\n"
        "- Only a separately evidenced decision owner, current consequential situation, permission, scope, and willingness to pay can qualify an opportunity."
    )
    created = request(f"/repos/{OWNER}/{REPO}/issues", "POST", {"title": QUEUE_TITLE, "body": body})
    return created["number"]

def main():
    candidates = search_candidates()
    queue_number = get_or_create_queue()
    prior_comments = paginated(
        f"/repos/{OWNER}/{REPO}/issues/{queue_number}/comments", max_pages=20
    )
    seen = set()
    for comment in prior_comments:
        seen.update(re.findall(r"https://github\.com/[^\s)]+/issues/\d+", comment.get("body") or ""))
    fresh = [item for item in candidates if item["url"] not in seen]
    print(f"Repositories={len(TARGET_REPOS)} unique_threads={len(candidates)} new_threads={len(fresh)}; no buying-intent inference is performed.")
    if not fresh:
        print("No new source threads. No queue comment created.")
        return
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    lines = [f"## Candidate review batch — {today}", "",
             f"New source threads: **{len(fresh)}**. Rank is a reading priority, not a lead score.", ""]
    for item in fresh:
        a = item["analysis"]
        lines.extend([
            f"### [{item['repo']}#{item['number']}] {item['title']}",
            f"- Source: {item['url']}",
            f"- Author: {item['author']} · Updated: {item['updated']}",
            f"- Review priority: {item['score']} · Classification: **{a['classification']}**",
            f"- Lifecycle signals: {', '.join(a['lifecycle_signals']) or 'none'}",
            f"- Decision-language signals: {', '.join(a['decision_signals']) or 'none detected'}",
            f"- Discussion comments read: {a['comment_count_read']}",
            f"- Issue excerpt: {item['excerpt'] or '[no description]'}",
            f"- Discussion excerpt: {a['discussion_excerpt']}",
            "- Commercial demand status: **not evidenced — do not count as a buyer, prospect or lead**", "",
        ])
    lines.extend([
        "## Required reviewer actions",
        "1. Open each source and verify the complete thread and current status.",
        "2. Record facts, reported claims, inferences, and unknowns separately.",
        "3. Identify whether a named commercial milestone/acceptance/payment decision is actually evidenced.",
        "4. If useful, prepare a technically accurate public contribution; do not post automatically.",
        "5. Record any unsolicited service inquiry separately and qualify authority, timing, permission, scope, and willingness to pay.",
    ])
    request(f"/repos/{OWNER}/{REPO}/issues/{queue_number}/comments", "POST", {"body": "\n".join(lines)})
    print(f"Appended {len(fresh)} candidates to {OWNER}/{REPO}#{queue_number}.")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
