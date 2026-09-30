# Commercial Clock Evidence — ASCON-IV / Ishan Infotech × ITI

**Observed:** 2026-09-30 research pass  
**Primary source:** Bengaluru Commercial Court judgment, *M/s Ishan Infotech Limited v. M/s ITI Limited*, 20 July 2026.

## Why this case matters

This is a real implementation/project-management transaction in which the economic state of a milestone became disputed around **Proof of Concept (PoC)** recognition.

The Purchase Order appointed Ishan Infotech as Project Management Agency for ASCON-IV. The Purchase Order value was ₹70,00,09,372. Its payment schedule linked later payment tranches to successful PoC.

The court record states that PoC for the relevant OFC and Microwave sub-systems was completed, while payment remained disputed. Ishan had stated in February 2022 that almost one year had elapsed from the expected PoC date without payment. ITI later proposed an ad hoc ₹3 crore payment while asking Ishan to continue services.

The court ultimately found that issuance of PoC for all sub-systems was not a prerequisite for release of payment and held that ₹14,44,25,839 was payable for the OFC and Microwave work, with 15% interest from the due date.

## Economic-state reconstruction

`PERFORM → PRODUCE/TEST EVIDENCE → PoC RECOGNITION → ENTITLEMENT → PAYMENT`

Observed blockage:

`PERFORMED SUB-SYSTEM WORK → PoC/recognition boundary disputed or delayed → PAYMENT HELD → WORKING-CAPITAL PRESSURE → AD HOC PAYMENT DISCUSSION → SERVICE SUSPENSION → COMMERCIAL SUIT`

## Evidence

- Purchase Order: ₹70,00,09,372 total consideration.
- Initial 7.5% payment: ₹5.25 crore paid in January 2021.
- Later payment stages were tied to PoC.
- February 2022 communication recorded nearly one year of delay from expected PoC with no payment released.
- ITI proposed an ad hoc ₹3 crore payment while acknowledging financial constraints.
- Court found PoC had been completed for the relevant OFC and Microwave sub-systems.
- Court found all-sub-system PoC was not a prerequisite for release of payment.
- Amount found due for completed OFC/Microwave work: ₹14,44,25,839.
- Final order: ₹14,44,25,839 plus 15% interest from the date due, payable within three months of judgment.

## What is proven

1. A consequential implementation transaction can contain a recognition boundary that directly controls cash movement.
2. The disputed boundary can persist long enough to create material financing/continuity pressure.
3. Existing project-management services may be involved in coordinating the transition.
4. The eventual resolution mechanism can be legal adjudication.

## What is NOT proven

This case does **not** prove that AUM is the right product, that the parties wanted a new coordination product, or that a pre-dispute recognition service would have been purchased.

It also does not establish that one side was solely responsible for the delay in every respect; the court's findings are specific to the pleaded and evidenced transaction.

## Next investigation

Do not build new AUM primitives from this case.

Find 2–3 independent transactions and test whether the same economic transition recurs:

1. Who performs?
2. What evidence establishes completion?
3. Who has authority to recognize it?
4. What exactly changes economically after recognition?
5. How long does the transition take?
6. What amount is trapped or exposed while it waits?
7. Who currently coordinates or resolves the transition?
8. Is that mechanism already paid for?
9. Does the same mechanism recur across unrelated buyers/vendors?

## Current conclusion

**The commercial clock is real. The paid mechanism for moving it is not yet proven.**

That is the next evidence boundary.