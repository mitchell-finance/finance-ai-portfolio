import unittest
from clean import APPROVALS, MASTER, SOURCE, classify, export_crosswalk


class MatchChecks(unittest.TestCase):
    def test_clean_conflict_bank_change_and_unmatched(self):
        outcomes = [d.split(":")[0] for _, d in classify(SOURCE, MASTER)]
        self.assertEqual(outcomes, ["Candidate for owner review","Hold","Hold","Unmatched"])

    def test_duplicate_entity_is_ambiguous(self):
        more = MASTER + [dict(MASTER[0], id="M3")]
        self.assertIn("Hold",classify(SOURCE[:1], more)[0][1])

    def test_blank_account_does_not_confirm_match(self):
        self.assertIn("Hold",classify([dict(SOURCE[0],account="")],MASTER)[0][1])

    def test_owner_approved_export_accounts_for_every_row(self):
        approved, pending = export_crosswalk(SOURCE, MASTER, APPROVALS)
        self.assertEqual(approved, [("L1", "M1")])
        self.assertEqual([ref for ref, _ in pending], ["L2", "L3", "L4"])

    def test_changed_bank_label_invalidates_owner_decision(self):
        changed = [dict(SOURCE[0], account="BANK-C")]
        self.assertEqual(export_crosswalk(changed, MASTER, APPROVALS)[0], [])

    def test_ambiguous_or_unknown_source_id_stops_export(self):
        for rows in (SOURCE + [SOURCE[0]], SOURCE[1:]):
            with self.assertRaises(ValueError):
                export_crosswalk(rows, MASTER, APPROVALS)
