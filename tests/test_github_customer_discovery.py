import os
import unittest
os.environ.setdefault("GITHUB_TOKEN", "test-token")
from scripts.github_customer_discovery import analyse_text, redact

class DiscoveryAnalysisTests(unittest.TestCase):
    def test_decision_language_is_priority_not_buyer(self):
        result = analyse_text("ERP implementation acceptance",
            "Customer needs go-live acceptance and milestone payment sign-off.",
            [{"body": "The vendor says deployment is complete but acceptance is pending."}])
        self.assertEqual(result["classification"], "decision_evidence_review")
        self.assertIn("milestone payment", result["decision_signals"])
        self.assertNotIn("buyer", result)

    def test_lifecycle_context_is_not_qualified(self):
        result = analyse_text("Migration deployment blocked",
            "Implementation is delayed during rollout.", [])
        self.assertEqual(result["classification"], "implementation_lifecycle_context")
        self.assertEqual(result["decision_signals"], [])

    def test_technical_only_is_insufficient(self):
        result = analyse_text("Database exception", "Stack trace and null pointer.", [])
        self.assertEqual(result["classification"], "insufficient_lifecycle_evidence")

    def test_redacts_email_and_secret(self):
        text = redact("Contact jane@example.com token=abc123 for details")
        self.assertNotIn("jane@example.com", text)
        self.assertNotIn("abc123", text)

if __name__ == "__main__":
    unittest.main()
