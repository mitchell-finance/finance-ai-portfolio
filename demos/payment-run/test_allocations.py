import unittest
from allocations import load_case, reconcile


class AllocationTests(unittest.TestCase):
    def setUp(self):
        self.case = load_case()

    def test_balanced_in_both_directions_still_pays_wrong_beneficiaries(self):
        report = reconcile(self.case)
        self.assertEqual(report["Invoice allocation difference"], [])
        self.assertEqual(report["Transfer allocation difference"], [])
        self.assertEqual(report["Wrong beneficiary"], [
            ("T02","B09","South","North",100000), ("T03","A18","North","South",100000)])

    def test_grouped_and_split_after_correction(self):
        self.case["allocations"][-2:] = [["T02","A18",100000],["T03","B09",100000]]
        self.assertFalse(any(reconcile(self.case).values()))

    def test_deleted_allocation_reports_both_sides(self):
        self.case["allocations"].pop()
        report = reconcile(self.case)
        self.assertIn(("T03",-100000), report["Transfer allocation difference"])
        self.assertIn(("A18",-100000), report["Invoice allocation difference"])

    def test_duplicate_and_orphan_rows_block(self):
        for row in (["T01","A17",280000],["T99","A17",20000]):
            with self.subTest(row=row):
                case = load_case()
                case["allocations"].append(row)
                with self.assertRaises(ValueError):
                    reconcile(case)
