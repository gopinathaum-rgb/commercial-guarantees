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

- Only public HTTP(S) resources are fetched. No login, CAPTCHA, paywall, robots, or access-control bypass.
- Exact-host restriction is the default; external hosts require explicit allowlisting.
- Page count, document count, response size, timeout, retries, and request pacing are bounded.
- This first slice enumerates ordinary HTML links and common document suffixes. It does not execute JavaScript, solve portal workflows, parse documents, or infer that a missing link means a document does not exist.
- Retrieval failures are recorded. A retrieved file is not thereby authenticated as an official or current tender version; publisher and version checks remain investigation steps.
- The module uses Python's standard library and does not require a paid search or scraping API.

## ICMAI acceptance test

Seed: `https://icmai.in/ClntAbout/Tender?page=-1`

The expected next increment is to make portal-specific link discovery robust for the ICMAI tender entry and GeM-linked document endpoints, then extract and compare the retrieved files. Do not treat this generic crawler as having already passed that tender-specific acceptance test.
