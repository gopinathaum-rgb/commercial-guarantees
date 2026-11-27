# Recon public source acquisition (v0.1)

Recon can now inspect a public HTML source page, enumerate linked document files, retrieve them, and write a provenance manifest.

## Run

```bash
python -m recon.acquisition --url "https://publisher.example/tender" --out ./acquisitions/tender
```

By default, retrieval is restricted to the seed page's exact hostname. Add exact, explicitly approved hosts with repeated `--allow-host` options when a publisher links documents from a separate public host:

```bash
python -m recon.acquisition --url "https://publisher.example/tender" --out ./acquisitions/tender --allow-host files.publisher.example
```

The manifest records source and final URLs, retrieval time, HTTP status, content type, byte size, local path, and SHA-256. Same-named files are not overwritten.

## Safety and current limits

- Only HTTP(S) resources are fetched. No login, CAPTCHA, paywall, or access-control bypass. This version does not yet automatically retrieve and enforce `robots.txt`; operators must confirm that the target permits automated access before running it.
- Exact-host restriction is the default; external hosts require explicit allowlisting. The same boundary is enforced on every HTTP redirect.
- Page count, document count, response size, timeout, retries, and request pacing are bounded.
- This first slice enumerates ordinary HTML links and common document suffixes. It does not execute JavaScript, solve portal workflows, parse documents, or infer that a missing link means a document does not exist.
- This is an operator-directed research tool, not yet a hardened service for arbitrary untrusted URLs; private-network/DNS-rebinding protections and automated robots-policy enforcement remain future hardening work.
- Retrieval failures are recorded. A retrieved file is not thereby authenticated as an official or current tender version; publisher and version checks remain investigation steps.
- The module uses Python's standard library and does not require a paid search or scraping API.

## Provenance-aware extraction

Run extraction on an acquired file without modifying the original:

```bash
python -m recon.extraction ./acquisitions/tender/<file>.pdf --out ./acquisitions/tender/<file>.extraction.json
```

Supported in this increment:

- PDF: one text unit per page (`page:N`).
- DOCX: non-empty paragraphs and table rows (`paragraph:N`, `table:N/row:N`).
- XLSX: non-empty cells with sheet and cell coordinates (`sheet:NAME/cell:A1`). Formulas are preserved as formulas; cached formula results are not substituted.
- CSV: one unit per row (`row:N`).
- TXT: one unit per line (`line:N`).

Each extracted unit carries the original file path and SHA-256. Extraction failures and unsupported formats are explicit. A successful extraction does not validate the document's authenticity, completeness, legal effect, or current status. Legacy DOC/XLS, scanned-image OCR, PPT, ODT/ODS, ZIP expansion, and layout-perfect table reconstruction are not supported in this increment.

## ICMAI acceptance test

Seed: `https://icmai.in/ClntAbout/Tender?page=-1`

The expected next increment is to make portal-specific link discovery robust for the ICMAI tender entry and GeM-linked document endpoints, then extract and compare the retrieved files. Do not treat this generic crawler as having already passed that tender-specific acceptance test.


## ICMAI ERP acceptance profile

The known ICMAI ERP document inventory and unresolved retrieval questions are captured in `recon/tenders/icmai_erp_2026.json`. It is an acceptance-test manifest, not evidence that the files have already been downloaded. The profile deliberately labels the Tenderkart page as a third-party discovery/recovery source and preserves the GeM closing-time discrepancy as unresolved until the live bid record is checked.

## Batch acquisition-to-extraction workflow

After acquisition, process every retrieved document and compare the inventory against the ICMAI acceptance profile:

```bash
python -m recon.extraction \
  --manifest ./acquisitions/icmai/acquisition-manifest.json \
  --profile recon/tenders/icmai_erp_2026.json \
  --out-dir ./acquisitions/icmai/extracted
```

This writes one provenance sidecar per extracted file plus `extraction-manifest.json`. The report distinguishes expected files that are missing, retrieval failures, successful extraction, and extraction failures. It does not treat third-party-hosted files as official publisher evidence; source and publisher verification remain separate review steps.
