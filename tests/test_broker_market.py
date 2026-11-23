import unittest
from scripts.broker_market import buyer_status, match, agreement_status, deal_status, cash_receipt_status

class BrokerMarketTests(unittest.TestCase):
    def setUp(self):
        self.buyer = {"id":"b1","organisation":"Buyer","need":"ERP migration","service_categories":["ERP migration"],
          "decision_owner":"Owner","authority_evidence":"ev1","current_need_evidence":"ev2","budget_status":"unknown",
          "timeline":"Q1","contact_permission":"yes"}
        self.provider = {"id":"p1","organisation":"Provider","service_categories":["ERP migration"],
          "capability_evidence":"ev3","references_checked":["ref1"],"availability":"confirmed","contact_permission":"yes"}
        self.agreement = {"id":"a1","provider_id":"p1","commission_basis":"fixed","commission_value":1000,
          "trigger":"provider receives payment","attribution_window_days":60,"accepted_by_provider":True,
          "accepted_by_company":True,"buyer_disclosure_required":True}

    def test_buyer_requires_authority_and_permission(self):
        result = buyer_status({"organisation":"Buyer","need":"ERP"})
        self.assertEqual(result["status"], "unqualified")
        self.assertIn("authority_evidence", result["missing"])
        self.assertIn("contact_permission", result["missing"])

    def test_match_only_returns_evidenced_category_overlap_candidates(self):
        weak = {"id":"p0","organisation":"Weak","service_categories":["ERP migration"]}
        result = match(self.buyer, [weak, self.provider])
        self.assertEqual([x["provider_id"] for x in result["matches"]], ["p1"])
        self.assertEqual(result["matches"][0]["status"], "human_verification_required")

    def test_no_overlap(self):
        p = dict(self.provider, service_categories=["web design"])
        self.assertEqual(match(self.buyer, [p])["matches"], [])

    def test_agreement_requires_both_acceptances(self):
        a = dict(self.agreement, accepted_by_company=False)
        self.assertNotEqual(agreement_status(a)["status"], "ready_for_owner_review")

    def test_deal_not_earned_without_contract_delivery_and_trigger(self):
        d = {"buyer_id":"b1","provider_id":"p1","buyer_contracted":False,"provider_delivered":False,
             "trigger_evidence_id":"","commission_agreement_id":"a1"}
        self.assertEqual(deal_status(d, [self.agreement])["status"], "not_earned")

    def test_receipt_requires_bank_and_evidence_reference(self):
        r = {"deal_id":"d1","amount":500,"currency":"INR","received_at":"2026-11-23"}
        self.assertEqual(cash_receipt_status(r)["status"], "unverified_receipt")
        self.assertIn("bank_reference", cash_receipt_status(r)["missing"])

if __name__ == "__main__": unittest.main()
