"""Review a proposed CRM update against supplied evidence. No live CRM writes."""
import json
from pathlib import Path


def review(case):
    notes = {n["id"]: n for n in case["notes"]}
    if len(notes) != len(case["notes"]):
        raise ValueError("Duplicate note ID")
    proposal = case["candidate"]
    stage_note = notes[proposal["stage_evidence"]]
    action_note = notes[proposal["action_evidence"]]
    if stage_note["speaker"] != "Buyer":
        raise ValueError("Stage evidence must cite the buyer")
    if proposal["owner"] != action_note["speaker"]:
        raise ValueError("Action owner differs from the cited speaker")
    if proposal["stage"] != "Won":
        raise ValueError("This example evaluates a proposed move to Won only")
    orders = [o for o in case["order_register"]
              if o["opportunity"] == case["opportunity"] and o["verified"] is True
              and isinstance(o["reference"], str) and o["reference"].strip()]
    return {
        "stage": case["stage"],
        "decision": "Review move to Won against verified order" if orders else "Hold proposed move to Won",
        "buyer_evidence": stage_note["quote"],
        "suggested_task": (proposal["owner"], proposal["next_action"], action_note["quote"]),
    }


if __name__ == "__main__":
    result = review(json.loads(Path(__file__).with_name("meeting.json").read_text(encoding="utf-8")))
    print(result["decision"], "| current stage:", result["stage"])
    print("Buyer:", result["buyer_evidence"])
    owner, task, citation = result["suggested_task"]
    print("Task for review:", owner, "|", task)
    print("Evidence:", citation)
