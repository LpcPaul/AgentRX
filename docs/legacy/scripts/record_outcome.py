#!/usr/bin/env python3
"""
AgentRX — Record a case outcome and advance verification status.

Usage:
    python3 scripts/record_outcome.py \
        --case-id 2026-04-17-browse-web-001 \
        --outcome resolved \
        --notes "playwright-mcp rendered the page; extracted full table"

Behavior:
    1. Finds the case file by ID (scans cases/ and cases/seeds/)
    2. Appends a resolution entry to the resolutions array
    3. If resolved count >= 2 and source != synthetic-seed, sets verified=true
    4. Rebuilds the index via build_index.py
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES_DIR = ROOT / "cases"


def find_case_file(case_id: str) -> Path:
    """Find case file by ID, scanning top-level and seeds/ directory."""
    for pattern in ["*.json", "seeds/*.json"]:
        for f in CASES_DIR.glob(pattern):
            if case_id in f.stem:
                return f
    raise FileNotFoundError(f"Case not found: {case_id}")


def record_outcome(case_id: str, outcome: str, notes: str) -> None:
    case_path = find_case_file(case_id)

    with open(case_path, "r", encoding="utf-8") as f:
        case = json.load(f)

    # Initialize resolutions array if absent
    if "resolutions" not in case:
        case["resolutions"] = []

    # Append new outcome
    entry = {
        "outcome": outcome,
        "recorded_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "notes": notes or "",
    }
    case["resolutions"].append(entry)

    # Also update legacy resolution field for backward compatibility
    case["resolution"] = {"outcome": outcome, "follow_up_notes": notes or ""}

    # Auto-verify if >=2 resolved and not synthetic seed
    resolved_count = sum(1 for r in case["resolutions"] if r["outcome"] == "resolved")
    if resolved_count >= 2 and case.get("source") != "synthetic-seed":
        case["verified"] = True
        print(f"  Case auto-verified: {resolved_count} resolved outcomes")

    # Write back
    with open(case_path, "w", encoding="utf-8") as f:
        json.dump(case, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Outcome recorded: {outcome}")
    print(f"  Case: {case_id}")
    print(f"  Resolutions: {len(case['resolutions'])}")
    print(f"  Verified: {case.get('verified', False)}")

    # Rebuild index
    print("  Rebuilding index...")
    build_script = ROOT / "scripts" / "build_index.py"
    subprocess.run([sys.executable, str(build_script)], check=True)


def main():
    parser = argparse.ArgumentParser(description="Record a case outcome.")
    parser.add_argument("--case-id", required=True, help="Case ID to record outcome for")
    parser.add_argument("--outcome", required=True, choices=["resolved", "partially_resolved", "unresolved"], help="Outcome of following the recommended route")
    parser.add_argument("--notes", default="", help="Brief note about what happened")
    args = parser.parse_args()

    try:
        record_outcome(args.case_id, args.outcome, args.notes)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
