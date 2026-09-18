# Commercial Validation

## Current Phase

**Phase 2 — Commercial validation**

The technical guarantee lifecycle has been exercised as a reference implementation. The current objective is different: determine whether a real buyer values a bounded commercial commitment enough to use and pay for it.

## Current Hypothesis

The first research wedge is:

> A customer or implementation vendor may value bounded certainty that a specifically defined enterprise software production milestone will either be demonstrated against agreed evidence or fall within a predefined guarantee response.

The initial milestone is **production deployment by a fixed deadline with objectively defined acceptance tests**.

See the [enterprise software implementation reference case](../examples/enterprise-software-implementation.md).

## What Has Been Technically Demonstrated

The private implementation repository has exercised the lifecycle:

`Obligation → Assessment → Commitment → Issued Guarantee → Evidence → Trigger → Claim → Settlement → Final Verification → Replay rejection`

The private implementation exercises structured deployment evidence, acceptance-test results, production verification, and provenance-aware realization. The public reference case describes these elements as a proposed commercial workflow, not as evidence from a live customer deployment.

Technical validation is not commercial validation.

## What Is Not Yet Proven

The following remain open:

- a real customer has an urgent recurring problem;
- the problem is economically meaningful;
- the customer prefers a guarantee to existing controls;
- the required evidence can be collected in a real deployment;
- an independent evidence/provenance model is acceptable to both parties;
- a buyer will pay a fee for the mechanism;
- the proposed settlement process is acceptable;
- a real project is suitable for a pilot.

## Customer Discovery

Initial outreach is focused on enterprise software implementation vendors that appear to have recurring deployments and contractual milestones. This describes the current target population, not a validated market characteristic.

The interview sequence is:

1. **Problem** — What happens commercially when a production milestone slips?
2. **Frequency** — How often does this occur?
3. **Consequence** — What payment, dispute, escalation, or customer impact follows?
4. **Evidence** — How is completion established today?
5. **Buyer** — Who owns the economic problem?
6. **Value** — What would bounded certainty change?
7. **Price** — Would the mechanism justify a fee?
8. **Pilot** — Is there a named real project on which it could be tested?

The interview process is deliberately non-promotional. A weak problem signal is evidence against the hypothesis, not a reason to broaden the product.

## Current Evidence

| Signal | Status |
|---|---|
| Technical reference lifecycle | Demonstrated |
| Public product definition | Documented |
| Customer discovery | In progress |
| Customer commitment | None yet |
| Paid pilot | None |
| Guarantee issued | None |
| Pricing validated | No |

## Decision Rule

No new guarantee category or major kernel abstraction should be added merely because it is technically possible.

A proposed addition should answer:

> **What real-world claim would this allow a customer to make more safely?**

If customer conversations do not support the claim, the correct response is to revise or narrow the hypothesis rather than add features.

## Commercial Acceptance

The target evidence for a pilot is:

`real problem → bounded obligation → agreed evidence → meaningful economic consequence → identifiable buyer → value recognized → price discussion → real pilot`

Until that chain is observed in the market, Commercial Guarantees remains in validation.
