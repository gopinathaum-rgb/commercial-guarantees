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

- Only HTTP(S) resources are fetched. No login, CAPTCHA, paywall, or access-control bypass. Before fetching a page or document, Recon retrieves and enforces that origin's `robots.txt`. A 404/410 means no published policy; a 401/403 or other retrieval failure fails closed. Policy decisions are cached per origin for the run.
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

## ICMAI live acceptance runner

Run the official-source-only acquisition and extraction workflow:

```bash
python -m recon.icmai_acceptance --out ./artifacts/icmai-erp-acceptance
```

The runner reads the official listing URL and the exact publisher-linked document CDN host (`cdn.icmai.in`) from `recon/tenders/icmai_erp_2026.json`, enforces robots policy independently on both origins, acquires only documents linked from that listing, extracts every retrieved supported file, and writes:

- `acquired/acquisition-manifest.json` — source/final URL, retrieval time, HTTP status, content type, size and SHA-256.
- `extracted/extraction-manifest.json` — extracted units, locators and expected-document coverage.
- `acceptance-summary.json` — explicit missing/retrieval-failed/extraction-failed states and a strict pass flag.

The workflow intentionally does not fetch third-party mirrors or authenticate to GeM. Expected GeM-only attachments remain missing until an official, publicly accessible source is independently identified. A run can complete successfully while the acceptance criteria remain unmet; inspect `acceptance_passed` rather than treating process exit code zero as a pass.

A manually triggered GitHub Actions workflow is available at `.github/workflows/icmai-acceptance.yml`. Open Actions → ICMAI ERP Source Acceptance → Run workflow. The resulting acquisition and extraction evidence is uploaded as a 30-day artifact. GitHub-hosted network reachability is not guaranteed; a blocked source is recorded rather than bypassed.

### When a publisher-linked CDN blocks automated retrieval

The live ICMAI run found the four ERP PDFs linked from the official listing on `cdn.icmai.in`, but that host returned HTTP 403 for `/robots.txt`. Recon therefore failed closed and did not request those PDFs. This is recorded as a policy-retrieval failure, not as proof that the files are missing or that the host explicitly disallows them.

If the files are accessible in an ordinary browser, download them manually into one folder using the exact filenames in the profile, then run:

```bash
python -m recon.icmai_acceptance \
  --local-source-dir ./icmai-downloads \
  --out ./artifacts/icmai-erp-acceptance
```

Recon copies each matching file, computes SHA-256, and extracts it with page/paragraph/table/sheet/cell locators. The manifest labels these records `operator_supplied`, retains any known official source URL, and leaves publisher verification pending. They are **not** silently reclassified as crawler-retrieved or counted as a strict official-source acceptance pass. GeM-only attachments remain missing unless supplied and independently verified. For network runs, expected files whose official URLs were blocked by a robots-policy fetch failure are reported as `blocked_by_policy`, not `missing`.
