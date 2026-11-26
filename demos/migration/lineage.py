"""Compare signed opening balances and trace split postings back to closing lines."""
import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parent


def load(name):
    with (ROOT / name).open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    for row in rows:
        row["pence"] = int(row["pence"])
    return rows


def totals(rows, keys):
    result = Counter()
    for row in rows:
        result[tuple(row[k] for k in keys)] += row["pence"]
    return result


def delta(closing, opening, keys):
    before, after = totals(closing, keys), totals(opening, keys)
    return {key: after[key] - before[key] for key in sorted(before.keys() | after.keys())
            if before[key] != after[key]}


def audit(closing, opening):
    sources = {row["source_id"]: row for row in closing}
    if not closing or not opening or len(sources) != len(closing):
        raise ValueError("Review empty exports or duplicate closing IDs")
    if len({row["line_id"] for row in opening}) != len(opening):
        raise ValueError("Duplicate opening line ID")
    trace = []
    linked = defaultdict(list)
    for row in opening:
        ref = row["source_id"]
        if ref not in sources:
            raise ValueError(f"Unknown source on {row['line_id']}: {ref}")
        linked[ref].append(row)
        origin = sources[ref]
        if (row["account"], row["project"]) != (origin["account"], origin["project"]):
            trace.append((row["line_id"], ref, row["account"], row["project"],
                          origin["account"], origin["project"], row["pence"]))
    for ref, origin in sources.items():
        if not linked[ref] or sum(r["pence"] for r in linked[ref]) != origin["pence"]:
            raise ValueError(f"Opening allocations do not reconstruct {ref}")
    return {keys: delta(closing, opening, keys) for keys in
            [(), ("account",), ("project",), ("account", "project")]}, sorted(trace)


def main():
    closing, opening = load("closing-lines.csv"), load("opening-lines.csv")
    checks, trace = audit(closing, opening)
    for keys, changes in checks.items():
        print(f"{' x '.join(keys) or 'Signed ledger'}: {len(changes)} differences")
        for cell, pence in changes.items():
            print("  " + " / ".join(cell) + f": {pence:+d} pence")
    for line, ref, account, project, expected_account, expected_project, amount in trace:
        print(f"HOLD {line} ({ref}): {amount} pence in {account}/{project}; "
              f"source shows {expected_account}/{expected_project}")
    # Replay two reviewed corrections on a copy of the opening extract.
    reviewed = {"B02": "North", "B06": "South"}
    corrected = [dict(r, project=reviewed.get(r["line_id"], r["project"])) for r in opening]
    final_checks, final_trace = audit(closing, corrected)
    if any(final_checks.values()) or final_trace:
        raise ValueError("Corrected extract still has exceptions")
    print("Corrected replay: all four totals checks and source-line checks agree.")


if __name__ == "__main__":
    main()
