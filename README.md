# Commercial Guarantees

![Commercial Guarantees](images/logo.svg)

> **Bounded commercial certainty for commitments that can be defined, evidenced, and independently reconstructed.**

## Start Here

| Commercial question | Reference |
|---|---|
| What problem are we solving? | [Problem](docs/PROBLEM.md) |
| How does the lifecycle work? | [How It Works](docs/HOW_IT_WORKS.md) |
| What are we validating now? | [Commercial Validation](docs/VALIDATION.md) |
| What does the current reference case look like? | [Enterprise Software Implementation](examples/enterprise-software-implementation.md) |
| What is technically defined? | [Architecture](docs/ARCHITECTURE.md) |
| What is the current status? | [Validation Status](docs/status/VALIDATION_STATUS.md) |
| How could a pilot work? | [Pilot Program](pilots/README.md) |
| Common questions | [FAQ](docs/FAQ.md) |

---

## The Current Wedge

The first commercial research case is **enterprise software production deployment**.

A customer hires an implementation vendor to deploy agreed software configuration into production.

The commitment is deliberately narrow:

> **Production deployment completed by a fixed deadline, with all mandatory acceptance tests passing and the agreed evidence available.**

The guarantee does **not** cover the entire project or promise that the software will create a particular business outcome.

See the complete [enterprise software implementation reference case](examples/enterprise-software-implementation.md).

---

## Why Commercial Guarantees?

Commercial transactions often contain commitments whose failure has economic consequences, while completion can be difficult to establish consistently.

A Commercial Guarantee makes one bounded commitment explicit:

`What is promised → What counts as completion → What evidence proves it → What happens if it cannot be demonstrated`

The lifecycle is:

`Obligation → Assessment → Commitment → Guarantee → Evidence → Trigger → Claim → Settlement → Verification`

The objective is not to replace commercial judgment. It is to make a defined commitment easier to evaluate, reconstruct, and act on.

---

## Reference Example

**Enterprise software implementation**

- Milestone: production deployment completed
- Deadline: 31 October 2026, 18:00 UTC
- Maximum guarantee response: ₹1,00,000
- Acceptance: all mandatory tests pass
- Evidence: deployment record + production verification + test results
- Trigger: milestone cannot be demonstrated against agreed conditions
- Settlement: bounded and separately recorded
- Verification: lifecycle can be reconstructed from recorded facts

This is a **reference product definition**, not a live customer guarantee.

---

## What Makes the Boundary Important?

A guarantee should not quietly become a promise about everything.

The reference case therefore excludes:

- complete project success
- subjective customer satisfaction
- every defect after go-live
- business outcomes after deployment
- unlimited delay damages
- evidence that cannot be reconstructed

A narrower commitment is easier to specify, evidence, monitor, and settle.

---

## Products

The repository contains broader product concepts for:

- Software Delivery Guarantee
- Milestone Completion Guarantee
- Advance Payment Guarantee

These are product definitions under validation, not claims of existing market adoption.

See:

- [Software Delivery Guarantee](products/software-delivery-guarantee.md)
- [Milestone Completion Guarantee](products/milestone-completion-guarantee.md)
- [Advance Payment Guarantee](products/advance-payment-guarantee.md)

---

## Commercial Validation

**Technical rigor is not commercial validation.**

The reference lifecycle has been exercised in the private implementation repository. The current public work is testing whether the underlying commercial problem is real, economically meaningful, and suitable for a pilot.

Current research sequence:

`Problem → Frequency → Commercial consequence → Evidence → Buyer → Value → Price → Pilot`

Open questions include:

- Is delayed or disputed go-live completion a recurring problem?
- Who bears the economic consequence?
- How is completion evidenced today?
- Can the evidence be independently reconstructed?
- Would a bounded guarantee change a real transaction?
- Who would pay for it?
- What fee and settlement mechanism would be acceptable?
- Can a named real deployment serve as a pilot?

See [Commercial Validation](docs/VALIDATION.md) for the current evidence boundary.

---

## What We Do Not Claim Yet

- No commercial guarantees have been issued.
- No paid pilot has been secured.
- Pricing has not been validated.
- Product-market fit has not been established.
- The reference case is not evidence that customers will adopt the mechanism.

The project is intentionally explicit about these limits.

---

## Repository Structure

```text
docs/
  PROBLEM.md
  HOW_IT_WORKS.md
  ARCHITECTURE.md
  VALIDATION.md
  status/VALIDATION_STATUS.md
products/
examples/
pilots/
images/
```

The public repository documents the commercial model, product boundaries, examples, and validation status.

Implementation continues in a separate engineering repository.

---

## Guiding Principle

> **Build evidence before expansion.**

No new guarantee category or major technical abstraction should be added merely because it is possible.

The useful question is:

> **What real-world claim would this allow a customer to make more safely?**

---

## License

MIT
