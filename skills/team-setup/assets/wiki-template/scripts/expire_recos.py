#!/usr/bin/env python3
"""Archive recommended tasks nobody decided on within N days (default 14).
An expired recommendation is NOT a rejection.

Queue: wiki/registers/recommended-tasks.md, sections "## <member>", open items
"- [ ] ... (added YYYY-MM-DD)". Undated items fall back to git blame; if that
fails they are counted as undatable and left alone (archive late, never early).

usage: expire_recos.py --path ROOT [--days 14] [--dry-run] [--date YYYY-MM-DD]
"""
import argparse
import datetime
import os
import re
import subprocess
import sys

QUEUE = "wiki/registers/recommended-tasks.md"
ARCHIVE = "wiki/registers/recommended-tasks-archive.md"
ADDED = re.compile(r"added (\d{4}-\d{2}-\d{2})")


def blame_dates(root, rel):
    try:
        out = subprocess.run(["git", "-C", root, "blame", "--line-porcelain", rel],
                             capture_output=True, text=True, check=True).stdout
    except Exception:
        return None
    dates, cur = [], None
    for l in out.splitlines():
        if l.startswith("author-time "):
            cur = datetime.date.fromtimestamp(int(l.split()[1]))
        elif l.startswith("\t"):
            dates.append(cur)
    return dates


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True)
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    a = ap.parse_args()
    today = datetime.date.fromisoformat(a.date)
    qf = os.path.join(a.path, QUEUE)
    if not os.path.exists(qf):
        print("QUEUE MISSING — nothing measured.")
        return 3
    lines = open(qf, encoding="utf-8").read().splitlines()
    blame = blame_dates(a.path, QUEUE)
    keep, expired, member = [], {}, None
    n_decl = n_blame = n_undatable = 0
    i = 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("## "):
            member = l[3:].split(" — ")[0].strip()
        if l.startswith("- [ ]"):
            block = [l]
            j = i + 1
            while j < len(lines) and lines[j].startswith(("  ", "\t")) and lines[j].strip():
                block.append(lines[j]); j += 1
            m = ADDED.search(" ".join(block))
            d, src = None, None
            if m:
                d, src = datetime.date.fromisoformat(m.group(1)), "declared"
            elif blame and i < len(blame) and blame[i]:
                d, src = blame[i], "inferred from git"
            if d is None:
                n_undatable += 1
                keep += block
            elif (today - d).days > a.days:
                n_decl += src == "declared"
                n_blame += src != "declared"
                expired.setdefault(member or "unassigned", []).append("\n".join(block) + f"  <!-- {src} {d} -->")
            else:
                keep += block
            i = j
            continue
        keep.append(l)
        i += 1
    total = sum(len(v) for v in expired.values())
    print(f"expired {total} (declared {n_decl}, git {n_blame}) · undatable {n_undatable}")
    if a.dry_run or not total:
        return 0
    open(qf, "w", encoding="utf-8").write("\n".join(keep) + "\n")
    af = os.path.join(a.path, ARCHIVE)
    cur = open(af, encoding="utf-8").read() if os.path.exists(af) else "# Recommended tasks — archive\n\n> Expired without a decision. Not rejections.\n"
    cur += f"\n## Expired without a decision — {today.isoformat()}\n"
    for m, items in expired.items():
        cur += f"\n### {m}\n" + "\n".join(items) + "\n"
    open(af, "w", encoding="utf-8").write(cur)
    return 0


if __name__ == "__main__":
    sys.exit(main())
