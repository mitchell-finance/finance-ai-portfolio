import subprocess
import sys
import unittest
from pathlib import Path
from cash import forecast, EVENTS


class CashChecks(unittest.TestCase):
    def test_monday_recovery_does_not_fund_friday(self):
        rows = forecast(12000, EVENTS, "2026-11-30")
        self.assertEqual([r[-1] for r in rows], [13500,-500,4500])
        self.assertEqual(forecast(12000, EVENTS, "2026-11-27")[-1][-1],-500)

    def test_duplicate_event_held(self):
        with self.assertRaises(ValueError):
            forecast(12000, EVENTS + EVENTS[:1], "2026-11-30")

    def test_delayed_remittance_moves_the_cash_once(self):
        script = Path(__file__).with_name("cash.py")
        output = subprocess.check_output([sys.executable, str(script), "--delay-remittance"], text=True)
        self.assertEqual(output.splitlines(), [
            "2026-11-27 | Supplier run | -14000 | -2000",
            "2026-11-30 | Customer receipt | 5000 | 3000",
            "2026-12-01 | Factor remittance | 1500 | 4500",
        ])
