#!/usr/bin/env python3
"""Project the flat skill sources (wiki/skills/<slug>/) into each company plugin
(wiki/plugins/<plugin>/skills/<slug>/), as declared in wiki/plugins/<plugin>/skills.list.

The plugin skills/ folders are GENERATED and gitignored: never edit them.
A slug may appear in exactly one skills.list (enforced here).
"""
import os
import shutil
import sys

ROOT = os.environ.get("WIKI_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    plugins_dir = os.path.join(ROOT, "wiki", "plugins")
    flat = os.path.join(ROOT, "wiki", "skills")
    if not os.path.isdir(plugins_dir):
        print("sync: no wiki/plugins — nothing to do")
        return 0
    owner, errors, n = {}, [], 0
    for p in sorted(os.listdir(plugins_dir)):
        lst = os.path.join(plugins_dir, p, "skills.list")
        if not os.path.isfile(lst):
            continue
        slugs = [l.strip() for l in open(lst, encoding="utf-8") if l.strip() and not l.lstrip().startswith("#")]
        out = os.path.join(plugins_dir, p, "skills")
        os.makedirs(out, exist_ok=True)
        for d in os.listdir(out):
            if d not in slugs:
                shutil.rmtree(os.path.join(out, d), ignore_errors=True)
        for s in slugs:
            if s in owner:
                errors.append(f"slug '{s}' listed in both {owner[s]} and {p}")
                continue
            owner[s] = p
            src = os.path.join(flat, s)
            if not os.path.isfile(os.path.join(src, "SKILL.md")):
                errors.append(f"{p}: flat skill wiki/skills/{s}/SKILL.md missing")
                continue
            shutil.rmtree(os.path.join(out, s), ignore_errors=True)
            shutil.copytree(src, os.path.join(out, s))
            n += 1
    for e in errors:
        print("ERROR:", e, file=sys.stderr)
    if errors:
        return 1
    print(f"sync OK — {n} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())
