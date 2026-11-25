import csv
from pathlib import Path
from typing import Dict, List


def load_telemetry(csv_path: str) -> List[Dict[str, str]]:
    """Read telemetry rows exported from the UNROT. Brain Profile view."""
    path = Path(csv_path)
    if not path.exists():
        return []
    with path.open(mode="r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def summarize_session(rows: List[Dict[str, str]]) -> Dict[str, object]:
    """Compute summary metrics from logged focus and distraction reps."""
    if not rows:
        return {
            "total_events": 0,
            "positive_reps": 0,
            "negative_reps": 0,
            "final_immunity": 100,
        }

    deltas = [int(r.get("Delta", 0)) for r in rows]
    final_immunity = int(rows[-1].get("Immunity", 100))

    return {
        "total_events": len(rows),
        "positive_reps": sum(1 for d in deltas if d > 0),
        "negative_reps": sum(1 for d in deltas if d < 0),
        "final_immunity": final_immunity,
    }


if __name__ == "__main__":
    sample_rows = [
        {"Time": "09:15:00", "Mode": "15s Feed", "Outcome": "Held focus", "Delta": "6", "Immunity": "100"},
        {"Time": "09:16:10", "Mode": "01 Stroop", "Outcome": "Solved (BLUE)", "Delta": "5", "Immunity": "100"},
    ]
    print("UNROT Telemetry Summary:", summarize_session(sample_rows))
