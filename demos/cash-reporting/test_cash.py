import unittest
from cash import forecast, EVENTS


class CashChecks(unittest.TestCase):
    def test_monday_recovery_does_not_fund_friday(self):
        rows = forecast(12000, EVENTS, "2026-11-30")
        self.assertEqual([r[-1] for r in rows], [13500,-500,4500])
        self.assertEqual(forecast(12000, EVENTS, "2026-11-27")[-1][-1],-500)

    def test_duplicate_event_held(self):
        with self.assertRaises(ValueError):
            forecast(12000, EVENTS + EVENTS[:1], "2026-11-30")
