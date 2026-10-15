# NTRO Evidence Audit 001: When Implementation, Testing, Acceptance, and Payment Diverge

**Status:** Research reconstruction based primarily on judicial records  
**Case:** *Corporate Infotech Private Limited v. National Technical Research Organisation*  
**Proceedings:** OMP (ENF.) (COMM.) 174/2024 and related proceedings  
**Purpose:** Examine what the available record establishes about a consequential implementation commitment—and what it does not establish.

> **Research boundary:** This is a reconstruction of the record described in court materials, not an independent audit of all original project records. We have not independently inspected the full original contract, every cited letter, the complete acceptance-test procedure (ATP), the underlying test-level reports, or all relevant annexures. Conclusions below are limited accordingly.

## Why examine this case?

Enterprise implementation disputes can involve several states that are easy to conflate: equipment delivered, sites ready, configurations completed, tests conducted, tests demonstrated, formal acceptance, contractual entitlement, enforceability, and actual payment. Those states may be related, but one does not automatically prove another.

This audit asks a narrow question:

**What can the available evidence support about the state of the commitment at each point in the record, and where does uncertainty remain material to a consequential decision?**

It does not assume that a later dispute proves an earlier warning was actionable, or that a better reconstruction would necessarily have changed the outcome.

## 1. The commitment and the dispute

The court materials describe a contract dated 10 August 2018 for a secure network across 23 locations. The judgment describes a 28-week contract timeline and identifies 20 February 2019 as the deadline in one passage. Another reproduced passage refers to 8 February before also referring to 20 February. Without inspecting the original contract and relevant amendments, this discrepancy should remain open rather than be silently resolved.

The judgment describes delays and dependencies involving site access, infrastructure, cabling, connectivity, configuration, and acceptance testing. It records that both parties contributed to delays. The dispute later involved outstanding acceptance tests, liquidated damages, a performance bank guarantee, and a balance payment.

These are not one single state. Evidence that a site was connected does not by itself prove that every required test passed. A test demonstration does not necessarily prove formal contractual acceptance. A tribunal's determination of contractual consequences does not, by itself, establish when each party could reasonably have recognized a problem or what intervention was feasible at the time.

**Sources:** [Delhi High Court judgment dated 1 April 2026 (official PDF)](https://delhihighcourt.nic.in/app/showFileJudgment/68001042026OMPCOMM3782024_142221.pdf) · [Judgment transcription](https://indiankanoon.org/doc/10455915/)

## 2. What the available record describes about testing

The judgment describes the acceptance-test procedure being requested, submitted, amended, and ultimately approved in late 2019 and early 2020. It also describes a sequence of operational readiness and testing events.

The judgment's account of the initial OSAT phase reports:
- 966 parametric tests in the reported set;
- 194 of those parametric tests marked as failed;
- 19 functional tests and 303 parametric tests described as “not conducted.”

A later passage discussing the report dated 28 May 2020 identifies 772 passed and 194 failed tests, again totaling 966, and says details of a balance of 284 tests were not set out. The judgment also describes later testing phases and a total of 1,269 tests across six phases between February 2020 and June 2022.

The numbers invite reconciliation, but arithmetic alone cannot establish that the categories share the same population or definitions. For example, 1,269 minus 966 equals 303, and 284 plus 19 also equals 303. That numerical alignment is a lead for investigation—not proof that the figures refer to the same tests. The record needs to be reconciled at the level of test identifiers, categories, sites, phases, and status definitions.

The judgment also describes later correspondence in which the number of failed tests was reported as 18, all tests were said to have been demonstrated to S-NOC, and OSAT Committee verification was still described as in progress. Those statements may reflect different scopes, stages, or authorities. Without the original letters, test register, and committee records, they should not be labelled a definitive contradiction.

### What this establishes—and what it does not

The judgment supports the conclusion that testing, test-status reporting, demonstration, and verification formed a material part of the dispute. It also describes gaps in the records available to the tribunal.

It does **not** give us a complete, independently verified test ledger. We cannot responsibly conclude from these summaries alone exactly which individual tests remained outstanding at every date, why each test was not conducted or failed, or whether every reported count used the same denominator.

## 3. A consequential change in control and verification

The judgment says that on 17 March 2020 NTRO took over system credentials and directed the contractor's personnel to keep away from the systems except for operational support. The tribunal reasoned that this arrangement, together with NTRO's control over sites and test documentation, made it difficult or impossible for the contractor to demonstrate or re-demonstrate pending tests objectively. The tribunal treated the remaining OSAT as complete for contractual purposes from that date.

That is an important retrospective tribunal conclusion about contractual consequences. It is not proof that all technical tests passed on 17 March 2020, nor does it establish exactly what each party knew on that date or which alternatives were practically available.

A contemporaneous reconstruction would need the original handover and access correspondence, the relevant contract provisions, the outstanding test inventory, the parties' rights and responsibilities after the change in control, and evidence of what further testing or independent verification could feasibly have occurred.

## 4. Economic state: entitlement is not realization

The materials describe a restructuring of the remaining 30% payment in May 2020: 20% linked to deployment/service at a minimum number of locations and 10% linked to successful completion/certification. The judgment describes the 20% as released and the 10% as disputed. The original amendment and payment records have not been independently inspected for this audit.

The contractor pursued the disputed balance and related relief through arbitration and subsequent court proceedings. The award was challenged under Section 34; on 1 April 2026 the Delhi High Court declined to interfere with the award under the applicable limited review. An enforcement proceeding was also documented in a court order dated 6 July 2026.

A cause-list entry dated 8 April 2026 appears inconsistent with the later order's reference to the same enforcement application. That discrepancy does not establish payment or release. We have not verified a later order or primary payment record that establishes actual realization.

For that reason, the economic-state sequence must keep separate:

**Contractual obligation → disputed performance/acceptance → payment dispute → arbitral determination → judicial challenge → enforcement process → verified release/payment.**

The available materials establish several of these stages, but **actual realization remains unverified for this audit**. A disputed balance or award amount is not automatically a loss avoided, savings achieved, or economic value created by Recon.

**Additional source:** [Delhi High Court enforcement order dated 6 July 2026 (transcription)](https://indiankanoon.org/doc/24499428/)

## 5. Could an earlier reconstruction have changed the situation?

This audit identifies plausible questions to investigate at several points: when the ATP was being developed; when readiness was reported for particular sites; after the initial OSAT results; when control and access changed; and when later reports described different test statuses.

Those are candidate investigation points, not proven early-warning opportunities.

To establish that an earlier intervention was genuinely available, we would need contemporaneous evidence showing:
1. what the relevant actor knew at that time;
2. which requirement or state gap was then defensible from available evidence;
3. who had authority to make the relevant decision;
4. what feasible action was available, within what time and at what cost;
5. whether that action could reasonably have changed a later decision or outcome.

The court's later findings cannot be used to manufacture knowledge that was unavailable to the parties at the time. This record also does not establish that a reconstruction method would have prevented the dispute, shortened it, changed the award, or accelerated payment.

## 6. What remains unresolved

The most material missing records for a stronger reconstruction are:
- the original contract, amendments, and complete acceptance criteria;
- the full ATP and versioned comment/approval history;
- the complete test inventory with stable test IDs, site, category, phase, execution date, and status;
- the original report dated 28 May 2020 and its annexures;
- the original letters describing later failed-test counts and S-NOC demonstrations;
- the relevant OSAT Committee records and the scope of its authority;
- the original credential/access handover correspondence and records of what testing remained feasible afterward;
- later enforcement and payment records sufficient to verify realization.

If these records cannot be obtained, that is a limit on what can be concluded—not permission to fill the gaps by inference.

## 7. What this case does—and does not—show about Recon

This case illustrates why a commercial commitment should not be compressed into a single “complete/not complete” label. Testing, demonstration, verification, contractual acceptance, entitlement, enforceability, and realization are distinct states. A useful reconstruction should preserve their provenance and chronology, make contradictions visible, and identify the evidence still needed for a defensible decision.

This is a **method illustration**, not proof of product effectiveness.

We have not demonstrated that Recon identified an actionable opportunity before the parties did, changed a consequential decision, caused an improved outcome, generated measurable economic benefit, or supports a repeatable paid service. Those questions require independent reconstruction and, especially, real current cases with open decisions.

## Bring a real, current case

Have you handled an implementation or other consequential commitment where the reported status, available evidence, actual operational state, and commercial milestone did not line up?

We are looking for one real situation where:
- completion, acceptance, readiness, or payment remains unresolved;
- relevant evidence is fragmented, contradictory, or difficult to reconcile;
- a consequential decision is still open; and
- a practitioner can discuss the situation without disclosing confidential customer information.

We are conducting a limited, manual research audit. The first step is a short private description of the commitment, the required outcome, the current unresolved question, and the decision that depends on it. We will agree scope and any fee before reviewing substantive evidence. Please do not send confidential contracts, credentials, personal data, or sensitive operational records through a public discussion or an unverified form.

Start with the [Can You Prove It? private commitment-audit method](can-you-prove-it.md), or contact us through the repository's private audit route. We will first assess whether the case is suitable; submitting a description does not guarantee acceptance into the research.

**The question we want to test is simple: can an independent reconstruction establish what is happening, what the evidence supports, what remains unresolved, and whether that changes a consequential decision?**

---

*Research note: This document summarizes and interprets publicly available court materials. It is not legal advice, does not determine the parties' present legal position, and should not be read as an allegation of misconduct by either party. Corrections supported by source records are welcome. Please do not post confidential material publicly.*
