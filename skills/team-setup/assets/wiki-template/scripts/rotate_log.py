#!/usr/bin/env python3
"""Monthly log rotation. Keeps the current month + the last 7 days of the previous
month in wiki/log.md; older entries move to wiki/log/YYYY-MM.md (idempotent merge).
Archived skill_update_needed entries are listed as checkboxes in wiki/log/archives.md.
Refuses to write if kept + archived != total.

usage: rotate_log.py --path ROOT [--dry-run] [--date YYYY-MM-DD]
"""
import argparse
import datetime
import os
import re
import sys

HEAD_RE = re.compile(r"(?m)^## \[(\d{4}-\d{2}-\d{2})\]")
LOG_HEADER = "# Log\n\n> Newest first. One title and a [[link]] per entry, 600 characters at most.\n> Navigate: grep \"^## \\[\" wiki/log.md | head\n\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    a = ap.parse_args()
    today = datetime.date.fromisoformat(a.date)
    threshold = today.replace(day=1) - datetime.timedelta(days=7)
    log = os.path.join(a.path, "wiki", "log.md")
    text = open(log, encoding="utf-8").read()
    starts = [m.start() for m in HEAD_RE.finditer(text)]
    if not starts:
        print("no entries")
        return 0
    entries = []
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else len(text)
        chunk = text[s:e].rstrip("\n") + "\n"
        entries.append((HEAD_RE.match(chunk).group(1), chunk))
    entries.sort(key=lambda x: x[0], reverse=True)
    keep = [c for d, c in entries if d >= threshold.isoformat()]
    old = [(d, c) for d, c in entries if d < threshold.isoformat()]
    if len(keep) + len(old) != len(entries):
        print("ENTRIES LOST — refusing to write", file=sys.stderr)
        return 2
    by_month = {}
    for d, c in old:
        by_month.setdefault(d[:7], []).append(c)
    print(f"total {len(entries)} · kept {len(keep)} · archived {len(old)} in {len(by_month)} month file(s)")
    if a.dry_run:
        return 0
    arch_dir = os.path.join(a.path, "wiki", "log")
    os.makedirs(arch_dir, exist_ok=True)
    pending = []
    for month, chunks in by_month.items():
        f = os.path.join(arch_dir, f"{month}.md")
        existing = open(f, encoding="utf-8").read() if os.path.exists(f) else f"# Log archive {month}\n\n"
        add = [c for c in chunks if c.split("\n", 1)[0] not in existing]
        open(f, "w", encoding="utf-8").write(existing.rstrip("\n") + "\n\n" + "\n".join(add))
        pending += [c.split("\n", 1)[0] for c in chunks if "skill_update_needed" in c.split("\n", 1)[0]]
    if pending:
        f = os.path.join(arch_dir, "archives.md")
        cur = open(f, encoding="utf-8").read() if os.path.exists(f) else "# Archived items still to process\n\n"
        cur += f"\n## rotation of {today.isoformat()}\n" + "\n".join(f"- [ ] {p}" for p in pending) + "\n"
        open(f, "w", encoding="utf-8").write(cur)
    open(log, "w", encoding="utf-8").write(LOG_HEADER + "\n".join(keep))
    return 0


if __name__ == "__main__":
    sys.exit(main())
