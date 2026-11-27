from __future__ import annotations

"""Run the ICMAI ERP tender source-acquisition and extraction acceptance workflow.

This command reads only the official listing URL in the checked-in profile.
It does not fetch third-party mirrors or authenticate to GeM.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import mimetypes
from pathlib import Path
import shutil
from urllib.parse import urlparse

from recon.acquisition import SourceAcquirer
from recon.extraction import extract_acquisition_manifest



def _write_operator_supplied_manifest(profile: dict, source_dir: Path, acquisition_dir: Path) -> Path:
    """Import operator-downloaded files while keeping their provenance distinct."""
    source_dir = Path(source_dir)
    acquisition_dir = Path(acquisition_dir)
    acquisition_dir.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()
    documents = []
    for expected in profile.get("expected_documents", []):
        name = Path(expected["filename"]).name
        source = source_dir / name
        if not source.is_file():
            documents.append({
                "source_url": expected.get("source_url"),
                "final_url": None,
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "status": "missing",
                "http_status": None,
                "content_type": None,
                "filename": name,
                "sha256": None,
                "size_bytes": 0,
                "path": None,
                "error": "expected file not present in operator source directory",
                "acquisition_method": "operator_supplied_local_copy",
                "publisher_verification": "not_available",
            })
            continue
        raw = source.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        stored_name = f"{digest[:12]}-{name}"
        destination = acquisition_dir / stored_name
        shutil.copy2(source, destination)
        content_type = mimetypes.guess_type(name)[0]
        documents.append({
            "source_url": expected.get("source_url"),
            "final_url": None,
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "status": "operator_supplied",
            "http_status": None,
            "content_type": content_type,
            "filename": stored_name,
            "sha256": digest,
            "size_bytes": len(raw),
            "path": stored_name,
            "error": None,
            "acquisition_method": "operator_supplied_local_copy",
            "publisher_verification": "pending_operator_confirmation",
        })
    manifest = {
        "seed_url": profile["official_listing_url"],
        "started_at": started,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "pages_visited": 0,
        "page_snapshots": [],
        "documents": documents,
        "errors": [],
        "acquisition_mode": "operator_supplied_local_import",
    }
    manifest_path = acquisition_dir / "acquisition-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest_path

def run_acceptance(profile_path: Path, output_dir: Path, allowed_hosts: set[str] | None = None, local_source_dir: Path | None = None) -> dict:
    profile_path = Path(profile_path)
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    seed_url = profile["official_listing_url"]
    seed_host = urlparse(seed_url).hostname
    if not seed_host:
        raise ValueError("official_listing_url must contain a hostname")
    output_dir = Path(output_dir)
    acquisition_dir = output_dir / "acquired"
    extraction_dir = output_dir / "extracted"

    if local_source_dir:
        acquisition_manifest = _write_operator_supplied_manifest(profile, local_source_dir, acquisition_dir)
    else:
        approved_hosts = set(profile.get("official_document_hosts", []))
        approved_hosts.update(allowed_hosts or set())
        SourceAcquirer(
            acquisition_dir,
            max_pages=1,
            max_documents=100,
            max_bytes=50 * 1024 * 1024,
            delay_seconds=0.5,
            allowed_hosts=approved_hosts or None,
        ).acquire(seed_url)
        acquisition_manifest = acquisition_dir / "acquisition-manifest.json"
    acquisition_payload = json.loads(acquisition_manifest.read_text(encoding="utf-8"))
    extraction = extract_acquisition_manifest(
        acquisition_manifest,
        profile_path=profile_path,
        output_dir=extraction_dir,
    )

    expected = extraction["expected_documents"]
    summary = {
        "profile_id": profile.get("profile_id"),
        "bid_number": profile.get("bid_number"),
        "started_at": acquisition_payload.get("started_at"),
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "source_mode": acquisition_payload.get("acquisition_mode", "official_public_source_retrieval"),
        "official_seed_url": seed_url,
        "official_seed_host": seed_host,
        "robots_policy_enforced": local_source_dir is None,
        "third_party_sources_fetched": False,
        "acquisition_manifest": str(acquisition_manifest),
        "extraction_manifest": str(extraction_dir / "extraction-manifest.json"),
        "acquisition_document_count": len(acquisition_payload.get("documents", [])),
        "retrieved_document_count": sum(item.get("status") == "retrieved" for item in acquisition_payload.get("documents", [])),
        "operator_supplied_document_count": sum(item.get("status") == "operator_supplied" for item in acquisition_payload.get("documents", [])),
        "retrieval_failure_count": sum(item.get("status") == "failed" for item in acquisition_payload.get("documents", [])),
        "expected_document_count": len(expected),
        "expected_missing_count": sum(item["acquisition_state"] == "missing" for item in expected),
        "expected_retrieval_failed_count": sum(item["acquisition_state"] == "retrieval_failed" for item in expected),
        "extracted_document_count": extraction["summary"]["extracted_count"],
        "extraction_failure_count": extraction["summary"]["extraction_failed_count"],
        "expected_document_states": expected,
        "acquisition_errors": acquisition_payload.get("errors", []),
        "acceptance_passed": (
            len(expected) > 0
            and all(item["acquisition_state"] == "extracted" for item in expected)
            and extraction["summary"]["extraction_failed_count"] == 0
            and not acquisition_payload.get("errors")
        ),
        "acceptance_note": (
            "Operator-supplied local files are extracted for analysis but remain explicitly distinct from public-source retrieval; "
            "publisher verification is pending and these files do not satisfy the strict official-source acceptance pass."
            if local_source_dir else
            "A pass requires every expected item to be acquired from its stated publisher and extracted. "
            "The profile includes GeM attachments not linked from the ICMAI listing; these remain missing "
            "until a public official GeM source is independently identified. Third-party mirrors are not fetched."
        ),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "acceptance-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the official ICMAI ERP tender acquisition acceptance test.")
    parser.add_argument("--profile", type=Path, default=Path("recon/tenders/icmai_erp_2026.json"))
    parser.add_argument("--out", type=Path, default=Path("artifacts/icmai-erp-acceptance"))
    parser.add_argument("--allow-host", action="append", default=None, help="Additional exact public hostname; repeat as needed")
    parser.add_argument("--local-source-dir", type=Path, help="Import files downloaded manually from the official publisher; no network retrieval is performed")
    args = parser.parse_args()
    summary = run_acceptance(
        args.profile, args.out,
        set(args.allow_host) if args.allow_host else None,
        args.local_source_dir,
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
