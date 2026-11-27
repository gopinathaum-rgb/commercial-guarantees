from email.message import Message
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from recon.acquisition import SourceAcquirer


class AcquisitionTests(unittest.TestCase):
    def test_discovers_and_downloads_linked_documents_with_hash_manifest(self):
        html = b"""<!doctype html><html><body>
        <a href="/files/rfp.pdf">RFP</a>
        <a href="/files/boq.xlsx" download>BOQ</a>
        <a href="https://outside.example/secret.pdf">outside</a>
        </body></html>"""
        pdf = b"%PDF-1.4 test document"
        xlsx = b"PK fake spreadsheet"
        with TemporaryDirectory() as tmp:
            acquirer = SourceAcquirer(Path(tmp), delay_seconds=0)
            def fake_get(url):
                headers = Message()
                if url.endswith("/tender"):
                    headers["Content-Type"] = "text/html; charset=utf-8"
                    return 200, headers, url, html
                headers["Content-Type"] = "application/pdf" if url.endswith(".pdf") else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return 200, headers, url, pdf if url.endswith(".pdf") else xlsx
            acquirer._get = fake_get
            result = acquirer.acquire("https://icmai.example/tender")
            self.assertEqual(result.pages_visited, 1)
            self.assertEqual(len(result.documents), 2)
            self.assertTrue(all(d.status == "retrieved" for d in result.documents))
            self.assertEqual(len({d.sha256 for d in result.documents}), 2)
            self.assertTrue((Path(tmp) / "acquisition-manifest.json").exists())
            self.assertTrue(all((Path(tmp) / d.path).exists() for d in result.documents))

    def test_rejects_non_http_seed(self):
        with TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                SourceAcquirer(Path(tmp)).acquire("file:///etc/passwd")

    def test_explicit_allowlist_is_exact(self):
        with TemporaryDirectory() as tmp:
            acquirer = SourceAcquirer(Path(tmp), allowed_hosts={"icmai.in"})
            self.assertTrue(acquirer._allowed("https://icmai.in/doc.pdf", "icmai.in"))
            self.assertFalse(acquirer._allowed("https://evil.icmai.in/doc.pdf", "icmai.in"))


if __name__ == "__main__":
    unittest.main()
