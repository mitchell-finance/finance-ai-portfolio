import unittest
from amendments import BASE, CHANGES, DRAFT, exceptions, resolve


class RevisionTests(unittest.TestCase):
    def test_only_explicit_terms_change(self):
        self.assertEqual(exceptions(resolve(BASE, CHANGES), DRAFT), [
            ("first_batch",16,4,"Q1"), ("deliveries_in_price",3,1,"Q1")])

    def test_conflicting_branch_or_reused_revision_blocks(self):
        for amendment in [("Q4","Q1",{"units":20}), ("Q2","Q3",{"units":20})]:
            with self.assertRaises(ValueError):
                resolve(BASE, CHANGES + [amendment])

    def test_missing_term_requires_review(self):
        with self.assertRaises(ValueError):
            exceptions(resolve(BASE, CHANGES), {"units":16})
