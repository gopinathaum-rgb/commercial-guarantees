# AI-operated commercial brokerage — pilot

## Model
A private, evidence-led brokerage connects organisations with service providers. Initial vertical: ERP implementation, migration, remediation, integration and acceptance-related services in India.

The company earns a disclosed referral/brokerage fee only under written terms accepted by the provider and the company. The buyer pays the provider directly; the company does not hold either party's funds. No rate is presumed: price and commission terms remain owner decisions.

## Transaction lifecycle
Demand signal → qualified buyer requirement → provider candidate → provider screening → match recommendation → consented introduction → written commission terms → buyer/provider contract → delivery and trigger evidence → commission invoice/receivable → reconciled cash receipt.

## Evidence gates
- A public issue is a demand signal, not a buyer.
- A provider website is a capability claim, not verification.
- Category overlap is a shortlist, not proof of fit.
- A conversation is not an accepted introduction.
- An introduction is not a contract.
- A contract is not delivery.
- A commission due is not cash received.

## First runnable slice
scripts/broker_market.py supports JSONL records, explicit buyer/provider field checks, category-overlap matching, commission agreement validation, deal-stage audit and separate cash-receipt evidence checks.

Run:
python scripts/broker_market.py match --buyers private/buyers.jsonl --providers private/providers.jsonl --buyer-id BUYER_ID
python scripts/broker_market.py audit --agreements private/agreements.jsonl --deals private/deals.jsonl --receipts private/receipts.jsonl

Keep real prospect identities, contact details, budgets, contracts, bank references and confidential evidence in a private access-controlled store. Never commit them to this public repository.

## Authority boundary
Automation may discover, normalize, flag missing evidence, rank category overlap and prepare private research. It must not autonomously contact prospects through new channels, publish promotional comments, disclose personal/confidential data, represent providers as verified without checks, negotiate or bind commercial terms, accept contracts, invoice, or move funds.

The owner approves commission terms and consequential introductions. Disclose provider-paid compensation to buyers where required and before they rely on a recommendation.

## Pilot success
Track separately: qualified buyer requirements; screened providers; consented introductions; contracts; completed provider delivery; commission due; commission cash received and reconciled. First success is one completed buyer-provider transaction and one reconciled brokerage receipt. Leads, matches, messages and introductions are not revenue.

## Limitations
This deterministic pilot is not an autonomous marketplace, legal/compliance determination, provider certification or proof of demand. Before scaling, obtain jurisdiction-specific advice on referral contracts, tax, privacy, disclosure and any sector-specific licensing.
