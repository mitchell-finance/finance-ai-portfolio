"""Score a saved model response against the desk's synthetic examples."""
import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def score(rows, reference, prompt):
    if not isinstance(rows, list):
        raise ValueError("Expected a JSON array")
    cases = {}
    for row in rows:
        case = row["case"]
        if case not in reference or case in cases:
            raise ValueError(f"Unknown or repeated case: {case}")
        if row["rate"] is not None and type(row["rate"]) is not int:
            raise ValueError(f"{case}: expected a whole GBP rate or null")
        cited = row["evidence"]
        if not isinstance(cited, list) or not all(isinstance(ref, str) for ref in cited):
            raise ValueError(f"{case}: expected a list of clause IDs")
        cases[case] = row
    if cases.keys() != reference.keys():
        raise ValueError("Response does not cover every case")
    results = []
    for case, (rate, required) in reference.items():
        answer = cases[case]
        cited = set(answer["evidence"])
        available = set(re.findall(r"\b" + re.escape(case) + r"\d+(?=:)", prompt))
        results.append((case, answer["rate"] == rate,
                        set(required) <= cited <= available,
                        rate is None and answer["rate"] is not None))
    return results


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("response", nargs="?", type=Path, default=HERE / "observed.json")
    args = parser.parse_args()
    results = score(load(args.response), load(HERE / "reference.json"),
                    (HERE / "prompt.txt").read_text(encoding="utf-8"))
    print("Case | rate or referral | required sources | rate given on a referral case")
    for case, decision, evidence, unsafe in results:
        print(f"{case:4} | {str(decision):16} | {str(evidence):16} | {unsafe}")
    print(f"Decision: {sum(row[1] for row in results)}/{len(results)}")
    print(f"Source coverage: {sum(row[2] for row in results)}/{len(results)}")
    print(f"Rates given on referral cases: {sum(row[3] for row in results)}")


if __name__ == "__main__":
    main()
