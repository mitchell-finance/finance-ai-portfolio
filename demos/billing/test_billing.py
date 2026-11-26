import unittest
from billing import assess


class BillingChecks(unittest.TestCase):
    def test_another_jobs_report_is_not_evidence(self):
        self.assertIn("Hold", assess(("A", "complete", 50),
            [{"id":"S", "original":"B", "filed":"A"}], []))

    def test_duplicate_drafts_are_held(self):
        self.assertIn("duplicate", assess(("A", "complete", 50),
            [{"id":"S", "original":"A", "filed":"A"}],
            [("D1","A","DRAFT",50), ("D2","A","DRAFT",50)]))

    def test_posted_job_cannot_be_billed_again(self):
        self.assertIn("Already invoiced", assess(("A", "complete", 50), [],
            [("I1","A","AUTHORISED",50)]))

    def test_posted_invoice_must_cover_the_job_value(self):
        for amount, difference in ((1, "+749"), (800, "-50")):
            result = assess(("A", "complete", 750), [], [("I1", "A", "AUTHORISED", amount)])
            self.assertTrue(result.startswith("Hold"))
            self.assertIn(difference, result)

    def test_draft_alongside_posted_invoice_is_held(self):
        self.assertIn("Hold", assess(("A", "complete", 750), [],
            [("I1", "A", "AUTHORISED", 750), ("D1", "A", "DRAFT", 750)]))
