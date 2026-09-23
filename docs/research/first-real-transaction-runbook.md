# First Real Transaction — Operator Runbook v0.1

## Purpose
Turn the first real portal submission into a disciplined commercial experiment.

This runbook is intentionally manual. It does not expand Recon or Evidence OS.

## Entry condition
A real company submits a transaction-shaped case through the portal.

Do not request confidential material until a private channel has been established.

## Stage 0 — Intake integrity
Record:
- submission timestamp;
- submitting party and company;
- transaction type;
- current stage;
- commitment summary;
- deadline;
- amount and currency;
- commercial consequence;
- evidence categories claimed available;
- immediate commercial problem.

Do not treat any submitted statement as an established fact.

## Stage 1 — Define the economic object
Before reconstructing evidence, state:
- what commercial commitment is being examined;
- what specific economic consequence depends on it;
- the unit whose state could change;
- what is explicitly outside scope.

Examples: one implementation milestone; one acceptance event; one payment-triggering condition; one guarantee/security consequence.

Do not begin with the whole contract if the commercial decision concerns one milestone.

## Stage 2 — Establish the bounded question
Write one question that could be answered from evidence.

Good: Can completion of the agreed production-deployment milestone be established by the contractual deadline under the specified acceptance conditions?
Bad: Did the vendor successfully complete the project?

The question must identify the commitment, condition, time boundary, and consequence where relevant.

## Stage 3 — Evidence reconstruction
Request only the minimum evidence needed to answer the bounded question.

Possible evidence: contract or relevant clause; milestone definition; acceptance criteria; deployment record; UAT/acceptance results; production verification; correspondence; ticket/change history; invoice or payment record; guarantee/security instrument; adjudication or settlement record.

For each material item record: source → observation → claim → evidence relationship.

Preserve competing claims and contradictions.

## Stage 4 — Economic-state determination
Classify only what the evidence supports.

Provisional vocabulary: committed, conditional, claimed, earned, due, invoiced, disputed, adjudicated, settled, unresolved.

These are not assumed to be a single linear state machine.

A successful result may be: Economic state not established from available evidence.

Never convert: invoice into entitlement; operational event into contractual completion; allegation into fact; guarantee invocation into merits finding; adjudication into settlement.

## Stage 5 — Commercial decision
Answer only the decision the customer actually needs.

Possible outputs: completion can be established; completion cannot yet be established; completion is disputed and the available evidence does not resolve it; a specific economic consequence is established while underlying merits remain unresolved; additional evidence or a clearer verification condition is required.

Then state the minimum evidence or verification condition that would make the commitment more bounded.

## Stage 6 — Customer value test
Ask the customer:
1. Did this reconstruction clarify a real commercial decision?
2. Did it identify evidence that was actually missing or disputed?
3. Would establishing this boundary have economic value?
4. Would they use this before or during a future commitment?
5. Who would pay for that outcome, and under what commercial arrangement?

Do not pitch a larger product before these answers.

## Stage 7 — Founder gate
After the first transaction, record:
- what the customer actually needed;
- what evidence was available;
- where manual work was required;
- what caused delay or ambiguity;
- what output the customer valued;
- whether the customer requested another case;
- whether money changed hands or a concrete commercial commitment followed.

Only repeated evidence should justify automation.

## Stop rule
If the first transaction is completed without exposing a repeated workflow bottleneck, do not build software for it.

If the same bottleneck appears across multiple real transactions, then evaluate whether it belongs in Recon, Evidence OS, the portal, or an operator procedure.

> Do not automate uncertainty. Instrument it first.