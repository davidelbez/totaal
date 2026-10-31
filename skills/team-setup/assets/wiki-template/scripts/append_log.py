#!/usr/bin/env python3
"""Insert one entry at the TOP of wiki/log.md (newest first).

usage: append_log.py --path ROOT --action update --title "one line" [--details "..."] [--date YYYY-MM-DD]

Heading format: ## [YYYY-MM-DD] action | title
Keep entries short: a title and a [[link]], 600 characters at most.
The action skill_update_needed is the queue the evening tuning reads.
"""
import argparse
import datetime
import os
import re
import sys

ACTIONS = {"ingest", "query", "lint", "bootstrap", "schema-evolve", "note", "update", "audit",
           "setup", "restructure", "decision", "arbitration", "routine", "onboarding",
           "skill_update_needed", "skill_update_processed", "tuning", "review"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True)
    ap.add_argument("--action", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--details", default="")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    a = ap.parse_args()
    if a.action not in ACTIONS:
        print(f"ERROR: action must be one of {sorted(ACTIONS)}", file=sys.stderr)
        return 2
    if "\n" in a.title:
        print("ERROR: title must be one line", file=sys.stderr)
        return 2
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", a.date):
        print("ERROR: date must be YYYY-MM-DD", file=sys.stderr)
        return 2
    entry = f"## [{a.date}] {a.action} | {a.title}\n" + (a.details.rstrip() + "\n" if a.details else "")
    if len(entry) > 600:
        print(f"WARNING: entry is {len(entry)} chars (> 600). Put the story in a page and link it.", file=sys.stderr)
    log = os.path.join(a.path, "wiki", "log.md")
    if not os.path.exists(log):
        print(f"ERROR: {log} not found", file=sys.stderr)
        return 2
    text = open(log, encoding="utf-8").read()
    m = re.search(r"(?m)^## \[\d{4}-\d{2}-\d{2}\]", text)
    if m:
        text = text[:m.start()] + entry + "\n" + text[m.start():]
    else:
        text = text.rstrip("\n") + "\n\n" + entry
    open(log, "w", encoding="utf-8").write(text)
    print(f"log: [{a.date}] {a.action} | {a.title}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
