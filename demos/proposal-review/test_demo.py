import json
import unittest
from pathlib import Path
from review import review


class ProposalChecks(unittest.TestCase):
    def setUp(self):
        self.case = json.loads(Path(__file__).with_name("quote.json").read_text(encoding="utf-8"))

    def test_price_agrees_but_two_commitments_need_review(self):
        issues, freight, profit = review(self.case)
        self.assertEqual(len(issues), 2)
        self.assertEqual((freight, profit), (700, 11300))

    def test_aligning_delivery_terms_clears_only_those_exceptions(self):
        self.case["draft"].update(promised_first_batch=4, deliveries=1, price=49000)
        issues, freight, _ = review(self.case)
        self.assertEqual(len(issues), 1)
        self.assertIn("price", issues[0])
        self.assertEqual(freight, 0)
