import unittest
from pack import HERE, compare, read


class PackChecks(unittest.TestCase):
    def setUp(self):
        self.pack = read(HERE / "issued.json")
        self.invoice = read(HERE / "invoice.json")
        self.export = read(HERE / "project-costs.json")

    def test_repeated_review_preserves_issued_pack(self):
        for _ in range(2):
            self.assertEqual(compare(self.pack, self.invoice, self.export), (42000,6000,8400,39600))
        self.assertEqual(self.pack, read(HERE / "issued.json"))

    def test_equal_total_wrong_date_stops_pack(self):
        with self.assertRaisesRegex(ValueError, "Replace the export"):
            compare(self.pack,self.invoice,read(HERE / "stale-project-costs.json"))

    def test_same_job_different_work_cannot_release_accrual(self):
        self.invoice["work_ref"] = "W9"
        with self.assertRaisesRegex(ValueError, "different work"):
            compare(self.pack,self.invoice,self.export)

    def test_unexplained_cost_change_is_held(self):
        self.export["other_costs_gbp"] += 100
        with self.assertRaisesRegex(ValueError, "separately"):
            compare(self.pack,self.invoice,self.export)
