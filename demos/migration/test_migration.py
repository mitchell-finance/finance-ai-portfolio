import unittest
from migration import balances, by_account, differences


class MigrationChecks(unittest.TestCase):
    def test_balanced_accounts_hide_project_transfer(self):
        closing = balances("xero.csv")
        mapping = {"N01":"North","N07":"South","S01":"South","HQ":"Central"}
        opening = balances("business-central.csv", mapping)
        self.assertEqual(by_account(closing), by_account(opening))
        self.assertEqual(differences(closing, opening), {("5100","North"):-300, ("5100","South"):300})
        mapping["N07"] = "North"
        self.assertFalse(differences(closing, balances("business-central.csv", mapping)))

    def test_unmapped_project_stops_check(self):
        with self.assertRaises(KeyError):
            balances("business-central.csv", {})

    def test_opening_only_balance_is_visible(self):
        self.assertEqual(differences({}, {("5100","Unexpected"):12}), {("5100","Unexpected"):12})
