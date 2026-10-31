#!/usr/bin/env python3
"""Commit check for skill patches (the "four boxes"). Looks only at ADDED lines of
staged wiki/skills/*/SKILL.md files and of wiki/log.md.

Checks patches to EXISTING files only (a new skill is not checked line by line).
1. One rule per line: at most one **bold** span, fewer than two ';' outside code.
2. Each added rule line (bullet) carries a [[link]] to the page holding the story.
3. The linked page exists in wiki/.
4. A new log entry is at most 600 characters.
Escape hatch: put <!-- short-format:exempt --> on the line and justify it in the commit body.

usage: check_short_format.py [--range A..B]   (default: staged changes)
Exit 0 ok, 1 blocked.
"""
import argparse
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK = re.compile(r"\[\[([^\]|#]+)")
RULE = re.compile(r"^\s*[-*]\s+\S")


def added(path_glob, rng):
    # --diff-filter=M: only patches to existing files; a brand-new skill is written whole by skill-writer
    cmd = ["git", "-C", ROOT, "diff", "-U0", "--diff-filter=M"] + ([rng] if rng else ["--cached"]) + ["--", path_glob]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    cur, res = None, []
    for l in out.splitlines():
        if l.startswith("+++ b/"):
            cur = l[6:]
        elif l.startswith("+") and not l.startswith("+++"):
            res.append((cur, l[1:]))
    return res


def strip_code(s):
    return re.sub(r"`[^`]*`", "", s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--range", default="")
    a = ap.parse_args()
    stems = set()
    for dp, _, fn in os.walk(os.path.join(ROOT, "wiki")):
        stems |= {f[:-3] for f in fn if f.endswith(".md")}
    errors, in_fm = [], False
    for f, line in added("wiki/skills/*/SKILL.md", a.range):
        if line.strip() == "---":
            continue
        if "short-format:exempt" in line or line.lstrip().startswith(("#", "|", "<!--", "```")):
            continue
        if not RULE.match(line):
            continue
        body = strip_code(line)
        if body.count("**") > 2:
            errors.append(f"{f}: several rules on one line (more than one bold span): {line[:90]}")
        if body.count(";") >= 2:
            errors.append(f"{f}: several rules on one line (two or more ';'): {line[:90]}")
        links = LINK.findall(line)
        if not links:
            errors.append(f"{f}: rule without a [[link]] to its story page: {line[:90]}")
        for l in links:
            if l.strip() not in stems:
                errors.append(f"{f}: [[{l}]] does not exist in wiki/")
    entry = ""
    for _, line in added("wiki/log.md", a.range) + [(None, "## [")]:
        if line.startswith("## [") and entry:
            if len(entry) > 600:
                errors.append(f"log entry over 600 characters ({len(entry)}): {entry[:80]}")
            entry = ""
        if line.startswith("## [") or entry:
            entry += line + "\n" if line != "## [" else ""
    for e in errors:
        print("SHORT-FORMAT:", e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
