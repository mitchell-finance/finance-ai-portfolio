import unittest
from datetime import datetime

from unapplied import DataError, HERE, load_snapshot, position


class UnappliedReceiptTests(unittest.TestCase):
    def setUp(self):
        self.case = load_snapshot(HERE / "data" / "unapplied-receipt.json")
        self.advice = self.case["advice"]

    def review(self, advice):
        ledger = self.case["snapshot"]
        return position(ledger, self.case["receipt"], advice, datetime.fromisoformat(ledger["checked_at"]))

    def test_unapplied_receipt_blocks_specific_chaser(self):
        self.assertEqual(self.review([]), (480000, 240000, 240000, None))

    def test_repeated_advice_applies_cash_once(self):
        result = self.review([self.advice])
        self.assertEqual(result[:3], (240000, 0, 240000))
        self.assertIn("INV-B", result[3])
        self.assertNotIn("INV-A", result[3])
        self.assertEqual(self.review([self.advice, self.advice]), result)

    def test_invoice_order_does_not_choose_the_target(self):
        before, after = self.review([]), self.review([self.advice])
        self.case["snapshot"]["invoices"].reverse()
        self.assertEqual(self.review([]), before)
        self.assertEqual(self.review([self.advice]), after)

    def test_conflicting_advice_requires_review(self):
        with self.assertRaisesRegex(DataError, "Conflicting"):
            self.review([self.advice, dict(self.advice, invoice="INV-B")])
