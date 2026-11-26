"""A dated GBP forecast. The opening cleared balance already includes factor advances."""
import argparse
from datetime import date


def forecast(opening, events, through):
    balance = opening
    seen = set()
    timeline = []
    for day, ref, kind, amount, retained in sorted(events):
        if ref in seen:
            raise ValueError("Duplicate cash event")
        seen.add(ref)
        if kind not in {"receipt", "factored settlement", "payment"} or not 0 <= retained <= amount:
            raise ValueError("Review cash input")
        if kind != "factored settlement" and retained:
            raise ValueError("Retention only applies to factor settlements")
        if date.fromisoformat(day) <= date.fromisoformat(through):
            movement = -amount if kind == "payment" else amount - retained
            balance += movement
            timeline.append((day, ref, movement, balance))
    return timeline


EVENTS = [("2026-11-26","Factor remittance","factored settlement",10000,8500),
          ("2026-11-27","Supplier run","payment",14000,0),
          ("2026-11-30","Customer receipt","receipt",5000,0)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--delay-remittance", action="store_true",
                        help="Move the factor remittance from Thursday to the following Tuesday")
    args = parser.parse_args()
    events = EVENTS
    through = "2026-11-30"
    if args.delay_remittance:
        through = "2026-12-01"
        events = [(through if kind == "factored settlement" else day, ref, kind, amount, retained)
                  for day, ref, kind, amount, retained in EVENTS]
    for line in forecast(12000, events, through):
        print(*line, sep=" | ")


if __name__ == "__main__":
    main()
