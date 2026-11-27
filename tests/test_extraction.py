from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from openpyxl import Workbook
from docx import Document
from reportlab.pdfgen import canvas

from recon.extraction import extract_document


class ExtractionTests(unittest.TestCase):
    def test_extracts_pdf_with_page_locator(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "notice.pdf"
            pdf = canvas.Canvas(str(path))
            pdf.drawString(72, 720, "Milestone acceptance requires evidence.")
            pdf.showPage()
            pdf.save()
            result = extract_document(path)
            self.assertEqual(result.status, "extracted")
            self.assertEqual(result.units[0].locator, "page:1")
            self.assertIn("Milestone acceptance", result.units[0].text)

    def test_extracts_docx_paragraphs_and_table_rows(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "terms.docx"
            doc = Document()
            doc.add_paragraph("Payment follows acceptance.")
            table = doc.add_table(rows=1, cols=2)
            table.cell(0, 0).text = "Milestone"
            table.cell(0, 1).text = "20 percent"
            doc.save(path)
            result = extract_document(path)
            self.assertEqual(result.status, "extracted")
            self.assertTrue(any(u.locator == "paragraph:1" and "Payment" in u.text for u in result.units))
            self.assertTrue(any(u.locator == "table:1/row:1" and "20 percent" in u.text for u in result.units))

    def test_extracts_xlsx_with_sheet_and_cell_provenance(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "financial-bid.xlsx"
            book = Workbook()
            sheet = book.active
            sheet.title = "Price Schedule"
            sheet["A1"] = "Implementation"
            sheet["B1"] = 1250000
            book.save(path)
            result = extract_document(path)
            self.assertEqual(result.status, "extracted")
            self.assertTrue(any(u.locator == "sheet:Price Schedule/cell:B1" and u.text == "1250000" for u in result.units))

    def test_extracts_csv_rows(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "items.csv"
            path.write_text("Clause,Value\nLD,0.5% per week\n", encoding="utf-8")
            result = extract_document(path)
            self.assertEqual(result.status, "extracted")
            self.assertEqual(result.units[1].locator, "row:2")
            self.assertIn("0.5% per week", result.units[1].text)

    def test_unsupported_format_is_reported_not_silently_ignored(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "archive.zip"
            path.write_bytes(b"not extracted")
            result = extract_document(path)
            self.assertEqual(result.status, "failed")
            self.assertIn("unsupported extraction format", result.error)


if __name__ == "__main__":
    unittest.main()
