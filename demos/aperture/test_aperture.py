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

    def test_revision_must_exist_on_both_records(self):
        for revision in (None, "", 0, -1, True):
            with self.subTest(revision=revision):
                self.assertIn("HOLD", review(revision, revision, 60, [(1, 48)], 12, 36)[0])

    def test_quantities_must_be_whole_units_and_invoice_positive(self):
        for invoice in (True, 0, 1.5):
            self.assertIn("HOLD", review(3, 3, 60, [(1, 48)], 12, invoice)[0])
