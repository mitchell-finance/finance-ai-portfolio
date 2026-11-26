import unittest
from lineage import audit, load


class LineageTests(unittest.TestCase):
    def setUp(self):
        self.closing = load("closing-lines.csv")
        self.opening = load("opening-lines.csv")

    def test_equal_marginals_hide_four_cell_errors(self):
        checks, trace = audit(self.closing, list(reversed(self.opening)))
        for keys in ((), ("account",), ("project",)):
            self.assertEqual(checks[keys], {})
        self.assertEqual(checks["account", "project"], {
            ("Labour","North"):-30025, ("Labour","South"):30025,
            ("Materials","North"):30025, ("Materials","South"):-30025})
        self.assertEqual([t[0] for t in trace], ["B02","B06"])

    def test_balanced_source_totals_do_not_establish_provenance(self):
        # Swap equal-value split lines' source references after fixing their projects.
        self.opening[1].update(project="North", source_id="X04")
        self.opening[5].update(project="South", source_id="X01")
        checks, trace = audit(self.closing, self.opening)
        self.assertFalse(any(checks.values()))
        self.assertEqual(len(trace), 2)

    def test_lost_penny_blocks_line_reconstruction(self):
        self.opening[1]["pence"] -= 1
        with self.assertRaisesRegex(ValueError, "X01"):
            audit(self.closing, self.opening)

    def test_unknown_source_and_duplicate_lines_are_held(self):
        for change in ({"source_id":"UNKNOWN"}, {"line_id":"B01"}):
            with self.subTest(change=change):
                opening = load("opening-lines.csv")
                opening[1].update(change)
                with self.assertRaises(ValueError):
                    audit(self.closing, opening)
