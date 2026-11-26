"""Propose supplier matches. No master data is modified."""
import unicodedata
from collections import Counter


def normalise(name):
    return " ".join(unicodedata.normalize("NFKC", name).casefold().split())


def classify(source, master):
    counts = Counter(s["id"] for s in master)
    if any(n != 1 for n in counts.values()):
        raise ValueError("Duplicate target ID")
    results = []
    for row in source:
        name_hits = [s for s in master if normalise(s["name"]) == normalise(row["name"])]
        id_hits = [s for s in master if row["entity"] and s["entity"] == row["entity"]]
        if len(id_hits) == 1 and id_hits == name_hits and row["account"] and row["account"] == id_hits[0]["account"]:
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


if __name__ == "__main__":
    for source_id, decision in classify(SOURCE, MASTER):
        print(source_id, decision, sep=" | ")
