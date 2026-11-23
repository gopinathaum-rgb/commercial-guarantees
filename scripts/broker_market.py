#!/usr/bin/env python3
"""Evidence-gated matching and commission ledger for the private broker pilot."""
from __future__ import annotations
import argparse, json
from pathlib import Path

BUYER_REQUIRED = ("organisation", "need", "service_categories", "decision_owner", "authority_evidence", "current_need_evidence", "budget_status", "timeline", "contact_permission")
PROVIDER_REQUIRED = ("organisation", "service_categories", "capability_evidence", "references_checked", "availability", "contact_permission")
AGREEMENT_REQUIRED = ("provider_id", "commission_basis", "commission_value", "trigger", "attribution_window_days", "accepted_by_provider", "accepted_by_company", "buyer_disclosure_required")
DEAL_REQUIRED = ("buyer_id", "provider_id", "buyer_contracted", "provider_delivered", "trigger_evidence_id", "commission_agreement_id")

def load_jsonl(path):
    rows = []
    for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip(): continue
        try: row = json.loads(line)
        except json.JSONDecodeError as exc: raise ValueError(f"{path}:{n}: invalid JSON: {exc}") from exc
        if not isinstance(row, dict): raise ValueError(f"{path}:{n}: each record must be an object")
        rows.append(row)
    return rows

def missing(record, fields):
    return [f for f in fields if record.get(f) in (None, "", [], False)]

def buyer_status(b):
    absent = missing(b, BUYER_REQUIRED)
    return {"status": "unqualified" if absent else "qualified_for_matching", "missing": absent,
            "warning": "Field presence is not proof; human review must verify cited evidence."}

def provider_status(p):
    absent = missing(p, PROVIDER_REQUIRED)
    return {"status": "unverified" if absent else "eligible_for_matching_review", "missing": absent,
            "warning": "Capability claims and references require independent checking."}

def match(buyer, providers):
    bs = buyer_status(buyer)
    if bs["status"] != "qualified_for_matching":
        return {"buyer_id": buyer.get("id"), "status": "not_ready", "matches": [], "missing_buyer_fields": bs["missing"]}
    requested = {str(x).casefold() for x in buyer.get("service_categories", [])}
    ranked = []
    for p in providers:
        if provider_status(p)["status"] != "eligible_for_matching_review": continue
        overlap = sorted(requested & {str(x).casefold() for x in p.get("service_categories", [])})
        if overlap:
            ranked.append({"provider_id": p.get("id"), "provider": p.get("organisation"),
                           "matching_categories": overlap, "score": len(overlap),
                           "status": "human_verification_required"})
    ranked.sort(key=lambda x: (-x["score"], str(x["provider_id"])))
    return {"buyer_id": buyer.get("id"), "status": "candidate_matches_only", "matches": ranked,
            "disclaimer": "Category overlap is not proof of competence, fit, availability, buyer intent or willingness to pay."}

def agreement_status(a):
    absent = missing(a, AGREEMENT_REQUIRED)
    basis, value = a.get("commission_basis"), a.get("commission_value")
    if basis not in {"percentage", "fixed"}: absent.append("commission_basis (percentage or fixed)")
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
        absent.append("commission_value (positive number)")
    elif basis == "percentage" and value > 100: absent.append("commission_value (percentage cannot exceed 100)")
    return {"status": "ready_for_owner_review" if not absent else "not_executable", "missing": absent,
            "rule": "No attributable introduction until written terms, trigger, attribution window, disclosure and both acceptances are evidenced."}

def deal_status(d, agreements):
    absent = missing(d, DEAL_REQUIRED)
    a = next((x for x in agreements if x.get("id") == d.get("commission_agreement_id")), None)
    if a is None: absent.append("valid commission agreement")
    elif agreement_status(a)["status"] != "ready_for_owner_review": absent.append("executable commission agreement")
    if d.get("buyer_contracted") is not True: absent.append("buyer contract evidence")
    if d.get("provider_delivered") is not True: absent.append("delivery evidence")
    if not d.get("trigger_evidence_id"): absent.append("commission trigger evidence")
    return {"status": "potentially_earned_subject_to_accounting_review" if not absent else "not_earned",
            "missing": sorted(set(absent)), "note": "Not cash received; reconcile commission receipt separately."}

def cash_receipt_status(r):
    required = ("deal_id", "amount", "currency", "received_at", "bank_reference", "evidence_id")
    absent = missing(r, required)
    amount = r.get("amount")
    if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
        absent.append("amount (positive number)")
    return {"status": "cash_received_evidence_recorded" if not absent else "unverified_receipt",
            "missing": sorted(set(absent)), "note": "Reconcile against actual bank statement before reporting collected cash."}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("match")
    p.add_argument("--buyers", required=True); p.add_argument("--providers", required=True); p.add_argument("--buyer-id", required=True)
    p = sub.add_parser("audit")
    p.add_argument("--agreements", required=True); p.add_argument("--deals", required=True); p.add_argument("--receipts", required=True)
    args = parser.parse_args()
    if args.command == "match":
        buyer = next((b for b in load_jsonl(args.buyers) if b.get("id") == args.buyer_id), None)
        if buyer is None: raise SystemExit("Buyer not found: " + args.buyer_id)
        result = match(buyer, load_jsonl(args.providers))
    else:
        agreements, deals, receipts = load_jsonl(args.agreements), load_jsonl(args.deals), load_jsonl(args.receipts)
        result = {"agreements": [{"id": a.get("id"), **agreement_status(a)} for a in agreements],
                  "deals": [{"id": d.get("id"), **deal_status(d, agreements)} for d in deals],
                  "cash_receipts": [{"id": r.get("id"), **cash_receipt_status(r)} for r in receipts]}
    print(json.dumps(result, indent=2))

if __name__ == "__main__": main()
