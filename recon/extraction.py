from __future__ import annotations

"""Document text extraction with source-location provenance.

Optional format libraries are imported only for the relevant format. Extraction
never changes the original acquired file; output is a JSON sidecar.
"""

import argparse
import csv
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ExtractedUnit:
    source_path: str
    source_sha256: str
    format: str
    locator: str
    kind: str
    text: str


@dataclass(frozen=True)
class ExtractionResult:
    source_path: str
    source_sha256: str
    format: str
    status: str
    units: tuple[ExtractedUnit, ...]
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_path": self.source_path,
            "source_sha256": self.source_sha256,
            "format": self.format,
            "status": self.status,
            "units": [asdict(unit) for unit in self.units],
            "error": self.error,
        }


def _unit(path: Path, digest: str, fmt: str, locator: str, kind: str, text: str) -> ExtractedUnit:
    return ExtractedUnit(str(path), digest, fmt, locator, kind, text)


def extract_document(path: Path) -> ExtractionResult:
    path = Path(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    suffix = path.suffix.lower()
    units: list[ExtractedUnit] = []
    try:
        if suffix == ".pdf":
            from pypdf import PdfReader
            reader = PdfReader(str(path))
            for index, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                units.append(_unit(path, digest, "pdf", f"page:{index}", "page_text", text))
        elif suffix == ".docx":
            from docx import Document
            doc = Document(str(path))
            for index, paragraph in enumerate(doc.paragraphs, start=1):
                if paragraph.text.strip():
                    units.append(_unit(path, digest, "docx", f"paragraph:{index}", "paragraph", paragraph.text))
            for t_index, table in enumerate(doc.tables, start=1):
                for r_index, row in enumerate(table.rows, start=1):
                    cells = [cell.text.replace("\n", " ").strip() for cell in row.cells]
                    units.append(_unit(path, digest, "docx", f"table:{t_index}/row:{r_index}", "table_row", " | ".join(cells)))
        elif suffix == ".xlsx":
            from openpyxl import load_workbook
            workbook = load_workbook(path, read_only=True, data_only=False)
            try:
                for sheet in workbook.worksheets:
                    for row in sheet.iter_rows():
                        for cell in row:
                            if cell.value is not None:
                                units.append(_unit(
                                    path, digest, "xlsx",
                                    f"sheet:{sheet.title}/cell:{cell.coordinate}",
                                    "cell", str(cell.value),
                                ))
            finally:
                workbook.close()
        elif suffix == ".csv":
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                for row_index, row in enumerate(csv.reader(handle), start=1):
                    units.append(_unit(path, digest, "csv", f"row:{row_index}", "row", " | ".join(row)))
        elif suffix == ".txt":
            for index, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
                units.append(_unit(path, digest, "txt", f"line:{index}", "line", line))
        else:
            raise ValueError(f"unsupported extraction format: {suffix or '[no extension]'}")
        return ExtractionResult(str(path), digest, suffix.lstrip("."), "extracted", tuple(units))
    except Exception as exc:
        return ExtractionResult(str(path), digest, suffix.lstrip(".") or "unknown", "failed", tuple(units), f"{type(exc).__name__}: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract document content with page/sheet/cell provenance.")
    parser.add_argument("path", type=Path)
    parser.add_argument("--out", type=Path, help="Optional JSON sidecar path")
    args = parser.parse_args()
    result = extract_document(args.path)
    payload = json.dumps(result.to_dict(), indent=2, ensure_ascii=False)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    print(payload)
    return 0 if result.status == "extracted" else 2


if __name__ == "__main__":
    raise SystemExit(main())
