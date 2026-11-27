from email.message import Message
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from recon.acquisition import SourceAcquirer, _AllowedHostRedirectHandler


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

    def test_finds_data_attributes_and_onclick_attachment_urls(self):
        from recon.acquisition import _Links
        parser = _Links()
        parser.feed('<a data-url="/files/terms.pdf">Terms</a><button onclick="download(\'/files/atc.docx\')">ATC</button>')
        urls = {item[0] for item in parser.links}
        self.assertIn("/files/terms.pdf", urls)
        self.assertIn("/files/atc.docx", urls)

    def test_redirect_handler_rejects_hosts_outside_allowlist(self):
        from io import BytesIO
        from urllib.error import HTTPError
        from urllib.request import Request
        handler = _AllowedHostRedirectHandler(lambda url: url.startswith("https://icmai.in/"))
        request = Request("https://icmai.in/tender")
        headers = Message()
        with self.assertRaises(HTTPError):
            handler.redirect_request(request, BytesIO(b""), 302, "Found", headers, "https://evil.example/file.pdf")

    def test_redirect_handler_allows_explicitly_allowed_host(self):
        from io import BytesIO
        from urllib.request import Request
        handler = _AllowedHostRedirectHandler(
            lambda url: url.startswith("https://icmai.in/") or url.startswith("https://files.icmai.in/")
        )
        request = Request("https://icmai.in/tender")
        headers = Message()
        redirected = handler.redirect_request(
            request, BytesIO(b""), 302, "Found", headers, "https://files.icmai.in/rfp.pdf"
        )
        self.assertEqual(redirected.full_url, "https://files.icmai.in/rfp.pdf")

    def test_allowlist_adds_hosts_without_excluding_seed_host(self):
        with TemporaryDirectory() as tmp:
            acquirer = SourceAcquirer(Path(tmp), allowed_hosts={"files.icmai.in"})
            self.assertTrue(acquirer._allowed("https://icmai.in/tender", "icmai.in"))
            self.assertTrue(acquirer._allowed("https://files.icmai.in/rfp.pdf", "icmai.in"))
            self.assertFalse(acquirer._allowed("https://evil.example/rfp.pdf", "icmai.in"))

    def test_icmai_profile_names_expected_documents_and_preserves_unknowns(self):
        import json
        profile = json.loads(Path("recon/tenders/icmai_erp_2026.json").read_text())
        roles = {item["role"] for item in profile["expected_documents"]}
        self.assertTrue({"main_bid", "pre_bid_minutes", "corrigendum_2", "corrigendum_3", "buyer_added_atc", "financial_bid"} <= roles)
        self.assertTrue(any("closing time conflict" in item.lower() for item in profile["known_unknowns"]))
        self.assertIn("Do not mark a third-party mirror as official publisher evidence.", profile["acceptance_criteria"])


if __name__ == "__main__":
    unittest.main()
