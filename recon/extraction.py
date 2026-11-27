from __future__ import annotations

"""Document text extraction with source-location provenance.

Optional format libraries are imported only for the relevant format. Extraction
never changes the original acquired file; output is a JSON sidecar.
"""

import argparse
import csv
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
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


def extract_acquisition_manifest(
    manifest_path: Path,
    *,
    profile_path: Path | None = None,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    """Extract every retrieved item and reconcile expected files against acquisition."""
    manifest_path = Path(manifest_path)
    acquisition = json.loads(manifest_path.read_text(encoding="utf-8"))
    output_dir = Path(output_dir) if output_dir else manifest_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    acquired = acquisition.get("documents", [])
    by_name = {
        Path(item.get("path") or item.get("filename") or "").name: item
        for item in acquired
        if item.get("path") or item.get("filename")
    }

    expected = []
    if profile_path:
        profile = json.loads(Path(profile_path).read_text(encoding="utf-8"))
        expected = profile.get("expected_documents", [])

    expected_report = []
    for item in expected:
        name = Path(item["filename"]).name
        record = next((
            candidate for candidate in acquired
            if any(
                Path(str(candidate.get(field) or "").split("?", 1)[0]).name == name
                or Path(str(candidate.get(field) or "")).name.endswith("-" + name)
                for field in ("path", "filename", "source_url", "final_url")
            )
        ), None)
        if record is None:
            state = "missing"
            extraction_status = None
        elif record.get("status") != "retrieved" or not record.get("path"):
            state = "retrieval_failed"
            extraction_status = None
        else:
            state = "acquired_pending_extraction"
            extraction_status = None
        expected_report.append({
            "role": item.get("role"),
            "filename": name,
            "acquired_path": record.get("path") if record else None,
            "publisher_claim": item.get("publisher"),
            "acquisition_state": state,
            "extraction_status": extraction_status,
            "source_url": record.get("source_url") if record else None,
            "sha256": record.get("sha256") if record else None,
        })

    extracted_documents = []
    for record in acquired:
        if record.get("status") != "retrieved" or not record.get("path"):
            continue
        source_path = (manifest_path.parent / record["path"]).resolve()
        try:
            source_path.relative_to(manifest_path.parent.resolve())
        except ValueError:
            extracted_documents.append({
                "source_path": record["path"],
                "status": "failed",
                "error": "manifest path escapes acquisition directory",
            })
            continue
        result = extract_document(source_path)
        sidecar_name = f"{result.source_sha256[:12]}-{source_path.name}.extraction.json"
        sidecar_path = output_dir / sidecar_name
        sidecar_path.write_text(
            json.dumps(result.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        extracted_documents.append({
            "source_path": record["path"],
            "source_url": record.get("source_url"),
            "sha256": result.source_sha256,
            "format": result.format,
            "status": result.status,
            "unit_count": len(result.units),
            "sidecar": sidecar_name,
            "error": result.error,
        })

    extraction_by_name = {
        Path(item["source_path"]).name: item for item in extracted_documents
    }
    for item in expected_report:
        extracted = extraction_by_name.get(Path(item["acquired_path"] or "").name)
        if extracted:
            item["extraction_status"] = extracted["status"]
            item["acquisition_state"] = (
                "extracted" if extracted["status"] == "extracted" else "extraction_failed"
            )

    report = {
        "acquisition_manifest": str(manifest_path),
        "profile": str(profile_path) if profile_path else None,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "acquisition_errors": acquisition.get("errors", []),
        "expected_documents": expected_report,
        "extracted_documents": extracted_documents,
        "summary": {
            "expected_count": len(expected_report),
            "expected_missing_count": sum(x["acquisition_state"] == "missing" for x in expected_report),
            "expected_retrieval_failed_count": sum(x["acquisition_state"] == "retrieval_failed" for x in expected_report),
            "extracted_count": sum(x["status"] == "extracted" for x in extracted_documents),
            "extraction_failed_count": sum(x["status"] == "failed" for x in extracted_documents),
        },
    }
    (output_dir / "extraction-manifest.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract documents with provenance, individually or from an acquisition manifest.")
    parser.add_argument("path", nargs="?", type=Path, help="Single document path")
    parser.add_argument("--out", type=Path, help="Single-document JSON sidecar path")
    parser.add_argument("--manifest", type=Path, help="Acquisition manifest to process as a batch")
    parser.add_argument("--profile", type=Path, help="Optional expected-document profile JSON")
    parser.add_argument("--out-dir", type=Path, help="Output directory for batch sidecars and report")
    args = parser.parse_args()

    if args.manifest:
        if args.path or args.out:
            parser.error("use either a single document path or --manifest, not both")
        report = extract_acquisition_manifest(
            args.manifest, profile_path=args.profile, output_dir=args.out_dir
        )
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report["summary"]["extraction_failed_count"] == 0 else 2

    if not args.path:
        parser.error("provide a document path or --manifest")
    result = extract_document(args.path)
    payload = json.dumps(result.to_dict(), indent=2, ensure_ascii=False)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    print(payload)
    return 0 if result.status == "extracted" else 2


if __name__ == "__main__":
    raise SystemExit(main())
