import unittest
from evaluate import HERE, load, score


class ScoreTests(unittest.TestCase):
    def setUp(self):
        self.reference = {"K": [None, ["K1", "K2"]]}
        self.row = {"case": "K", "rate": None, "evidence": ["K1", "K2"]}

    def evaluate(self, rows):
        return score(rows, self.reference, "K1: signed. K2: also signed.")

    def test_unwarranted_rate_and_missing_clause(self):
        self.row.update(rate=80, evidence=["K1"])
        self.assertEqual(self.evaluate([self.row]), [("K", False, False, True)])

    def test_foreign_citation(self):
        self.row["evidence"].append("X1")
        self.assertFalse(self.evaluate([self.row])[0][2])

    def test_missing_duplicate_and_boolean(self):
        for rows in ([], [self.row, self.row], [dict(self.row, rate=True)]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                self.evaluate(rows)

    def test_recorded_run_can_be_scored(self):
        reference = load(HERE / "reference.json")
        results = score(load(HERE / "observed.json"), reference,
                        (HERE / "prompt.txt").read_text(encoding="utf-8"))
        self.assertEqual(len(results), 8)
        self.assertTrue(all(decision and evidence and not unsafe for _, decision, evidence, unsafe in results))
