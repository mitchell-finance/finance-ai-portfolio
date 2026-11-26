"""Replay one fictional cumulative variation. Values are whole metres and net GBP."""
import json
import re
from datetime import date
from pathlib import Path

HERE = Path(__file__).parent
# These patterns describe the sample document formats. Unknown wording goes to review.
FORMATS = {
    "instruction": {
        "limit_m": (r"(?:up to|revised total is) ([0-9]+) metres\b", "instruction ceiling"),
        "rate_gbp": (r"£([0-9]+) per metre\b", "extracted rate"),
    },
    "signed certificate": {
        "certified_m": (r"(?:^|[.!?]\s+)I (?:now )?certify ([0-9]+) metres cumulatively for V17\b",
                        "certified quantity"),
    },
    "site diary": {"measured_m": (r"measured total for V17 to date is ([0-9]+) metres\b", "measured quantity")},
    "billing register": {"billed_gbp": (r"V17 previously billed: £(\d{1,3}(?:,\d{3})+|\d+) net\b", "prior billing")},
}


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def assess(documents, claims, cutoff):
    cutoff = date.fromisoformat(cutoff)
    evidence = {doc["id"]: doc for doc in documents}
    if len(evidence) != len(documents):
        raise ValueError("Duplicate evidence ID")
    seen = set()
    latest = {}
    for claim in claims:
        ref = claim["id"]
        doc = evidence.get(ref)
        if doc is None:
            raise ValueError(f"Check citation {ref}")
        day = date.fromisoformat(doc["date"])
        if day > cutoff:
            continue
        if ref in seen or not claim["quote"] or claim["quote"] not in doc["text"]:
            raise ValueError(f"Check citation {ref}")
        seen.add(ref)
        source, fields = doc["source"], claim["fields"]
        if source not in FORMATS or fields.keys() != FORMATS[source].keys():
            raise ValueError(f"Source cannot support these fields: {ref}")
        if any(type(v) is not int or v < 0 for v in fields.values()):
            raise ValueError(f"Check units or values: {ref}")
        for field, (pattern, label) in FORMATS[source].items():
            matches = re.findall(pattern, doc["text"])
            quoted = re.findall(pattern, claim["quote"])
            if len(matches) != 1 or quoted != matches or int(matches[0].replace(",", "")) != fields[field]:
                raise ValueError(f"{ref}: verify the {label} against the {source}")
        key = (source, day)
        if key in latest:
            raise ValueError(f"Resolve conflicting same-day evidence: {source}")
        latest[key] = (ref, fields)
    for ref, doc in evidence.items():
        if doc["source"] in FORMATS and date.fromisoformat(doc["date"]) <= cutoff and ref not in seen:
            raise ValueError(f"Missing extraction for {ref}")
    chosen = {}
    for (source, day), record in sorted(latest.items()):
        chosen[source] = record
    if set(chosen) != set(FORMATS):
        raise ValueError("Incomplete evidence at cut-off")
    values = {k:v for _, fields in chosen.values() for k,v in fields.items()}
    measured, certified = values["measured_m"], values["certified_m"]
    if certified > min(measured, values["limit_m"]):
        raise ValueError("Certificate exceeds the measurement or instruction")
    amount = certified * values["rate_gbp"] - values["billed_gbp"]
    if amount < 0:
        raise ValueError("Prior billing exceeds certified value")
    return amount, measured - certified, [ref for ref, _ in chosen.values()]


if __name__ == "__main__":
    for cutoff in ("2026-10-31", "2026-11-03"):
        amount, pending, refs = assess(load("evidence.json"), load("interpretation.json"), cutoff)
        print(f"{cutoff} | GBP {amount:,} for finance review | {pending} m awaiting certification")
        print("Evidence used: " + ", ".join(refs))
