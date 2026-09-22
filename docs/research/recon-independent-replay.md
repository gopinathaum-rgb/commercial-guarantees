# Recon v0.1 — Independent Replay Result

## Purpose

This document records the first independent-reconstruction pass against the five-case Recon v0.1 baseline.

The test was performed from the recorded source fixtures and operator protocol, then compared with the canonical case tests.

This is a **fresh reconstruction pass, not a fully blind independent-human replay**. The same working context has access to the canonical implementation and tests. Therefore the result is evidence of reconstruction stability, not a definitive inter-operator reproducibility measurement.

## Replay result

### 1. WAPCOS × CYFUTURE

**Reconstructed subject:** WAPCOS-CYFUTURE.

**Core chronology:**

contract award → implementation activity → alleged non-performance / termination → blacklisting process → court-directed restoration → arbitration with merits expressly left open.

**Core claims:**

- contractual implementation obligations exist, but the full contractual condition set is not present in the fixture;
- WAPCOS alleges CYFUTURE failed stipulated terms;
- CYFUTURE's position conflicts with that allegation through its restoration/support position;
- the court's treatment preserves the dispute rather than adjudicating the implementation merits.

**Evidence relationships:** source observations support the respective party positions and procedural treatment; the later court reservation prevents upgrading the failure allegation into an established finding.

**Missing evidence:** full RFP/contract, milestones, acceptance/UAT evidence, correspondence, defect records, handover evidence, termination notice and related primary implementation records.

**Trajectory:** deteriorating / contested.

**Difference from canonical test:** none material. A second operator could reasonably add an explicit procedural/arbitration claim, but that is claim granularity, not a representation failure.

---

### 2. Sage Technologies × Shree Baidyanath

**Reconstructed subject:** SAGE-BAIDYANATH.

**Core chronology:**

contractual milestone conditions → Go-Live event → contemporaneous operational problems → dispute → judicial determination that Successful Go-Live was not established and UAT sign-off requirements were breached.

**Core claims:**

- Successful Go-Live was a contractual condition;
- Sage relied on the Go-Live event as evidence of success;
- Baidyanath relied on contemporaneous operational problems to dispute successful implementation;
- the court adjudicated that Successful Go-Live was not established.

**Evidence relationships:** Go-Live observation supports the party assertion; contemporaneous problems contradict that assertion; the later judicial finding resolves the disputed condition.

**Missing evidence:** complete PO/contract, complete UAT/sign-off package, defect records, acceptance correspondence and full implementation record.

**Trajectory:** deteriorating, ultimately adjudicated.

**Difference from canonical test:** none material.

---

### 3. NTRO × Corporate Infotech

**Reconstructed subject:** NTRO-CORPORATE-INFOTECH.

**Core chronology:**

contractual OSAT/PBG condition → NTRO takeover of system/site control → dispute over completion and payment → arbitral treatment of delay → later judicial treatment deeming OSAT completed for contractual consequences.

**Core claims:**

- successful OSAT was a contractual condition;
- NTRO disputed completion and related payment/PBG consequences;
- the takeover changed the evidence/control environment;
- OSAT was later deemed completed for contractual consequences.

**Evidence relationships:** the original contract supports the condition; the legal notice supports the dispute; the takeover record supports the changed evidence environment; the later judgment resolves the OSAT question for the stated contractual consequences.

**Missing evidence:** complete acceptance-testing package, contemporaneous test records, control/access logs, correspondence around takeover and full arbitral record.

**Trajectory:** transitioning/deteriorating dispute with later adjudicated resolution.

**Difference from canonical test:** no material representation failure. The independent reconstruction could additionally represent the arbitral finding that delay was attributable to both parties. That would increase claim granularity but does not require a new primitive.

---

### 4. Velocis × CONCOR

**Reconstructed subject:** VELOCIS-CONCOR.

**Core chronology:**

ten-milestone implementation schedule → vendor assertion of deployment/testing and missing sign-off → customer assertion that milestones remained incomplete → court treatment of delay/termination → performance-bank-guarantee invocation → court refusal to interfere with invocation on the supplied record.

**Core claims:**

- milestone completion and acceptance were contractual conditions;
- vendor asserted relevant milestone completion;
- CONCOR disputed completion;
- the court did not stay termination and did not restrain guarantee invocation on the supplied record.

**Evidence relationships:** the contractual schedule establishes the conditions; competing party statements preserve the dispute; later procedural treatment resolves the immediate guarantee-intervention question without establishing the full merits of implementation performance.

**Missing evidence:** signed milestone records, test results, field-user acceptance, 48-cycle evidence, termination record and complete guarantee correspondence.

**Trajectory:** deteriorating / contested.

**Difference from canonical test:** none material. The critical boundary—guarantee consequence without merits finality—is preserved.

---

### 5. Videocon × IBM

**Reconstructed subject:** VIDEOCON-IBM.

**Core chronology:**

service agreement → five milestone structure → disputed project-level invoices → arbitral project-by-project treatment → partial allowance/rejection of claims → limited High Court review.

**Core claims:**

- Project Service Charges were conditioned on project milestone progression;
- the parties disputed whether IBM had completed sufficient milestones;
- the tribunal treated entitlement project-by-project, allowing completed projects while rejecting claims with incomplete later milestones, double billing or non-progression.

**Evidence relationships:** the contractual milestone structure supports the condition; the parties' dispute establishes the competing claims; the arbitral treatment resolves the aggregate dispute through project-specific findings.

**Missing evidence:** complete project register, project-level milestone records, UAT/B2O evidence, scope-change records, invoice mapping and complete arbitral project schedules.

**Trajectory:** transition from commercial disagreement to adjudicated project-specific resolution.

**Difference from canonical test:** no material representation failure. The fixture compresses many project outcomes into relationship-level observations. Explicit project/subcase identity could improve future reconstruction detail, but the present case does not justify changing v0.1.

---

## Cross-case comparison

| Dimension | Replay result |
|---|---|
| Subject identity | Stable across all five |
| Chronology | Stable across all five |
| Contractual conditions | Representable; strongest limitation is missing primary contract detail in some fixtures |
| Claims | Representable; differences are mostly granularity |
| Claim status | Representable without inference |
| Evidence relationships | Supports, contradicts and resolves remain sufficient |
| Contradictions | Representable as competing claims/observations |
| Changed evidence/control environment | Representable without a new primitive |
| Resolution | Representable from procedural or adjudicated records |
| Uncertainty | Explicitly preservable |
| Trajectory | Useful as a derived summary, not a core proof artifact |
| Project/subcase detail | Compressed in Videocon × IBM, but not yet a demonstrated schema failure |

## Replay disagreements

The disagreements found in this pass are of three types:

### A. Claim-granularity differences

WAPCOS and NTRO can support additional claims beyond the canonical tests.

**Classification:** operator-level granularity difference.

**Action:** no schema change.

### B. Compressed commercial structure

Videocon × IBM contains many project-level outcomes that are summarized in relationship-level observations.

**Classification:** future detail/representation question.

**Action:** defer explicit project/subcase identity until repeated cases demonstrate that relationship-level reconstruction is insufficient.

### C. Trajectory interpretation

NTRO can reasonably be described as transitioning rather than simply deteriorating because the evidence environment changes and later adjudication establishes a contractual consequence.

**Classification:** interpretation difference.

**Action:** do not expand the trajectory vocabulary. Record the reasoning and preserve the underlying claims/evidence as the primary artifact.

## Gate result

The five cases continue to support the v0.1 model.

No repeated disagreement demonstrates a missing primitive.

The strongest recurring structure remains:

**condition → evidence → competing claim → contradiction → change → resolution / non-resolution → uncertainty**

The next validation step should therefore be **a genuine second-operator replay**, preferably performed by a person who has not seen the canonical claim/test construction.

Until that occurs, the correct conclusion is:

> **Recon v0.1 is provisionally stable under fresh reconstruction, but independent human reproducibility remains unproven.**

No runtime or schema changes are warranted from this replay.
