# Commercial Reality Reconnaissance v0.1

Recon v0.1 is an evidence-bound situation detector, not an autonomous sales agent.

## Operating model

source records → observations → states → changes → trajectory → investigation report

The human operator remains responsible for discovering and selecting sources, resolving ambiguous entities, deciding whether a source is credible enough to retain, investigating missing evidence, and deciding whether and how to engage.

The runtime provides repeatable memory and comparison: ingest source records, normalize observations, derive bounded state labels, detect state changes, assess observed directional movement, preserve source URLs and uncertainty language, and render a repeatable situation report.

## Deliberate limits

- No autonomous internet crawler.
- No customer-intent inference.
- No prediction.
- No prospect ranking.
- No outreach.
- No restricted Apollo people-search dependency.

## Run

python -m recon scan --input recon/sources/demo.jsonl --subject DemoCo

The demo is synthetic. Real runs should use curated source records collected by the operator.

## Next gate

Do not build autonomous crawling until several manually operated investigations show that the state/change/trajectory model consistently produces useful research decisions.
