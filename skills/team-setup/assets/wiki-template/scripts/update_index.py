#!/usr/bin/env python3
"""Upsert one entry in wiki/index.md.

usage: update_index.py --path ROOT --category Concepts --title "Title" --page-path wiki/concepts/x.md [--summary "..."]

Entry format: - [Title](relative/link.md) — summary
Sections are kept in a canonical order. Run it for every new or updated page.
Never chain it with && before a commit: if it fails, the commit would be skipped.
"""
import argparse
import os
import re
import sys

CANONICAL_ORDER = ["By domain", "Onboarding", "Sources", "Entities", "Accounts",
                   "Team", "Concepts", "Notes", "Decisions", "Routines", "Reports", "Skills"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True)
    ap.add_argument("--category", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--page-path", required=True)
    ap.add_argument("--summary", default="")
    a = ap.parse_args()

    root = os.path.abspath(a.path)
    index = os.path.join(root, "wiki", "index.md")
    if not os.path.exists(index):
        print(f"ERROR: {index} not found", file=sys.stderr)
        return 2
    page = os.path.abspath(os.path.join(root, a.page_path)) if not os.path.isabs(a.page_path) else a.page_path
    idx_dir = os.path.dirname(index)
    link = os.path.relpath(page, idx_dir)
    if link.startswith(".."):
        print("ERROR: page is outside wiki/", file=sys.stderr)
        return 2
    cat = a.category if a.category[:1] in "#@" else a.category[:1].upper() + a.category[1:]

    text = open(index, encoding="utf-8").read()
    parts = re.split(r"(?m)^## ", text)
    header = parts[0]
    sections = []
    for p in parts[1:]:
        name, _, body = p.partition("\n")
        lines = [l for l in body.split("\n") if l.strip()]
        sections.append([name.strip(), lines])

    entry = f"- [{a.title}]({link})" + (f" — {a.summary}" if a.summary else "")
    target = next((s for s in sections if s[0].lower() == cat.lower()), None)
    if target is None:
        target = [cat, []]
        sections.append(target)
    pat = re.compile(r"^\s*-\s*\[" + re.escape(a.title) + r"\]\(")
    for i, l in enumerate(target[1]):
        if pat.match(l):
            target[1][i] = entry
            break
    else:
        target[1].append(entry)

    def key(s):
        try:
            return (0, CANONICAL_ORDER.index(s[0]))
        except ValueError:
            return (1, 0)
    sections.sort(key=key)
    out = header.rstrip("\n") + "\n\n"
    for name, lines in sections:
        out += f"## {name}\n" + "\n".join(lines) + "\n\n"
    open(index, "w", encoding="utf-8").write(out.rstrip("\n") + "\n")
    print(f"index: {cat} <- {a.title}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
