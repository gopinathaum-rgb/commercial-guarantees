from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import json
import unittest
from unittest.mock import patch

from recon.icmai_acceptance import run_acceptance


class IcmAIAcceptanceTests(unittest.TestCase):
    def test_acceptance_summary_does_not_call_missing_documents_a_pass(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = root / "profile.json"
            profile.write_text(json.dumps({
                "profile_id": "test",
                "bid_number": "GEM/2026/B/8263375",
                "official_listing_url": "https://icmai.example/tenders",
                "official_document_hosts": ["cdn.icmai.example"],
                "expected_documents": [{"role": "main_bid", "filename": "main.pdf", "publisher": "ICMAI"}],
            }))
            acquisition_dir = root / "out" / "acquired"
            acquisition_dir.mkdir(parents=True)
            (acquisition_dir / "acquisition-manifest.json").write_text(json.dumps({
                "seed_url": "https://icmai.example/tenders",
                "started_at": "2026-11-27T00:00:00+00:00",
                "completed_at": "2026-11-27T00:00:01+00:00",
                "pages_visited": 0,
                "page_snapshots": [],
                "documents": [],
                "errors": [],
            }))
            fake_result = SimpleNamespace(
                started_at="2026-11-27T00:00:00+00:00",
                completed_at="2026-11-27T00:00:01+00:00",
                documents=(),
                errors=(),
            )
            fake_extraction = {
                "expected_documents": [{
                    "role": "main_bid", "filename": "main.pdf",
                    "acquisition_state": "missing", "extraction_status": None,
                }],
                "summary": {
                    "extracted_count": 0,
                    "extraction_failed_count": 0,
                },
            }
            with patch("recon.icmai_acceptance.SourceAcquirer") as acquirer, patch(
                "recon.icmai_acceptance.extract_acquisition_manifest", return_value=fake_extraction
            ):
                acquirer.return_value.acquire.return_value = fake_result
                summary = run_acceptance(profile, root / "out")
                self.assertEqual(acquirer.call_args.kwargs["allowed_hosts"], {"cdn.icmai.example"})
            self.assertFalse(summary["acceptance_passed"])
            self.assertEqual(summary["expected_missing_count"], 1)
            self.assertFalse(summary["third_party_sources_fetched"])
            self.assertTrue((root / "out" / "acceptance-summary.json").exists())


if __name__ == "__main__":
    unittest.main()
