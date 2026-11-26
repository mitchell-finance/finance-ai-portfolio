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

    def test_empty_and_truncated_exports_cannot_pass(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as folder:
            export = Path(folder) / "export.csv"
            for body in ("", "5100,North,1800.00\n"):
                export.write_text("account,project,amount_gbp\n" + body)
                with self.assertRaisesRegex(ValueError, "Incomplete export"):
                    balances(export, expected_rows=3)
