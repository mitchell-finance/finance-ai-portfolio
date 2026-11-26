"""Replay one fictional cumulative variation. Values are whole metres and net GBP."""
import json
import re
from datetime import date
from pathlib import Path

HERE = Path(__file__).parent
SCHEMA = {"instruction": {"limit_m", "rate_gbp"}, "signed certificate": {"certified_m"},
          "site diary": {"measured_m"}, "billing register": {"billed_gbp"}}


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
        if ref in seen or doc is None or not claim["quote"] or claim["quote"] not in doc["text"]:
            raise ValueError(f"Check citation {ref}")
        seen.add(ref)
        source, fields = doc["source"], claim["fields"]
        if source not in SCHEMA or set(fields) != SCHEMA[source]:
            raise ValueError(f"Source cannot support these fields: {ref}")
        if any(type(v) is not int or v < 0 for v in fields.values()):
            raise ValueError(f"Check units or values: {ref}")
        if source == "instruction":
            rates = re.findall(r"£([0-9]+) per metre\b", doc["text"])
            if len(rates) != 1 or int(rates[0]) != fields["rate_gbp"]:
                raise ValueError(f"{ref}: verify the extracted rate against the instruction")
        day = date.fromisoformat(doc["date"])
        if day <= cutoff:
            key = (source, day)
            if key in latest:
                raise ValueError(f"Resolve conflicting same-day evidence: {source}")
            latest[key] = (ref, fields)
    for ref, doc in evidence.items():
        if doc["source"] in SCHEMA and date.fromisoformat(doc["date"]) <= cutoff and ref not in seen:
            raise ValueError(f"Missing extraction for {ref}")
    chosen = {}
    for (source, day), record in sorted(latest.items()):
        chosen[source] = record
    if set(chosen) != set(SCHEMA):
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
