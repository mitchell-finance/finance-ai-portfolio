"""A dated GBP forecast. The opening cleared balance already includes factor advances."""
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


if __name__ == "__main__":
    for line in forecast(12000, EVENTS, "2026-11-30"):
        print(*line, sep=" | ")
