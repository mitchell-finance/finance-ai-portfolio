import sqlite3
import unittest
from recover import BATCH, ROWS, closed_batch, initialise, inspect, recover


class ImportRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.addCleanup(self.db.close)
        initialise(self.db)
        self.source = closed_batch(ROWS, 3, 362500)

    def seed(self, rows):
        with self.db:
            self.db.executemany("INSERT INTO staged VALUES (?, ?, ?, ?)", rows)

    def test_detects_gap_despite_later_invoice_and_replays_once(self):
        self.seed([(BATCH, *ROWS[0]), (BATCH, *ROWS[2]), ("other", *ROWS[1])])
        self.assertEqual(recover(self.db, BATCH, self.source), ["S102"])
        self.assertEqual(recover(self.db, BATCH, self.source), [])
        self.assertEqual(inspect(self.db, BATCH, self.source), ([], [], []))

    def test_equal_totals_with_wrong_customer_hold(self):
        self.seed([(BATCH, key, "East", value) for key, _, value in ROWS])
        with self.assertRaisesRegex(ValueError, "conflicting"):
            recover(self.db, BATCH, self.source)

    def test_unexpected_row_blocks_all_inserts(self):
        self.seed([(BATCH, "S104", "North", 100)])
        with self.assertRaisesRegex(ValueError, "S104"):
            recover(self.db, BATCH, self.source)
        self.assertEqual(len(inspect(self.db, BATCH, self.source)[0]), 3)

    def test_incomplete_and_duplicate_source_rejected(self):
        for rows in ([], ROWS[:2], [ROWS[0], ROWS[0], ROWS[2]]):
            with self.assertRaises(ValueError):
                closed_batch(rows, 3, 362500)

    def test_mid_recovery_failure_rolls_back(self):
        self.db.execute("""CREATE TRIGGER interrupted BEFORE INSERT ON staged
            WHEN NEW.invoice='S102' BEGIN SELECT RAISE(ABORT, 'interrupted'); END""")
        with self.assertRaises(sqlite3.IntegrityError):
            recover(self.db, BATCH, self.source)
        self.assertEqual(inspect(self.db, BATCH, self.source)[0], ["S101", "S102", "S103"])
