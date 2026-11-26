import unittest
from clean import classify, SOURCE, MASTER


class MatchChecks(unittest.TestCase):
    def test_clean_conflict_bank_change_and_unmatched(self):
        outcomes = [d.split(":")[0] for _, d in classify(SOURCE, MASTER)]
        self.assertEqual(outcomes, ["Candidate for owner review","Hold","Hold","Unmatched"])

    def test_duplicate_entity_is_ambiguous(self):
        more = MASTER + [dict(MASTER[0], id="M3")]
        self.assertIn("Hold",classify(SOURCE[:1], more)[0][1])

    def test_blank_account_does_not_confirm_match(self):
        self.assertIn("Hold",classify([dict(SOURCE[0],account="")],MASTER)[0][1])
