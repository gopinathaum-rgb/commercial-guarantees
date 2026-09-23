# Recon — Economic-State Replay v0.2 Direction

## Purpose

This document defines the next Recon research experiment after the five-case v0.1 reconstruction.

The question is:

> **What can we actually prove about the changing economic state of a commercial commitment?**

This is a research model, not a financial product specification.

Recon must distinguish between:
- a commercial commitment;
- an asserted economic claim;
- a contractual entitlement;
- an earned or due amount;
- a disputed amount;
- an adjudicated amount;
- a settled amount.

No state may be inferred merely because money is mentioned in a source.

## Design principle

> **Money is interpreted through commercial conditions and evidence, not treated as a standalone fact.**

A monetary statement should therefore be traceable to:

amount → currency → economic state → contractual/commercial basis → evidence → effective time → uncertainty

The model must also preserve the difference between when an economic state became effective and when Recon learned about or recorded that state.

## Candidate economic-state vocabulary

These labels are deliberately provisional.

### committed
A commercial commitment exists, but the economic entitlement has not yet been established as earned or due.

### conditional
An economic consequence depends on one or more conditions that have not yet been established.

### claimed
A party asserts an economic entitlement or amount. claimed does not establish that the amount is contractually due.

### earned
The available evidence establishes that the contractual/commercial performance condition for the relevant economic consequence has been satisfied.

### due
The available evidence establishes that the amount is payable under the applicable commercial arrangement. earned and due must remain distinct because a contract can make payment dependent on additional timing or procedural conditions.

### invoiced
A monetary demand or invoice has been issued. invoiced does not establish due.

### disputed
The economic claim or its underlying condition is materially contested. A disputed claim may coexist with an earlier state; dispute is therefore better treated as a state dimension than as a simple terminal state.

### adjudicated
A competent adjudicative record establishes a material economic or contractual consequence. The scope of the adjudication must be preserved.

### settled
The economic obligation has been discharged or otherwise finally settled according to the available evidence.

### unresolved
The available evidence does not establish the final economic state. unresolved is an epistemic state, not a conclusion that no obligation exists.

## Important constraint

These labels are not yet a mandatory linear state machine.

Commercial reality can branch, split, partially resolve, or move between dimensions.

Example: a ₹10cr commitment can contain ₹6cr evidenced as earned, ₹2cr disputed, and ₹2cr still conditional.

The eventual implementation should therefore avoid forcing an entire contract into one monetary state.

## Economic-state record

A future economic-state record should be able to preserve at least:
- subject;
- economic claim identifier;
- amount;
- currency;
- economic state;
- commercial basis;
- relevant condition;
- supporting observation IDs;
- claim/evidence relationships;
- effective date;
- recorded/observed date;
- predecessor state or event;
- uncertainty;
- scope.

This is a candidate model only. It is not yet added to the v0.1 runtime.

# Five-case economic replay

The following is the research baseline against which a human/operator replay should be compared.

## 1. WAPCOS × CYFUTURE

### Commercial structure
ERP implementation contract following the RFP and award.

### Economic interpretation
The fixture establishes a commercial commitment and later competing positions concerning performance, termination, restoration and dispute resolution. It does not establish a final monetary entitlement from the supplied record.

### Candidate economic state
committed → conditional / performance-dependent → disputed → unresolved

Do not convert alleged implementation failure into established loss or extinguished payment entitlement.

Missing economic evidence includes the full contract/RFP, milestone/payment schedule, acceptance evidence, invoices/payment records, termination consequences, damages calculations and settlement/arbitration outcome.

## 2. Sage Technologies × Shree Baidyanath

### Commercial structure
SAP implementation with milestone-linked payments, including UAT sign-off and Successful Go-Live conditions.

### Economic interpretation
The evidence establishes that payment depended on specified implementation conditions. The court ultimately found that UAT sign-off requirements were breached and that Successful Go-Live was not established, affecting entitlement to later milestones.

### Candidate economic state
committed → conditional → claimed → disputed → adjudicated

Critical boundary: operational launch is not equivalent to contractual payment entitlement.

## 3. NTRO × Corporate Infotech

### Commercial structure
Contractual acceptance testing/OSAT, Performance Bank Guarantee, balance payment and warranty consequences.

### Economic interpretation
The evidence shows a change in the control environment when NTRO took over system/site access. A later judicial determination treated OSAT as completed on 17 March 2020 for stated contractual consequences and upheld PBG release.

### Candidate economic state
committed → conditional → disputed → adjudicated → economic consequence established

Critical boundary: the economic state changed partly because the evidence/control environment itself changed.

Recon must preserve condition + evidence environment + event + resulting economic consequence.

## 4. Velocis × CONCOR

### Commercial structure
Ten implementation milestones with testing, deployment, data migration, Go-Live and acceptance/warranty consequences.

### Economic interpretation
Completion of milestones was disputed. Termination followed. CONCOR invoked a performance bank guarantee. The court declined to interfere with the invocation on the supplied record, without converting that procedural treatment into a final merits finding on all underlying implementation questions.

### Candidate economic state
committed → conditional → claimed / disputed → termination → guarantee consequence

Critical boundary: a guarantee invocation is an economic consequence, not automatically proof that every underlying performance allegation was true.

## 5. Videocon × IBM

### Commercial structure
Project Service Charges tied to project-specific milestone progression.

### Economic interpretation
The tribunal treated entitlement project-by-project. Some project claims were established as completed and payable; other claims were rejected because later milestones were incomplete, projects did not proceed, or other contractual/accounting problems applied.

### Candidate economic state
contract-level commitment → project/milestone conditions → project-specific claims → some established / some rejected / some incomplete → partial adjudicated economic resolution

Critical boundary: the contract-level amount cannot safely be treated as one economic object.

# Cross-case findings

The five cases suggest that economic interpretation repeatedly requires five separations:

1. Commitment vs claim — a contractual commitment does not itself establish a monetary entitlement.
2. Claim vs evidence — a party asserting that money is due does not establish that it is due.
3. Performance vs economic consequence — completion, failure, termination, guarantee invocation and payment can have different evidentiary status.
4. Economic consequence vs merits finding — a court can permit or decline to interfere with a financial consequence without finally adjudicating every underlying commercial allegation.
5. Aggregate contract vs economic unit — one contract can contain multiple milestone/project-level economic claims with different states.

## Proposed next experiment

Do not implement these states in the runtime yet.

Perform an Economic-State Replay of the five cases.

For each case, the operator should produce:
- SUBJECT
- COMMERCIAL COMMITMENT
- ECONOMIC UNIT
- AMOUNT / CURRENCY: only where actually evidenced; otherwise explicitly not established
- INITIAL ECONOMIC STATE
- MATERIAL EVENTS
- STATE TRANSITIONS
- CLAIMED AMOUNTS
- EVIDENCED ENTITLEMENTS
- DISPUTED AMOUNTS
- ADJUDICATED CONSEQUENCES
- SETTLED AMOUNTS
- UNRESOLVED ECONOMIC QUESTIONS
- EVIDENCE FOR EACH TRANSITION
- BOUNDING CONDITION

The operator must be allowed to conclude: economic state not established. That is a successful Recon result when the evidence does not support a stronger conclusion.

## Success criterion

The model passes this research gate if the five cases can be represented without:
- treating invoices as proof of entitlement;
- treating claims as facts;
- treating guarantees as merits findings;
- treating contract value as earned value;
- forcing partial outcomes into one aggregate state;
- inventing amounts or settlement;
- losing the evidence basis for an economic transition.

A repeated failure that cannot be represented through existing source/observation/claim/evidence/change mechanisms becomes a candidate v0.2 schema issue.

## Relationship to AUM

Recon's role remains: **What economic state does the available evidence support?**

AUM's future role remains: **What bounded commitment can be constructed around that supported state?**

The capital-mobility question comes later: **Can a sufficiently bounded economic claim remain trackable and usable within the financial system while the surrounding commercial environment continues to change?**

That is a hypothesis, not a v0.2 product requirement.

## Guardrail

Recon must never represent stable money when the evidence only supports a bounded claim at a particular point in time.

The market, contract, counterparty, evidence environment and settlement status may continue to change.

The system's job is to preserve that change rather than hide it.

> **Do not make money appear stable. Make its changing state explainable.**