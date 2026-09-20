---
title: "Commitment Teardown: Can a Go-Live Milestone Actually Be Proved?"
description: "A worked example showing how an ERP go-live commitment can fail to define completion evidence, verification, and the commercial consequence."
---

# Commitment Teardown: Can a Go-Live Milestone Actually Be Proved?

Here is a deliberately simple commitment:

> **“Production deployment will be completed by October 31.”**

At first glance, this looks objective.

It has a deliverable and a date.

But suppose the milestone also controls a payment.

The useful question changes:

> **What observable evidence would allow both sides to establish, without reconstructing the argument later, that the commitment was satisfied?**

## 1. Commitment

**What was promised?**

Production deployment by October 31.

That gives us a target event and a deadline.

It does not yet tell us everything required for the event to count as complete.

## 2. Completion condition

Possible interpretations include:

- the application was deployed
- users could log in
- critical integrations were operating
- mandatory acceptance tests passed
- production verification was completed
- the customer formally accepted the release

If these conditions were never distinguished, two reasonable people can reach different conclusions about the same milestone.

**The date is objective. The meaning of completion may not be.**

## 3. Evidence

Suppose the intended condition is:

> Production deployment is complete when the agreed production environment is deployed and all mandatory acceptance tests pass.

Now evidence can be named:

| Condition | Possible evidence |
|---|---|
| Production environment deployed | Deployment record |
| Mandatory tests pass | Test results |
| Production is operational | Production verification |
| Result occurred by deadline | Timestamped records |

The important shift is from **“we believe it was done”** to **“these observable records establish the required conditions.”**

## 4. Verification

Evidence alone does not necessarily settle the question.

Someone still needs to determine whether the evidence satisfies the commitment.

That could be:

- an agreed customer representative
- an independent verification process
- a predefined evidence rule
- another authority specified in the commercial agreement

The mechanism matters because otherwise the dispute can simply move from:

> “Was it complete?”

to:

> “Who gets to decide whether this evidence counts?”

## 5. Commercial consequence

Now consider the payment:

> **Milestone payment is due when the commitment is satisfied.**

If completion cannot be established, the commercial consequence is no longer just an operational disagreement.

Payment, rework, escalation, delay, or another contractual consequence may depend on the determination.

That makes the quality of the completion definition economically important.

## 6. Reconstruction test

The final test is simple:

> **Could someone who was not in the room later reconstruct why the milestone was treated as complete or incomplete?**

If the answer depends mainly on emails, meeting memories, conflicting interpretations, and a negotiation over what “complete” was supposed to mean, the commitment was not very easy to reconstruct.

That does not mean the project failed.

It means the **commercial commitment was difficult to establish objectively**.

## The pattern

A more bounded commitment can be represented as:

**Commitment → Completion condition → Evidence → Verification → Consequence → Reconstruction**

The point is not to add paperwork for its own sake.

The point is to make the factual basis of a consequential commercial decision clearer before the decision becomes disputed.

## Have a real one?

This example is intentionally simple.

If you have a real implementation milestone, go-live condition, acceptance clause, supplier commitment, or similar commercial obligation, you can submit a **redacted** version for a private manual audit.

[Bring a real commitment for a private audit](../../?submitted=0#request)

No confidential customer information is needed.

**Research status:** This is a demonstration of the method, not evidence of validated market demand or a live customer deployment.
