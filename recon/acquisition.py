from __future__ import annotations

"""Public-web source acquisition for Recon.

This module deliberately uses the Python standard library. It does not bypass
authentication, CAPTCHAs, robots restrictions, or other access controls.
"""

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
import hashlib
import json
import mimetypes
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, build_opener
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.robotparser import RobotFileParser
from urllib.request import Request


DOCUMENT_SUFFIXES = {
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".csv", ".odt", ".ods",
    ".ppt", ".pptx", ".zip", ".rtf", ".txt",
}
DEFAULT_USER_AGENT = "ReconSourceAcquisition/0.1 (+public-source research; contact: operator)"


@dataclass(frozen=True)
class AcquiredDocument:
    source_url: str
    final_url: str
    retrieved_at: str
    status: str
    http_status: int | None
    content_type: str | None
    filename: str | None
    sha256: str | None
    size_bytes: int
    path: str | None
    error: str | None = None


@dataclass(frozen=True)
class AcquisitionResult:
    seed_url: str
    started_at: str
    completed_at: str
    pages_visited: int
    documents: tuple[AcquiredDocument, ...]
    errors: tuple[str, ...]
    page_snapshots: tuple[dict, ...] = ()

    def to_dict(self) -> dict:
        return {
            "seed_url": self.seed_url,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "pages_visited": self.pages_visited,
            "page_snapshots": list(self.page_snapshots),
            "documents": [asdict(item) for item in self.documents],
            "errors": list(self.errors),
        }


class _Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        target = values.get("href") or values.get("src") or values.get("data-url") or values.get("data-href") or values.get("data-file")
        if target and tag in {"a", "iframe", "embed", "object", "link"}:
            self.links.append((target.strip(), values.get("download", "")))
        # Some public tender portals place attachment URLs in inline onclick handlers.
        onclick = values.get("onclick", "")
        for match in re.findall(r"[\"']((?:https?://|/)[^\"']+)[\"']", onclick):
            self.links.append((match.strip(), values.get("download", "")))


def _is_document(url: str, download_attr: str = "") -> bool:
    path = urlparse(url).path.lower()
    return bool(download_attr) or Path(path).suffix in DOCUMENT_SUFFIXES


def _safe_name(url: str, content_type: str | None) -> str:
    name = Path(urlparse(url).path).name or "download"
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name)[:150]
    if not Path(name).suffix and content_type:
        ext = mimetypes.guess_extension(content_type.split(";", 1)[0].strip()) or ""
        name += ext
    return name or "download.bin"


class _AllowedHostRedirectHandler(HTTPRedirectHandler):
    """Reject redirects outside the same host/explicit allowlist boundary."""

    def __init__(self, allowed) -> None:
        super().__init__()
        self.allowed = allowed

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target = urljoin(req.full_url, newurl)
        if not self.allowed(target):
            raise HTTPError(req.full_url, code, "redirect target host is not allowed", headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, target)


class SourceAcquirer:
    def __init__(
        self,
        output_dir: Path,
        *,
        max_pages: int = 30,
        max_documents: int = 100,
        max_bytes: int = 50 * 1024 * 1024,
        timeout: int = 25,
        retries: int = 2,
        delay_seconds: float = 0.25,
        user_agent: str = DEFAULT_USER_AGENT,
        allowed_hosts: set[str] | None = None,
    ) -> None:
        self.output_dir = Path(output_dir)
        self.max_pages = max_pages
        self.max_documents = max_documents
        self.max_bytes = max_bytes
        self.timeout = timeout
        self.retries = retries
        self.delay_seconds = delay_seconds
        self.user_agent = user_agent
        self.allowed_hosts = {h.lower() for h in allowed_hosts} if allowed_hosts else None
        self._robots_cache: dict[str, RobotFileParser | bool] = {}

    def _allowed(self, url: str, seed_host: str) -> bool:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return False
        host = (parsed.hostname or "").lower()
        if self.allowed_hosts is not None:
            return host == seed_host or host in self.allowed_hosts
        return host == seed_host

    def _robots_allowed(self, url: str, seed_host: str) -> bool:
        """Fail closed when robots policy cannot be established; cache per origin."""
        parsed = urlparse(url)
        origin = f"{parsed.scheme}://{parsed.netloc}"
        if origin not in self._robots_cache:
            robots_url = f"{origin}/robots.txt"
            try:
                _status, _headers, _final_url, body = self._get(robots_url, seed_host)
                parser = RobotFileParser()
                parser.set_url(robots_url)
                parser.parse(body.decode("utf-8", errors="replace").splitlines())
                self._robots_cache[origin] = parser
            except HTTPError as exc:
                if exc.code in {404, 410}:
                    self._robots_cache[origin] = True
                else:
                    self._robots_cache[origin] = False
            except Exception:
                self._robots_cache[origin] = False
        policy = self._robots_cache[origin]
        if policy is True:
            return True
        if policy is False:
            return False
        return bool(policy.can_fetch(self.user_agent, url))

    def _get(self, url: str, seed_host: str | None = None):
        request = Request(url, headers={"User-Agent": self.user_agent, "Accept": "*/*"})
        boundary_host = seed_host or (urlparse(url).hostname or "").lower()
        opener = build_opener(_AllowedHostRedirectHandler(
            lambda target: self._allowed(target, boundary_host)
        ))
        last_error = None
        for attempt in range(self.retries + 1):
            try:
                with opener.open(request, timeout=self.timeout) as response:
                    body = response.read(self.max_bytes + 1)
                    if len(body) > self.max_bytes:
                        raise ValueError(f"response exceeds max_bytes ({self.max_bytes})")
                    return response.status, response.headers, response.geturl(), body
            except HTTPError as exc:
                last_error = f"HTTP {exc.code}: {exc.reason}"
                if exc.code not in {408, 425, 429, 500, 502, 503, 504}:
                    raise
            except (URLError, TimeoutError, OSError) as exc:
                last_error = f"{type(exc).__name__}: {exc}"
            if attempt < self.retries:
                time.sleep(min(2 ** attempt, 4))
        raise RuntimeError(last_error or "request failed")

    def acquire(self, seed_url: str) -> AcquisitionResult:
        started = datetime.now(timezone.utc).isoformat()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        seed_host = (urlparse(seed_url).hostname or "").lower()
        if not seed_host or urlparse(seed_url).scheme not in {"http", "https"}:
            raise ValueError("seed_url must be an absolute HTTP(S) URL")

        queue = [seed_url]
        seen_pages: set[str] = set()
        seen_docs: set[str] = set()
        documents: list[AcquiredDocument] = []
        errors: list[str] = []
        page_snapshots: list[dict] = []

        while queue and len(seen_pages) < self.max_pages and len(documents) < self.max_documents:
            page_url = urldefrag(queue.pop(0))[0]
            if page_url in seen_pages or not self._allowed(page_url, seed_host):
                continue
            if not self._robots_allowed(page_url, seed_host):
                errors.append(f"robots.txt disallows or could not authorize page: {page_url}")
                continue
            seen_pages.add(page_url)
            try:
                status, headers, final_url, body = self._get(page_url, seed_host)
                content_type = headers.get("Content-Type", "").lower()
                if "html" not in content_type and not body.lstrip().startswith((b"<!doctype html", b"<html")):
                    if _is_document(page_url):
                        self._save_document(page_url, final_url, status, content_type, body, documents)
                    continue
                html_text = body.decode(headers.get_content_charset() or "utf-8", errors="replace")
                page_digest = hashlib.sha256(body).hexdigest()
                page_name = f"{page_digest[:12]}-page-snapshot.html"
                (self.output_dir / page_name).write_bytes(body)
                page_snapshots.append({
                    "source_url": page_url,
                    "final_url": final_url,
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "http_status": status,
                    "content_type": content_type or None,
                    "sha256": page_digest,
                    "size_bytes": len(body),
                    "path": page_name,
                })
                parser = _Links()
                parser.feed(html_text)
                for raw_link, download_attr in parser.links:
                    candidate = urldefrag(urljoin(final_url, raw_link))[0]
                    if not self._allowed(candidate, seed_host):
                        continue
                    if not self._robots_allowed(candidate, seed_host):
                        errors.append(f"robots.txt disallows or could not authorize URL: {candidate}")
                        continue
                    if _is_document(candidate, download_attr):
                        if candidate not in seen_docs and len(documents) < self.max_documents:
                            seen_docs.add(candidate)
                            try:
                                d_status, d_headers, d_final, d_body = self._get(candidate, seed_host)
                                self._save_document(candidate, d_final, d_status, d_headers.get("Content-Type", "").lower(), d_body, documents)
                            except Exception as exc:
                                documents.append(AcquiredDocument(candidate, candidate, datetime.now(timezone.utc).isoformat(), "failed", None, None, None, None, 0, None, str(exc)))
                    elif candidate not in seen_pages and len(queue) + len(seen_pages) < self.max_pages:
                        suffix = Path(urlparse(candidate).path).suffix.lower()
                        if suffix in {"", ".html", ".htm", ".php", ".aspx"}:
                            queue.append(candidate)
            except Exception as exc:
                errors.append(f"{page_url}: {type(exc).__name__}: {exc}")
            if self.delay_seconds:
                time.sleep(self.delay_seconds)

        result = AcquisitionResult(
            seed_url, started, datetime.now(timezone.utc).isoformat(),
            len(seen_pages), tuple(documents), tuple(errors), tuple(page_snapshots),
        )
        (self.output_dir / "acquisition-manifest.json").write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")
        return result

    def _save_document(self, source_url, final_url, status, content_type, body, documents) -> None:
        digest = hashlib.sha256(body).hexdigest()
        name = _safe_name(final_url, content_type)
        # A digest prefix prevents same-name attachments from overwriting one another.
        filename = f"{digest[:12]}-{name}"
        destination = self.output_dir / filename
        destination.write_bytes(body)
        documents.append(AcquiredDocument(
            source_url=source_url,
            final_url=final_url,
            retrieved_at=datetime.now(timezone.utc).isoformat(),
            status="retrieved",
            http_status=status,
            content_type=content_type or None,
            filename=filename,
            sha256=digest,
            size_bytes=len(body),
            path=filename,
        ))


def main() -> int:
    parser = argparse.ArgumentParser(description="Acquire publicly accessible documents linked from a source page.")
    parser.add_argument("--url", required=True, help="Public HTTP(S) page to inspect")
    parser.add_argument("--out", type=Path, required=True, help="Directory for downloaded files and manifest")
    parser.add_argument("--max-pages", type=int, default=30)
    parser.add_argument("--max-documents", type=int, default=100)
    parser.add_argument("--max-bytes", type=int, default=50 * 1024 * 1024)
    parser.add_argument("--allow-host", action="append", default=None, help="Additional exact hostname allowed; repeat as needed")
    args = parser.parse_args()
    result = SourceAcquirer(
        args.out,
        max_pages=args.max_pages,
        max_documents=args.max_documents,
        max_bytes=args.max_bytes,
        allowed_hosts=set(args.allow_host) if args.allow_host else None,
    ).acquire(args.url)
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if any(d.status == "retrieved" for d in result.documents) else 2


if __name__ == "__main__":
    raise SystemExit(main())
