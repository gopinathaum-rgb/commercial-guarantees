# Recon v0.1 — State Drift Cutoff Replay

## Purpose

Test whether state drift can be reconstructed **without hindsight** by applying historical cutoffs to the existing five-case replay baseline.

The test asks:

> At an earlier point in each commercial situation, using only evidence available by that cutoff, could an operator identify a material divergence between the required next state and the observed state?

This is an early-warning reconstruction test, not a prediction test.

## Method

For each case, use three conceptual views:

1. **Pre-resolution cutoff** — before formal termination, arbitration, judgment, or final adjudication.
2. **First observable gap** — earliest date supported by the available record where required and observed state materially diverge.
3. **Post-resolution control** — later record used only to check whether the earlier reconstruction was materially consistent. Later findings must not be used to create the earlier signal.

Classification:

- **Reproducible early drift** — the gap is observable before formal dispute resolution.
- **Partial** — a gap is visible, but the earliest date cannot be established from the available record.
- **Not established** — the available record only establishes the gap retrospectively.
- **Control/aligned** — evidence shows the required state was reached; no drift should be manufactured.

## Results

| Case | Pre-resolution evidence | Earliest supported gap | Early-warning result |
|---|---|---|---|
| WAPCOS × CYFUTURE | Publicly available record begins mainly with 2026 termination/restoration proceedings; later record describes earlier requests for backup/data but does not give enough dated evidence to establish the first divergence | Unknown from current public record | **Not established** |
| Sage Technologies × Shree Baidyanath | Go-Live occurred 1 Apr 2022; emails from 18 Apr onward record unresolved Go-Live issues, missing development objects and operational problems | 18 Apr 2022 (first presently supported dated post-Go-Live gap) | **Reproducible early drift** |
| NTRO × Corporate Infotech | Contract required completion by Feb 2019; supply was already 24 weeks late; OSAT did not begin until Feb 2020; initial OSAT recorded failed/not-conducted tests | No later than initial OSAT in Feb 2020; broader schedule drift was already visible earlier | **Reproducible early drift** |
| Velocis × CONCOR | Contract had explicit milestone gates; 2023 correspondence shows vendor testing, CONCOR testing and field-user deployment, while sign-off remained disputed; repeated extensions were later acknowledged | At least by Jul–Sep 2023; earlier onset cannot yet be established precisely | **Partial / reproducible gap, incomplete lead-time** |
| Videocon × IBM | Five milestone structure existed per project; some projects completed successfully while others stopped at UAT/B2O or earlier | Project-specific: gap visible when a project failed to progress to the next contractual milestone; exact earliest dates vary by project | **Reproducible at project level** |

## Case notes

### 1. WAPCOS × CYFUTURE

The 2026 court record establishes that WAPCOS alleged failure to provide ERP backup and later required restoration, passwords/passcodes and data. The Court directed restoration and handover, while expressly leaving the merits open.

This demonstrates a strong state gap:

- required state: operational ERP plus usable data/access/control;
- observed state: disputed service continuity and data accessibility.

But the available public record does **not** yet provide enough dated pre-dispute evidence to establish when that gap first became observable.

Therefore do not claim early warning for this case.

### 2. Sage × Shree Baidyanath

The contractual payment state was explicitly tied to successful milestones. The system went live on 1 Apr 2022, but emails beginning 18 Apr recorded unresolved issues. Later evidence records continuing problems and a dispute over whether Go-Live had actually been successfully achieved.

The key reconstruction is:

- required state: successful Go-Live sufficient to trigger the contractual next milestone;
- observed state at 18 Apr: system was live, but material issues remained;
- gap: operational launch did not yet establish successful contractual Go-Live;
- actor: implementation/customer teams jointly had actions affecting the transition;
- economic consequence: milestone payment/support relationship was already becoming entangled.

The later judgment is not needed to identify the existence of this early gap; it is used only as the post-resolution control.

### 3. NTRO × Corporate Infotech

The contract made acceptance testing and OSAT prerequisites for full commissioning and warranty commencement. The original completion date was 20 Feb 2019, and the record states equipment supply was already delayed by 24 weeks.

The historical record then shows OSAT beginning in February 2020, with 194 of 966 parametric tests initially failing and other tests not conducted. Subsequent evidence shows that both parties contributed to delay and that control of systems/sites later affected the ability to complete testing.

The strongest early signal is therefore not the eventual arbitration dispute. It is the earlier failure of the required transition:

- required state: delivery/installation/commissioning → successful OSAT → full commissioning;
- observed state: delayed supply and incomplete/failing acceptance testing;
- gap: the contractual completion state was not being reached on schedule.

This is a strong reproducible drift case.

### 4. Velocis × CONCOR

The contract contained ten explicit milestones, culminating in data migration/go-live and software acceptance. In 2023, the record contains dated communications concerning vendor testing, CONCOR testing and field-user deployment, while the parties disagreed about sign-off. By April 2024 the dispute had become formal enough for termination and performance-guarantee protection proceedings.

The state gap can therefore be reconstructed before termination:

- required state: successive testing/deployment/acceptance milestones;
- observed state: implementation/testing activity occurred, but contractual recognition/sign-off remained unresolved;
- consequence: payment and performance-guarantee exposure became linked to the unresolved transition.

However, the available record does not yet establish the **first** point of divergence. Therefore this case passes reproducibility of the gap but not precise lead-time reconstruction.

### 5. Videocon × IBM

This case is a useful control against overgeneralization.

The commercial relationship contained multiple projects, each with a five-stage milestone chain: Kick Off → Infra-Ready → UAT → B2O → B2O+90.

Some projects reached successful completion. Others did not progress beyond UAT or B2O. The later adjudication therefore does not imply that the whole relationship was drifting.

The correct reconstruction is project-specific:

- required state: next project milestone;
- observed state: project-specific completion status;
- gap: only where the project stopped short of its next required milestone;
- control: completed projects should remain aligned.

This validates the decision to defer a new project/subcase primitive rather than prematurely adding one to v0.1.

## Cross-case finding

The experiment supports three conclusions.

### 1. State drift is reproducible

Across materially different commercial situations, the same reconstruction object survives:

**required state → observed state → state gap → blocker → actor → economic consequence**

This is not dependent on a particular legal dispute or ERP implementation.

### 2. Hindsight can be separated from reconstruction

The strongest cases show that the gap existed in contemporaneous evidence before the later formal resolution:

- Sage: post-Go-Live issues were documented before the later judgment.
- NTRO: delay and testing failures were documented years before the later adjudication.
- Velocis: testing/sign-off divergence was documented before termination.
- Videocon: project-specific milestone failure can be reconstructed from project-level records.

WAPCOS is deliberately retained as a negative result because the currently available public record does not support a precise early cutoff.

### 3. Early-warning lead time is still not proven

The experiment does **not** establish that Recon could have intervened earlier or prevented failure.

The current evidence supports:

> **Historical state drift can often be reconstructed before formal resolution.**

It does not yet support:

> **Recon can reliably detect economically consequential drift early enough to change the outcome.**

That requires a separate test using contemporaneous source packets and blinded cutoffs.

## Decision

**Do not change the Recon v0.1 schema.**

The state-drift record survives the cutoff experiment.

The next validation target is narrower:

> Give an operator only the evidence available at a historical cutoff, hide all later documents, and ask for the state-drift record.

Success requires the operator to identify the same material gap without knowing the eventual outcome.

That is the first experiment capable of testing whether Recon creates **lead time**, rather than merely producing a better post-mortem.
