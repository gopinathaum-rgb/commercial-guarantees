# Recon v0.1 — Operator Protocol

## Purpose

Recon v0.1 is a disciplined research instrument, not an autonomous researcher.

The operator uses it to turn a messy commercial situation into a traceable reconstruction of:

**commitment → conditions → claims → evidence → contradiction → change → resolution → uncertainty**

The immediate validation question is:

> Can two human research operators repeatedly reconstruct real commercial situations using the same evidence discipline?

Do not automate a step merely because it can be automated. First establish that the step is repeatable and useful.

---

## Operating boundary

The human operator remains responsible for:

- choosing the commercial subject;
- locating and selecting sources;
- reading sources in context;
- deciding what a source actually establishes;
- distinguishing fact from allegation, response, procedural action, and unresolved dispute;
- resolving ambiguous entities;
- identifying missing primary evidence;
- creating claims and assigning their status;
- investigating contradictions;
- characterizing the resulting trajectory.

Recon currently assists with:

- source-record normalization;
- observation creation;
- chronological state construction;
- change detection;
- trajectory rendering;
- claim/evidence traceability;
- repeatable report generation.

Recon must not:

- infer customer intent;
- rank prospects;
- predict commercial outcomes;
- silently upgrade allegations into facts;
- treat repeated reporting as independent verification;
- invent missing evidence;
- send outreach;
- depend on restricted people-search infrastructure.

---

## Investigation protocol

### 1. Define the subject

State the bilateral or otherwise bounded commercial situation being investigated.

Prefer one timeline per commercial relationship or dispute.

Example:

`WAPCOS-CYFUTURE`

Do not split a single dispute into separate company timelines when doing so would destroy the sequence of commitment, performance, dispute, and resolution.

### 2. Find the strongest primary record

Start with the strongest available source:

- contract / purchase order;
- acceptance document;
- court order or judgment;
- arbitral award;
- formal notice;
- official project record.

Secondary reporting and practitioner traces can supplement the record, but should not silently replace primary evidence.

### 3. Read the source in context

Do not extract isolated sentences first.

Determine:

- who is speaking;
- what document is being described;
- what date matters;
- whether the statement is a fact, allegation, response, direction, reservation, or later finding;
- what the source does not establish.

### 4. Create source records

Record only what the source actually supports.

Every source record should have:

- stable source ID;
- URL;
- relevant date;
- publisher;
- concise source-grounded statement;
- entities;
- signal types where useful;
- evidence stance.

Use the stance vocabulary already implemented in Recon:

- `procedural_fact`
- `party_allegation`
- `party_response`
- `court_direction`
- `court_reservation`
- `practitioner_trace`

### 5. Normalize into observations

Run the source records through Recon.

Check:

- every source became the intended observation(s);
- entity normalization did not accidentally split one bilateral case;
- dates are ordered correctly;
- stance is preserved exactly.

If normalization is wrong, fix the source data rather than compensating downstream.

### 6. Build the commercial timeline

Read the observations chronologically.

Look specifically for:

- commitment creation;
- contractual completion conditions;
- implementation activity;
- acceptance / UAT;
- go-live or deployment;
- milestone payment;
- operational incident;
- notice;
- escalation;
- termination / abandonment;
- handover or change of control;
- arbitration / litigation;
- adjudicated treatment.

The timeline is descriptive. Do not turn it into a prediction.

### 7. Create explicit claims

Create a claim when the investigation needs to reason about something stronger than a raw observation.

Typical claim types:

- `contractual_condition`
- `performance_claim`
- `counter_claim`
- `procedural_claim`
- `adjudicated_finding`

Every claim must cite one or more observations.

Claim status is operator-supplied:

- `asserted`
- `disputed`
- `adjudicated`
- `unresolved`

Recon does not infer claim status.

### 8. Link evidence relationships

For each material claim, make the relationship explicit:

- `supports`
- `contradicts`
- `resolves`

Do not use a generic “evidence” label when the direction of the relationship is known.

### 9. Investigate contradictions

When two observations appear inconsistent, stop and investigate.

Ask:

1. Are they actually talking about the same condition?
2. Are they from different parties?
3. Did the contractual definition change the meaning?
4. Is one a later adjudicated treatment?
5. Is the apparent contradiction only a difference in timing?
6. What primary evidence is still missing?

Do not resolve the contradiction by intuition.

### 10. Record missing evidence

Explicitly record what would be needed to strengthen the reconstruction.

Typical missing evidence:

- signed contract / PO;
- acceptance criteria;
- UAT sign-off;
- deployment record;
- production verification;
- test results;
- change request;
- correspondence;
- defect / incident log;
- handover record;
- termination notice;
- payment record;
- arbitration or court record.

Missing evidence is itself a research result.

### 11. Assess trajectory

Use Recon's trajectory only as an observed-direction summary.

Permitted directions:

- stable;
- improving;
- deteriorating;
- transitioning;
- uncertain.

The current implementation is heuristic. Its confidence value is **not** a calibrated probability, reliability score, or forecast.

Trajectory is not:

- probability of failure;
- probability of winning;
- buying-intent score;
- prospect ranking;
- forecast.

If the evidence is materially contested, preserve that uncertainty.

### 12. Produce the Commercial Reality Record

The final report should answer:

1. What was promised?
2. What had to be true for completion?
3. What evidence says it happened?
4. What evidence disputes that?
5. What changed over time?
6. Was the dispute resolved, and how?
7. What remains uncertain?
8. What evidence would be required to make the commitment more bounded?

The report should let another operator reconstruct the reasoning without relying on unstated intuition.

---

## Quality gate

A case is **replayable** only if another operator can:

- identify the same subject;
- trace each material claim to observations;
- distinguish allegations from established findings;
- identify the same major contradictions;
- identify materially similar missing evidence;
- understand why the trajectory was characterized as it was;
- reproduce the report from the recorded inputs.

A case is **not** a successful replay merely because the generated report looks plausible.

---

## Five-case replay baseline

The v0.1 replay baseline now contains five materially different cases:

1. **WAPCOS × CYFUTURE** — disputed implementation / court intervention / merits reserved.
2. **Sage Technologies × Shree Baidyanath** — milestone conditions / operational dispute / judicial adjudication.
3. **NTRO × Corporate Infotech** — testing condition / control takeover / adjudicated treatment of completion.
4. **Velocis × CONCOR** — implementation milestones / termination / performance-guarantee consequence without merits finality.
5. **Videocon × IBM** — multiple project outcomes within one commercial relationship / project-specific milestone adjudication.

The fifth case did not require a new primitive.

Videocon × IBM did expose a possible future need for explicit project or subcase identity. That is deliberately **deferred**: one case is insufficient evidence for changing the v0.1 schema.

---

## Independent replay gate

The next validation step is no longer “add another case.”

It is:

> **Can a second operator reproduce the reconstruction from the recorded source material?**

For each case, compare:

- subject identity;
- chronology;
- material contractual conditions;
- claims;
- claim status;
- evidence links;
- contradictions;
- missing evidence;
- resolution treatment;
- uncertainty;
- trajectory characterization.

Record disagreements rather than silently reconciling them.

If disagreement repeatedly occurs at the same conceptual boundary, that boundary becomes a candidate for v0.2 design.

If disagreements are primarily source-selection or interpretation differences, improve the operator protocol rather than the schema.

---

## Operator rule

> **Do not automate uncertainty. Instrument it first.**

Recon v0.1 is successful if it makes disciplined human investigation more repeatable before it makes investigation more autonomous.
