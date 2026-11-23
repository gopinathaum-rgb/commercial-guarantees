#!/usr/bin/env python3
"""Discover India provider candidates from Frappe's public partner directory.

Directory presence is evidence of listing only, not an independent quality
certification or evidence of availability, willingness to pay, or commission terms.
"""
from __future__ import annotations
import json, os, re, sys, urllib.error, urllib.parse, urllib.request
from html.parser import HTMLParser

DIRECTORY = "https://frappe.io/partners/list"
API = "https://api.github.com"
OWNER, REPO = os.environ.get("GITHUB_REPOSITORY", "gopinathaum-rgb/commercial-guarantees").split("/", 1)
TOKEN = os.environ["GITHUB_TOKEN"]
QUEUE_TITLE = "Provider discovery — ERPNext/Frappe India supply queue"

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current = None
        self.items = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href", "")
            self.current = [href, []]
    def handle_data(self, data):
        if self.current is not None:
            self.current[1].append(data)
    def handle_endtag(self, tag):
        if tag == "a" and self.current is not None:
            href, parts = self.current
            name = re.sub(r"\s+", " ", " ".join(parts)).strip()
            if re.search(r"^/partners/india/[^?#]+$", href, re.I) and name:
                self.items.append((name, urllib.parse.urljoin("https://frappe.io", href)))
            self.current = None

def get(url, api=False):
    headers = {"User-Agent": "commercial-guarantees-provider-discovery/1.0"}
    if api:
        headers.update({"Accept":"application/vnd.github+json","Authorization":f"Bearer {TOKEN}",
                        "X-GitHub-Api-Version":"2022-11-28"})
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8", "replace")

def api(path, method="GET", payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(API + path, data=data, method=method, headers={
        "Accept":"application/vnd.github+json","Authorization":f"Bearer {TOKEN}",
        "X-GitHub-Api-Version":"2022-11-28","User-Agent":"commercial-guarantees-provider-discovery",
        "Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            raw=response.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"GitHub API {exc.code}: {exc.read().decode('utf-8','replace')[:800]}") from exc

def discover():
    parser=Links()
    parser.feed(get(DIRECTORY))
    unique={url:name for name,url in parser.items}
    return [{"name":name,"profile_url":url,"source_url":DIRECTORY,
             "source_type":"official_frappe_partner_directory",
             "directory_status":"listed_on_source_at_run_time",
             "provider_quality":"not_independently_verified",
             "availability":"unknown","commission_willingness":"unknown",
             "contact_permission":"not_obtained"}
            for url,name in sorted(unique.items(), key=lambda x:x[1].casefold())]

def queue_issue():
    page=1
    while page<=5:
        rows=api(f"/repos/{OWNER}/{REPO}/issues?state=open&per_page=100&page={page}")
        for row in rows:
            if not row.get("pull_request") and row.get("title")==QUEUE_TITLE:
                return row["number"]
        if len(rows)<100: break
        page+=1
    created=api(f"/repos/{OWNER}/{REPO}/issues","POST",{"title":QUEUE_TITLE,"body":
        "Private-operating queue for publicly listed ERPNext/Frappe provider candidates.\\n\\n"
        "Directory listing is not independent quality verification. Do not infer availability, "
        "capacity, willingness to pay, commission acceptance or buyer suitability. "
        "Do not publish private contact details or initiate outreach from this queue."})
    return created["number"]

def main():
    candidates=discover()
    number=queue_issue()
    comments=[]
    for page in range(1,21):
        batch=api(f"/repos/{OWNER}/{REPO}/issues/{number}/comments?per_page=100&page={page}")
        comments.extend(batch)
        if len(batch)<100: break
    seen=set()
    issue=api(f"/repos/{OWNER}/{REPO}/issues/{number}")
    seen.update(re.findall(r"https://frappe\\.io/partners/india/[^\\s)]+",issue.get("body") or ""))
    for c in comments:
        seen.update(re.findall(r"https://frappe\\.io/partners/india/[^\\s)]+",c.get("body") or ""))
    fresh=[x for x in candidates if x["profile_url"] not in seen]
    print(f"directory_candidates={len(candidates)} new_candidates={len(fresh)}; no contact or quality inference.")
    if not fresh: return
    lines=["## Provider discovery batch","",f"New India directory profiles: **{len(fresh)}**","",
           "Every record is a candidate only. Independently verify capability, references, team, current availability, buyer fit and consent before matching or introducing.",""]
    for x in fresh:
        lines += [f"### {x['name']}",f"- Official profile: {x['profile_url']}",
                  f"- Directory: {x['source_url']}",
                  "- Listing evidence: listed on official directory at run time",
                  "- Quality / availability / willingness to pay: **unverified / unknown**",""]
    api(f"/repos/{OWNER}/{REPO}/issues/{number}/comments","POST",{"body":"\\n".join(lines)})
    print(f"Appended {len(fresh)} candidates to internal queue #{number}.")

if __name__=="__main__":
    try: main()
    except Exception as exc:
        print(f"ERROR: {exc}",file=sys.stderr)
        raise
