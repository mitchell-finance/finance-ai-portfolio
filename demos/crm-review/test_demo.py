import json
import unittest
from pathlib import Path
from review import review


class CRMChecks(unittest.TestCase):
    def setUp(self):
        self.case = json.loads(Path(__file__).with_name("meeting.json").read_text(encoding="utf-8"))

    def test_conditional_order_stays_open_and_task_survives(self):
        result = review(self.case)
        self.assertEqual(result["stage"], "Proposal sent")
        self.assertIn("Hold", result["decision"])
        self.assertEqual(result["suggested_task"][:2], ("Account manager","Send the board pack on Friday."))

    def test_only_verified_matching_order_supports_review(self):
        for opportunity, verified, allowed in [("OTHER",True,False), ("OP-17",False,False), ("OP-17",True,True)]:
            self.case["order_register"] = [{"opportunity":opportunity,"verified":verified,"reference":"P-5"}]
            self.assertEqual(review(self.case)["decision"].startswith("Review"), allowed)

    def test_wrong_task_owner_blocks_update(self):
        self.case["candidate"]["owner"] = "Buyer"
        with self.assertRaises(ValueError):
            review(self.case)
