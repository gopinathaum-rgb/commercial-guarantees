# Commercial Reality Reconnaissance v0.1

Recon v0.1 is an evidence-bound research instrument for reconstructing consequential commercial situations. It is not an autonomous sales agent or autonomous researcher.

## Core question

> **What can we actually prove about a commercial commitment from the evidence available?**

Recon turns messy commercial history into a traceable reconstruction:

**commitment → conditions → observations → claims → evidence relationships → change → resolution → uncertainty**

The intended output is a **Commercial Reality Record** that another operator can replay without relying on unstated intuition.

## Operating model

```
source records
    ↓
observations
    ↓
states / changes
    ↓
claims + evidence links
    ↓
trajectory
    ↓
Commercial Reality Record
```

The human operator remains responsible for discovering and selecting sources, reading them in context, resolving ambiguous entities, identifying missing evidence, creating claims, assigning claim status, investigating contradictions, and deciding whether and how to engage.

The runtime provides repeatable memory and comparison: source normalization, observation creation, chronological state construction, change detection, trajectory rendering, claim/evidence traceability, and report generation.

## v0.1 evidence model

### SourceRecord

A source-grounded record containing:

- stable source ID;
- URL;
- relevant date;
- publisher;
- concise source-grounded statement;
- entity references;
- optional signal types;
- evidence stance.

### Observation

A normalized representation of a source statement tied to a subject and date.

### Claim

An operator-created statement that requires reasoning beyond a raw observation.

Claim types:

- `contractual_condition`
- `performance_claim`
- `counter_claim`
- `procedural_claim`
- `adjudicated_finding`

Claim status is explicitly supplied by the operator:

- `asserted`
- `disputed`
- `adjudicated`
- `unresolved`

Recon does not infer claim status.

### EvidenceLink

A directional relationship between a claim and an observation:

- `supports`
- `contradicts`
- `resolves`

### State / Change

States capture bounded labels derived from an observation. Changes record additions and removals between successive observed states.

These are descriptive instruments, not predictions.

### Trajectory

Trajectory provides an observed directional summary:

- `stable`
- `improving`
- `deteriorating`
- `transitioning`
- `uncertain`

The current trajectory implementation is a **heuristic research aid** based on observed signal vocabulary. Its confidence value is **not a calibrated probability, reliability score, or forecast**. Contested evidence is deliberately bounded rather than converted into apparent certainty.

Trajectory must never be interpreted as:

- probability of failure;
- probability of winning;
- buying intent;
- prospect quality;
- commercial forecast.

## What five real replays established

Recon v0.1 has now been replayed against five materially different commercial patterns:

1. **WAPCOS × CYFUTURE** — disputed implementation, termination, court intervention, merits reserved.
2. **Sage Technologies × Shree Baidyanath** — milestone conditions, operational dispute, judicial adjudication.
3. **NTRO × Corporate Infotech** — acceptance-testing condition, change of control, adjudicated treatment of completion.
4. **Velocis × CONCOR** — implementation milestones, termination, performance-guarantee consequence without merits finality.
5. **Videocon × IBM** — multiple project outcomes within one commercial relationship, including partial milestone completion and project-specific adjudication.

Across these cases, the same reconstruction pattern remained usable:

**condition → evidence → competing claim → contradiction → change → resolution / non-resolution → uncertainty**

No new schema primitive was required by the fifth case.

The Videocon × IBM replay exposed a possible future need for explicit sub-project identity, but one case is insufficient evidence for adding that abstraction. v0.1 therefore deliberately keeps one subject timeline and represents project-specific distinctions through claims and observations.

## Stable v0.1 specification

The following are frozen for validation:

- source-grounded observations;
- explicit evidence stance;
- explicit operator-created claims;
- explicit claim status;
- directional evidence links;
- chronological state/change representation;
- bounded trajectory vocabulary;
- source traceability;
- explicit uncertainty language;
- human operator responsibility for interpretation.

The following are **not** part of v0.1:

- autonomous web crawling;
- customer-intent inference;
- prospect ranking;
- outcome prediction;
- outreach;
- restricted people-search dependency;
- automatic claim-status inference;
- calibrated scoring;
- project/subcase primitives;
- automatic resolution of contradictions.

## Commercial Reality Record

A completed investigation should answer:

1. **Commitment** — What was promised?
2. **Conditions** — What had to be true for completion?
3. **Evidence** — What evidence establishes those conditions?
4. **Competing claims** — Who says what?
5. **Contradictions** — Where does the evidence conflict?
6. **Changes** — What materially changed over time?
7. **Resolution** — What, if anything, was subsequently established?
8. **Uncertainty** — What remains unproven?
9. **Bounding requirements** — What additional evidence or verification condition would make the commitment more objectively bounded?

The ninth question is the bridge from Recon into the broader AUM research thesis.

## Replay acceptance gate

Recon v0.1 is considered validated as a research instrument only if another operator can, from the recorded inputs:

- identify the same commercial subject;
- trace material claims to observations;
- distinguish allegations, responses, procedural acts, and findings;
- identify the major contradictions;
- identify materially similar missing evidence;
- understand the basis for the trajectory characterization;
- reproduce the Commercial Reality Record.

A passing software test is necessary but not sufficient.

## Deliberate limits

- No autonomous internet crawler.
- No customer-intent inference.
- No prediction.
- No prospect ranking.
- No outreach.
- No restricted Apollo people-search dependency.
- No automation of uncertainty before the underlying operator workflow is shown to be repeatable.

## Run

```
python -m recon scan --input recon/sources/demo.jsonl --subject DemoCo
```

The demo is synthetic. Real investigations use curated source records collected and interpreted by the operator.

## Next gate

Do not add new schema primitives or autonomous crawling yet.

The next validation step is **independent replay**: have a second operator reconstruct the existing cases from the recorded source material and compare the resulting Commercial Reality Records.

> **Do not automate uncertainty. Instrument it first.**
