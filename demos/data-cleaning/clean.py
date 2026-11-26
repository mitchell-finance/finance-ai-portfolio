"""Propose supplier matches. No master data is modified."""
import unicodedata
from collections import Counter


def normalise(name):
    return " ".join(unicodedata.normalize("NFKC", name).casefold().split())


def classify(source, master):
    counts = Counter(s["id"] for s in master)
    if any(n != 1 for n in counts.values()):
        raise ValueError("Duplicate target ID")
    if len({row["id"] for row in source}) != len(source):
        raise ValueError("Duplicate source ID")
    results = []
    for row in source:
        name_hits = [s for s in master if normalise(s["name"]) == normalise(row["name"])]
        id_hits = [s for s in master if row["entity"] and s["entity"] == row["entity"]]
        if (normalise(row["name"]) and len(id_hits) == 1 and id_hits == name_hits
                and row["account"].strip() and row["account"] == id_hits[0]["account"]):
            outcome = "Candidate for owner review: " + id_hits[0]["id"]
        elif id_hits or name_hits:
            outcome = "Hold: conflicting or incomplete identifiers"
        else:
            outcome = "Unmatched: obtain evidence"
        results.append((row["id"], outcome))
    return results


MASTER = [{"id":"M1","name":"Fen Works","entity":"E1","account":"BANK-A"},
          {"id":"M2","name":"Fen Hire","entity":"E2","account":"BANK-B"}]
SOURCE = [{"id":"L1","name":" FEN  Works ","entity":"E1","account":"BANK-A"},
          {"id":"L2","name":"Fen Works","entity":"E2","account":"BANK-B"},
          {"id":"L3","name":"Fen Hire","entity":"E2","account":"BANK-C"},
          {"id":"L4","name":"New Supply","entity":"","account":""}]


# Sample owner decision. Keep the reviewed values so a later change invalidates approval.
APPROVALS = {"L1": ("M1", " FEN  Works ", "E1", "BANK-A")}


def export_crosswalk(source, master, approvals):
    outcomes = dict(classify(source, master))
    if set(approvals) - outcomes.keys():
        raise ValueError("Approval refers to an unknown source record")
    crosswalk, exceptions = [], []
    for row in source:
        ref = row["id"]
        approval = approvals.get(ref)
        if approval is None:
            exceptions.append((ref, outcomes[ref]))
            continue
        target, name, entity, account = approval
        if ((row["name"], row["entity"], row["account"]) != (name, entity, account)
                or outcomes[ref] != "Candidate for owner review: " + target):
            exceptions.append((ref, "Hold: owner decision no longer matches current evidence"))
            continue
        crosswalk.append((ref, target))
    return crosswalk, exceptions


if __name__ == "__main__":
    crosswalk, exceptions = export_crosswalk(SOURCE, MASTER, APPROVALS)
    for ref, target in crosswalk:
        print(f"Owner-approved export | {ref} -> {target}")
    for ref, decision in exceptions:
        print(f"Exception | {ref} | {decision}")
    print(f"Control: {len(SOURCE)} source rows = {len(crosswalk)} approved + {len(exceptions)} pending")
