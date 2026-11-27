from __future__ import annotations

"""Run the ICMAI ERP tender source-acquisition and extraction acceptance workflow.

This command reads only the official listing URL in the checked-in profile.
It does not fetch third-party mirrors or authenticate to GeM.
"""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.parse import urlparse

from recon.acquisition import SourceAcquirer
from recon.extraction import extract_acquisition_manifest


def run_acceptance(profile_path: Path, output_dir: Path, allowed_hosts: set[str] | None = None) -> dict:
    profile_path = Path(profile_path)
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    seed_url = profile["official_listing_url"]
    seed_host = urlparse(seed_url).hostname
    if not seed_host:
        raise ValueError("official_listing_url must contain a hostname")
    output_dir = Path(output_dir)
    acquisition_dir = output_dir / "acquired"
    extraction_dir = output_dir / "extracted"

    approved_hosts = set(profile.get("official_document_hosts", []))
    approved_hosts.update(allowed_hosts or set())
    acquisition = SourceAcquirer(
        acquisition_dir,
        max_pages=1,
        max_documents=100,
        max_bytes=50 * 1024 * 1024,
        delay_seconds=0.5,
        allowed_hosts=approved_hosts or None,
    ).acquire(seed_url)
    acquisition_manifest = acquisition_dir / "acquisition-manifest.json"
    extraction = extract_acquisition_manifest(
        acquisition_manifest,
        profile_path=profile_path,
        output_dir=extraction_dir,
    )

    expected = extraction["expected_documents"]
    summary = {
        "profile_id": profile.get("profile_id"),
        "bid_number": profile.get("bid_number"),
        "started_at": acquisition.started_at,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "official_seed_url": seed_url,
        "official_seed_host": seed_host,
        "robots_policy_enforced": True,
        "third_party_sources_fetched": False,
        "acquisition_manifest": str(acquisition_manifest),
        "extraction_manifest": str(extraction_dir / "extraction-manifest.json"),
        "acquisition_document_count": len(acquisition.documents),
        "retrieved_document_count": sum(item.status == "retrieved" for item in acquisition.documents),
        "retrieval_failure_count": sum(item.status != "retrieved" for item in acquisition.documents),
        "expected_document_count": len(expected),
        "expected_missing_count": sum(item["acquisition_state"] == "missing" for item in expected),
        "expected_retrieval_failed_count": sum(item["acquisition_state"] == "retrieval_failed" for item in expected),
        "extracted_document_count": extraction["summary"]["extracted_count"],
        "extraction_failure_count": extraction["summary"]["extraction_failed_count"],
        "expected_document_states": expected,
        "acquisition_errors": list(acquisition.errors),
        "acceptance_passed": (
            len(expected) > 0
            and all(item["acquisition_state"] == "extracted" for item in expected)
            and extraction["summary"]["extraction_failed_count"] == 0
            and not acquisition.errors
        ),
        "acceptance_note": (
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
    args = parser.parse_args()
    summary = run_acceptance(args.profile, args.out, set(args.allow_host) if args.allow_host else None)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
