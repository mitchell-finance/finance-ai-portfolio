import unittest
from receipt_review import review


class ReceiptChecks(unittest.TestCase):
    def test_late_receipt_correction_changes_match(self):
        self.assertEqual(review(3,3,60,[(1,48)],12,36)[1],36)
        result, remaining = review(3,3,60,[(2,36),(1,48),(2,36)],12,36)
        self.assertIn("HOLD",result)
        self.assertEqual(remaining,24)

    def test_prior_approval_cannot_release_revision(self):
        self.assertIn("approval",review(4,3,60,[(2,36)],12,12)[0])

    def test_correction_below_prior_billing_is_an_exception(self):
        self.assertIn("prior billing",review(3,3,60,[(2,10)],12,12)[0])
