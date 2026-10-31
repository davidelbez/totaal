#!/usr/bin/env python3
"""Duplicate-fact guard for append-only journals. Never writes.

usage: journal_guard.py --journal FILE (--line "candidate line" | --stdin) [--head N]

Extracts content tokens from the candidate (emails, quoted subjects, `ids`,
long numbers, hex ids, ticket-like references) and looks for them in the journal.
Exit 0 clean · 1 collision (same fact already logged) · 2 negation or reversal
(the line asserts an absence, or flips a resolved item, while the fact exists)
· 3 journal missing (explicitly NOT "no collision").
"""
import argparse
import re
import sys
import unicodedata

import json
import os

_CFG = {}
try:
    _CFG = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".wiki.json"))).get("journal_guard", {})
except Exception:
    pass
# Add words in your own language in .wiki.json: {"journal_guard": {"negation": [...], "alert": [...], "resolved": [...]}}
NEGATION = re.compile(r"\b(" + "|".join(["no reply", "no answer", "not received", "not sent", "never", "nothing", "missing", "no response", "still waiting"] + _CFG.get("negation", [])) + r")\b", re.I)
ALERT = re.compile(r"\b(" + "|".join(["urgent", "blocked", r"escalat\w*", "open again", "reopened"] + _CFG.get("alert", [])) + r")\b", re.I)
RESOLVED = re.compile(r"\b(" + "|".join(["resolved", "closed", "done", "fixed", "settled"] + _CFG.get("resolved", [])) + r")\b", re.I)
TOKEN_RES = [
    re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),
    re.compile(r"\"([^\"]{8,})\"|“([^”]{8,})”"),
    re.compile(r"`([^`]{4,})`"),
    re.compile(r"\b\d{9,}\b"),
    re.compile(r"\b[0-9a-f]{32}\b"),
    re.compile(r"\b[A-Z]{2,}-?\d{3,}\b"),
]


def norm(s):
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()


def tokens(line):
    out = set()
    for r in TOKEN_RES:
        for m in r.finditer(line):
            t = next((g for g in m.groups() if g), None) if m.groups() else m.group(0)
            t = t or m.group(0)
            if len(t) >= 4:
                out.add(norm(t.strip()))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--journal", required=True)
    ap.add_argument("--line")
    ap.add_argument("--stdin", action="store_true")
    ap.add_argument("--head", type=int, default=0, help="only compare with the first N lines")
    a = ap.parse_args()
    try:
        jl = open(a.journal, encoding="utf-8").read().splitlines()
    except FileNotFoundError:
        print("JOURNAL MISSING — this is not 'no collision'.")
        return 3
    if a.head:
        jl = jl[:a.head]
    cands = sys.stdin.read().splitlines() if a.stdin else [a.line or ""]
    worst = 0
    for c in filter(None, cands):
        if c in jl:
            continue
        toks = tokens(c)
        hits = [l for l in jl if any(t in norm(l) for t in toks)]
        if not hits:
            continue
        code = 1
        if NEGATION.search(c):
            code = 2
            print(f"NEGATION: candidate asserts an absence but the fact exists:\n  {c}\n  vs {hits[0]}")
        elif ALERT.search(c) and any(RESOLVED.search(h) for h in hits):
            code = 2
            print(f"REVERSAL: candidate re-opens a resolved item:\n  {c}\n  vs {hits[0]}")
        else:
            print(f"COLLISION: same fact already logged:\n  {c}\n  vs {hits[0]}")
        worst = max(worst, code)
    if worst == 0:
        print("CLEAN")
    return worst


if __name__ == "__main__":
    sys.exit(main())
