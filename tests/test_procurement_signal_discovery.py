import unittest
from scripts.procurement_signal_discovery import extract_procurement_signals

SOURCE = {
    "organisation": "Example Institute",
    "url": "https://www.fsid-iisc.in/tenders/",
    "source_kind": "official_buyer_tender_page",
}

class ProcurementSignalTests(unittest.TestCase):
    def test_extracts_erp_tender_as_unqualified_procurement_signal(self):
        html = """
        <html><body><h1>Open Tenders</h1>
        <p>Procurement notice and bid information</p>
        <a href="/files/erp-rfp.pdf">Selection of SAP ERP Solution &amp; Implementation Partner (RFP)</a>
        </body></html>
        """
        rows = extract_procurement_signals(html, SOURCE)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["signal_type"], "formal_procurement_signal_unqualified")
        self.assertEqual(rows[0]["buyer_status"], "not_qualified")
        self.assertEqual(rows[0]["procurement_route_status"],
                         "blocked_pending_document_and_legal_review")

    def test_captures_page_when_notice_link_is_labelled_download(self):
        html = """
        <html><body><h1>Tenders</h1>
        <h2>Tender for Implementation and Support of Enterprise Resource Planning (ERP) Solution</h2>
        <p>Notice inviting tender. Closing date and bid submission information.</p>
        <a href="/files/notice.pdf">Download</a>
        </body></html>
        """
        rows = extract_procurement_signals(html, SOURCE)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["notice_url"], SOURCE["url"])
        self.assertIn("Implementation and Support", rows[0]["title"])

    def test_ignores_unrelated_tender(self):
        html = '<a href="/laptop.pdf">Procurement of laptops (Tender)</a>'
        self.assertEqual(extract_procurement_signals(html, SOURCE), [])

    def test_ignores_non_official_external_notice_link(self):
        html = '<a href="https://thirdparty.example/erp">ERP implementation RFP tender</a>'
        self.assertEqual(extract_procurement_signals(html, SOURCE), [])

    def test_requires_procurement_context(self):
        html = '<a href="/erp.html">ERP implementation partner information</a>'
        self.assertEqual(extract_procurement_signals(html, SOURCE), [])

if __name__ == "__main__":
    unittest.main()
