"""Resolve a reviewed chain of partial amendments, then compare draft terms."""
def resolve(base, amendments):
    terms = {k: (v, "Q1") for k, v in base.items()}
    head = "Q1"
    seen = {head}
    for ref, parent, changes in amendments:
        if ref in seen or parent != head or not changes or changes.keys() - terms.keys():
            raise ValueError("Resolve revision history before quoting")
        terms.update({key: (value, ref) for key, value in changes.items()})
        seen.add(ref)
        head = ref
    return terms


def exceptions(terms, draft):
    if set(draft) != set(terms):
        raise ValueError("Draft and authority must cover the same terms")
    return [(key, draft[key], value, ref) for key, (value, ref) in terms.items()
            if draft[key] != value]


BASE = {"units": 12, "first_batch": 4, "first_week": 6, "deliveries_in_price": 1}
CHANGES = [("Q2", "Q1", {"first_week": 8}), ("Q3", "Q2", {"units": 16})]
DRAFT = {"units": 16, "first_batch": 16, "first_week": 8, "deliveries_in_price": 3}


if __name__ == "__main__":
    for key, offered, approved, source in exceptions(resolve(BASE, CHANGES), DRAFT):
        print(f"HOLD {key}: draft {offered}; agreed {approved} under {source}")
