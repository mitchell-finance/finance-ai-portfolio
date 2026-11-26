import unittest
from check import HERE, compare, read_rows


class PaymentTests(unittest.TestCase):
    def setUp(self):
        self.approved = read_rows(HERE / "approved.csv")

    def test_equal_totals_hide_substitution(self):
        bank = read_rows(HERE / "bank-export.csv")
        self.assertEqual(len(bank), len(self.approved))
        self.assertEqual(sum(p for _, _, p in bank), 4260000)
        self.assertEqual(sum(p for _, _, p in self.approved), 4260000)
        missing, excess = compare(self.approved, bank)
        self.assertEqual(missing, {("SUP-02","INV-102",240000): 1})
        self.assertEqual(excess, {("SUP-01","INV-101",240000): 1})

    def test_regenerated_file_matches_in_different_order(self):
        self.assertEqual(compare(self.approved, list(reversed(self.approved))), ({}, {}))

    def test_authority_itself_contains_duplicate(self):
        with self.assertRaises(ValueError):
            compare(self.approved + self.approved[:1], self.approved)
