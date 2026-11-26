import json
import unittest
from pathlib import Path
from forecast import bridge


class ForecastChecks(unittest.TestCase):
    def setUp(self):
        self.case = json.loads(Path(__file__).with_name("forecast.json").read_text(encoding="utf-8"))

    def test_allowance_replaced(self):
        self.assertEqual(bridge(self.case), (6600, 5500, 52600, 7400))

    def test_later_accrual_moves_remaining_cost_only(self):
        self.case["ledger"].append({"ref":"AC-32","amount":1100})
        self.assertEqual(bridge(self.case), (6600, 4400, 52600, 7400))

    def test_duplicate_accrual_requires_review(self):
        self.case["ledger"] *= 2
        with self.assertRaises(ValueError):
            bridge(self.case)
