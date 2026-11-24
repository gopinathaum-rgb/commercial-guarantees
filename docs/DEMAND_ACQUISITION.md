# Demand acquisition: procurement signals and market intervention

## Decision

Public developer discussions are retained as ecosystem/problem research only. They are not the primary demand channel and must never be counted as buyers, buying intent or commercial leads.

The acquisition engine now prioritises formal ERP implementation and transformation procurement notices published on official buyer pages. A formal notice is stronger evidence that an organisation has an active procurement process, but it is still **not a qualified buyer for our brokerage**.

## Current automated source allowlist

- FSID / IISc official tenders page: https://www.fsid-iisc.in/tenders/
- MOIL official tender archive: https://www.moil.nic.in/tender-archive?nop=109

The current source set is deliberately narrow. CPPP/eProcure advanced search presents a CAPTCHA gate; the automation must not bypass it. Add new official sources only after verifying their ownership, terms, stable page structure and current tender coverage.

## What the new collector does

`scripts/procurement_signal_discovery.py`:
- Fetches only explicitly allowlisted official buyer pages.
- Extracts ERP/SAP/implementation/migration notices from same-domain links.
- Deduplicates notices in the internal GitHub queue.
- Labels each as `formal_procurement_signal_unqualified`.
- Preserves source page and notice links.
- Records deadline and intermediary eligibility as manual checks.
- Does not contact buyers, providers or tender authorities; does not submit bids or make introductions.

## Intervention workflow

For every candidate:
1. Open the official notice and all corrigenda. Verify whether the process is current and the deadline has not passed.
2. Extract organisation, scope, procurement reference, geography, eligibility, value (if disclosed), contract model, delivery milestones and acceptance/payment terms.
3. Review the tender and procurement rules for restrictions on intermediaries, referral fees, conflicts, bidder communications and disclosure.
4. If buyer-side paid brokerage is not permitted or is not commercially credible, do not pitch the buyer as a broker. Consider provider-side teaming only if a provider independently consents and accepts written terms.
5. Independently verify provider capability, relevant recent references, delivery team and current capacity.
6. Prepare a specific, evidence-backed intervention and route it for owner approval where it creates an introduction or commercial commitment.
7. Keep every stage separate: signal → verified current procurement → permissible route → qualified counterparty → accepted terms → consented introduction → transaction → commission trigger → reconciled cash.

## Hard evidence boundaries

- A tender is not a qualified buyer.
- An expired or cancelled notice is not current demand.
- A procurement organisation may be prohibited from paying a referral commission.
- A provider directory listing is not provider verification.
- Category overlap is not provider fit.
- A public signal is not permission to contact or introduce.
- A provider's customer payment is not our commission cash until terms, trigger and bank receipt are evidenced and reconciled.

## Operating priority

The target is not a larger queue. It is one permissible, qualified, consented buyer-provider transaction with written commission terms and a reconciled commission receipt. The owner has approved the disclosed success-fee principle only; no default rate or deal-specific terms are approved.
