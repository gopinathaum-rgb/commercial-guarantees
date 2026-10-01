# Three-Case Transaction Comparison — Recognition Boundary

Date: 2026-10-01

## Purpose

Compare three documented consequential commercial situations using the same existing investigation structure, without introducing a new data model:

participants → commitment → completion condition → evidence → recognition authority → economic state → uncertainty → consequence → existing resolution mechanism → cost of delay/failure

## Case 1 — WAPCOS × CYFUTURE

### Reconstruction
- Participants: WAPCOS and CYFUTURE in an ERP implementation relationship.
- Commitment: ERP implementation/services and, after termination, restoration and handover of relevant services, data and materials.
- Completion condition: disputed implementation/performance obligations; after termination, practical handover/access had to be sufficient for WAPCOS to continue services.
- Evidence: contract/RFP provisions, services, data, backups, source material, passwords/passcodes, technical access, correspondence and court directions.
- Recognition authority: ultimately disputed between the parties; court did not decide merits and referred disputes to arbitration.
- Economic state: terminated/contested relationship requiring continuity, restoration and handover rather than a cleanly recognized completed state.
- Uncertainty: whether required materials/data had actually been handed over in usable form; whether contractual breaches existed; whether the services had been restored without remaining glitches.
- Consequence: service continuity, access to data, handover, termination consequences, possible payment/claim issues and arbitration.
- Existing resolution mechanism: DRC/arbitration plus interim court directions.
- Cost of delay/failure: operational interruption and inability to access data/services; exact monetary loss was not determined in the interim orders.

Evidence: Delhi High Court recorded disputes over restoration, passwords/passcodes, data and access, and expressly left merits open while referring the parties to arbitration.

## Case 2 — NTRO × Corporate Infotech

### Reconstruction
- Participants: NTRO and Corporate Infotech.
- Commitment: supply, installation and integration of secure network infrastructure across 23 locations, with testing, training and support.
- Completion condition: successful Acceptance Testing / OSAT, linked to commissioning and commencement of warranty; contractual payment and PBG consequences followed.
- Evidence: ATPs, OSAT phases, site availability, operationalisation, login credentials, correspondence, test records and contractual provisions.
- Recognition authority: contractual buyer-side acceptance process, but the eventual recognition boundary became contested and required arbitral/judicial determination.
- Economic state: 70% paid, then 20% paid; 10% remained withheld while testing, delay, LD, warranty commencement and PBG status were disputed.
- Uncertainty: progress of testing, attribution of delay, operational readiness, whether OSAT was completed, and whether the PBG/LD consequences remained active.
- Consequence: withheld 10% balance, PBG retention/release, warranty commencement and LD exposure.
- Existing resolution mechanism: contractual testing/acceptance process, arbitration, Section 34 court review.
- Cost of delay/failure: approximately 10% of contract value remained economically trapped; the 2026 judgment records the tribunal's award of Rs. 7,14,61,511 as balance consideration due as of 17 March 2020.

Key determination: the tribunal deemed OSAT completed on 17 March 2020 after the buyer took control of systems/sites and excluded the supplier from access; the High Court upheld the factual/contractual reasoning and treated the resulting payment/PBG/warranty consequences as flowing from that determination.

## Case 3 — Sage Technologies × Shree Baidyanath

### Reconstruction
- Participants: Sage Technologies and Shree Baidyanath Ayurved.
- Commitment: SAP S/4HANA implementation under a Rs. 62.5 lakh purchase order.
- Completion condition: explicit milestone success factors — project start-up, blueprint sign-off, UAT sign-off, successful Go-Live, successful quarter-end and year-end.
- Evidence: purchase order, milestone invoices, UAT/sign-off material, issue lists, emails/correspondence, implementation records and operational evidence.
- Recognition authority: client-side recognition/sign-off was embedded in the milestone structure; whether UAT and successful Go-Live had occurred was contested.
- Economic state: first 65% was paid through UAT according to the judgment record; later milestone payments were disputed.
- Uncertainty: unresolved implementation issues, whether UAT was actually signed off, whether Go-Live satisfied the contractual “successful Go-Live” condition, and whether additional work was contractually authorized.
- Consequence: invoices for milestones 4–6 were disputed; the court held the plaintiff was not entitled to those payments.
- Existing resolution mechanism: contractual milestone/sign-off process followed by commercial litigation.
- Cost of delay/failure: the court found the defendant suffered business losses and operational hardship from incomplete implementation; exact damages were not awarded to Syzygy and should not be generalized beyond this case.

## Cross-case comparison

### What repeats

1. A commercial consequence is attached to a state transition.
   - WAPCOS: service continuity/handover after termination.
   - NTRO: commissioning → warranty/payment/PBG consequences.
   - Sage: UAT/Go-Live → milestone payment.

2. The dispute is not simply “did work happen?”
   The harder question is whether the available evidence establishes the contractual state that unlocks the next consequence.

3. Evidence is distributed across multiple records and events.
   Contracts alone are insufficient; correspondence, testing, access/control state, sign-offs, operational use and contemporaneous records matter.

4. Recognition is consequential.
   The disputed recognition point changes money, security, warranty, service continuity or litigation posture.

5. Existing resolution mechanisms are reactive.
   The cases ultimately rely on client sign-off, DRC, arbitration, court proceedings or contractual testing procedures. They do not establish that a neutral reconstruction service existed before the dispute.

### What does NOT repeat cleanly

- The failure mode differs: termination/handover, acceptance-testing/payment/security, and incomplete implementation/UAT/Go-Live.
- The recognition authority differs by contract and situation.
- The economic consequence differs.
- The evidence required differs materially by transaction.
- These cases do not prove customers would pay Syzygy for pre-dispute reconstruction.

## Current hypothesis

The strongest repeated mechanism is not:

“companies lack evidence.”

It is:

“commercial evidence exists across a chain of records, but a consequential economic state still depends on whether the relevant condition is recognized by the party/authority whose recognition activates the next contractual consequence.”

This remains a research hypothesis, not a product-validation conclusion.

## Recon implication

No new schema or ontology is justified by these three cases.

Keep the existing classes and use the repeated comparison as an observation/comparison layer:

evidence → condition → recognition → economic state → consequence

The next empirical question is:

**Before a dispute becomes formal, where does the recognition chain become uncertain enough to delay payment, acceptance, handover, warranty commencement, release of security, or another economic transition?**

That question should now be tested against a live commercial situation, preferably a customer-supplied one.

## Decision

Do not expand Recon v0.2 yet.
Do not declare AUM validated.
Do not claim the Commercial Commitment Audit is validated.

The three cases justify continuing transaction-led investigation and moving toward a real customer case.
