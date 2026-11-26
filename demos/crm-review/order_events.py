"""Replay a reviewed order feed. Versions replace the prior value of the same order."""
def forecast(deal, value, events):
    messages, revisions, orders = {}, {}, {}
    for event_id, opportunity, order, version, amount in events:
        payload = (opportunity, order, version, amount)
        if event_id in messages and messages[event_id] != payload:
            raise ValueError("Same message ID has conflicting contents")
        messages[event_id] = payload
        if opportunity != deal:
            continue
        if type(amount) is not int or amount < 0 or type(version) is not int or version < 1:
            raise ValueError("Invalid order revision")
        key = (order, version)
        if key in revisions and revisions[key] != amount:
            raise ValueError("Conflicting values for the same order revision")
        revisions[key] = amount
        if order not in orders or version > orders[order][0]:
            orders[order] = (version, amount)
    booked = sum(amount for _, amount in orders.values())
    if booked > value:
        raise ValueError("Orders exceed opportunity; review scope")
    return booked, value - booked


EVENTS = [
    ("M02","OP17","PO8",2,16000), ("M01","OP17","PO8",1,12000),
    ("M02","OP17","PO8",2,16000), ("M03","OP99","PO9",1,32000),
]


if __name__ == "__main__":
    booked, open_value = forecast("OP17", 48000, EVENTS)
    print(f"Verified order cover: GBP {booked:,}; still open: GBP {open_value:,}")
