"""Independent replay of one order line. Quantities are units, prices are integer pence."""
def review(order_revision, approved_revision, received, inspections, billed, invoice):
    if not inspections:
        raise ValueError("Missing inspection")
    current = {}
    for version, accepted in inspections:
        if type(version) is not int or version < 1 or type(accepted) is not int or not 0 <= accepted <= received:
            raise ValueError("Invalid inspection")
        if version in current and current[version] != accepted:
            raise ValueError("Conflicting inspection revision")
        current[version] = accepted
    accepted = current[max(current)]
    if order_revision != approved_revision:
        return "HOLD: obtain approval for this order revision", 0
    if min(billed, invoice) < 0 or billed > accepted:
        return "HOLD: reconcile prior billing and accepted quantity", 0
    available = accepted - billed
    return ("HOLD: invoice exceeds remaining accepted units" if invoice > available
            else "MATCH: finance review"), available


if __name__ == "__main__":
    for events in [[(1, 48)], [(2, 36), (1, 48)]]:
        print(review(3, 3, 60, events, 12, 36))
