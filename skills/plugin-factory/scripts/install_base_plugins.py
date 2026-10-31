#!/usr/bin/env python3
"""Install base plugins (starters) into a company wiki.

usage: install_base_plugins.py --root ROOT --areas sales,accounts,finance
                               [--matrix '{"Sales": ["sales", "accounts"], "Finance": ["finance"]}']
                               [--list]

For each chosen area: copies its starter skills into wiki/skills/<slug>/ (never
overwrites an existing skill), creates wiki/plugins/<org>-<area>/ (manifest,
skills.list, README with required connectors), and adds rows to the plugin map,
the role -> plugins matrix and the skill catalogue. Replaces {{ORG}}, {{ORG_SLUG}},
{{DATE}} and the ~~category placeholders mapped in .wiki.json.
These are starting points: the evening tuning reshapes them from real use.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STARTERS = os.path.join(os.path.dirname(HERE), "assets", "starters")

KNOWN = ["CRM", "email", "calendar", "chat", "task tracker", "meeting recorder", "ticketing",
         "shared drive", "BI", "product analytics", "email marketing", "e-signature", "accounting"]


def sub_tools(text, tools):
    """Replace ~~category by the company's tool. Longest category wins, so
    ~~email marketing is never turned into '<email tool> marketing'."""
    lower = {k.lower(): v for k, v in (tools or {}).items()}
    cats = sorted(set(c.lower() for c in KNOWN) | set(lower), key=len, reverse=True)
    pat = re.compile(r"~~(" + "|".join(re.escape(c) for c in cats) + r")\b", re.I)
    return pat.sub(lambda m: lower.get(m.group(1).lower(), m.group(0)), text)


def subst(text, cfg):
    text = (text.replace("{{ORG}}", cfg["org"]).replace("{{ORG_SLUG}}", cfg["org_slug"])
                .replace("{{DATE}}", datetime.date.today().isoformat()))
    return sub_tools(text, cfg.get("tools"))


def describe(skill_md, cfg):
    """First sentence of the description + the quoted trigger phrases, for the catalogue."""
    text = open(skill_md, encoding="utf-8").read()
    m = re.search(r"^description: (.*)$", text, re.M)
    d = subst(m.group(1), cfg) if m else ""
    first = d.split(". Use on")[0].split(" — ")[0].strip().rstrip(".")
    trig = ", ".join(re.findall(r'"([^"]+)"', d)[:4])
    return first.replace("|", "/"), trig.replace("|", "/")


def add_row(path, header_marker, row):
    """Add a table row under the section/table that starts at header_marker,
    unless a row with the same first cell already exists in that section."""
    text = open(path, encoding="utf-8").read()
    key = "|" + row.split("|")[1] + "|"
    i = text.find(header_marker)
    section = text[i:] if i != -1 else text
    nxt = section.find("\n## ", 1)
    section = section if nxt == -1 else section[:nxt]
    if any(l.startswith(key) for l in section.split("\n")):
        return
    if i == -1:
        text = text.rstrip("\n") + "\n" + row + "\n"
    else:
        # insert after the table that follows the marker
        lines = text[i:].split("\n")
        n = 0
        for n, l in enumerate(lines):
            if n > 0 and not l.startswith("|") and any(x.startswith("|") for x in lines[:n]):
                break
        else:
            n = len(lines)
        lines.insert(n, row)
        text = text[:i] + "\n".join(lines)
    open(path, "w", encoding="utf-8").write(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--areas", default="")
    ap.add_argument("--matrix", default="{}")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    areas = sorted(os.listdir(STARTERS))
    if a.list:
        for ar in areas:
            meta = json.load(open(os.path.join(STARTERS, ar, "area.json")))
            print(f"{ar:12s} {meta['title']:20s} roles: {meta['roles']} · skills: {', '.join(meta['skills'])}")
        return 0
    if not a.root:
        ap.error("--root is required")
    cfg = json.load(open(os.path.join(a.root, ".wiki.json"), encoding="utf-8"))
    org = cfg["org_slug"]
    plugins_dir = os.path.join(a.root, "wiki", "plugins")
    taken = {}
    for p in os.listdir(plugins_dir):
        lst = os.path.join(plugins_dir, p, "skills.list")
        if os.path.isfile(lst):
            for l in open(lst, encoding="utf-8"):
                if l.strip() and not l.startswith("#"):
                    taken[l.strip()] = p
    for ar in filter(None, a.areas.split(",")):
        if ar not in areas:
            print(f"unknown area '{ar}' (see --list)", file=sys.stderr)
            return 2
        meta = json.load(open(os.path.join(STARTERS, ar, "area.json")))
        pname = f"{org}-{ar}"
        pdir = os.path.join(plugins_dir, pname)
        os.makedirs(os.path.join(pdir, ".claude-plugin"), exist_ok=True)
        mf = os.path.join(pdir, ".claude-plugin", "plugin.json")
        if not os.path.exists(mf):
            json.dump({"name": pname, "version": "0.1.0", "description": subst(meta["description"], cfg),
                       "author": {"name": cfg["org"]}}, open(mf, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        slugs = []
        for s in meta["skills"]:
            if s in taken and taken[s] != pname:
                print(f"SKIP {s}: already in plugin {taken[s]} (one slug, one plugin)")
                continue
            dst = os.path.join(a.root, "wiki", "skills", s)
            if os.path.exists(dst):
                print(f"KEEP {s}: wiki/skills/{s} exists, not overwritten")
            else:
                shutil.copytree(os.path.join(STARTERS, ar, "skills", s), dst)
                for dp, _, fn in os.walk(dst):
                    for f in fn:
                        fp = os.path.join(dp, f)
                        content = open(fp, encoding="utf-8").read()
                        open(fp, "w", encoding="utf-8").write(subst(content, cfg))
                print(f"ADD  {s} -> {pname}")
            slugs.append(s)
            what, triggers = describe(os.path.join(STARTERS, ar, "skills", s, "SKILL.md"), cfg)
            add_row(os.path.join(a.root, "wiki", "skills", "index.md"), "| Skill |",
                    f"| {s} | {what} | {pname} | {meta['roles']} | {triggers} | lead | {datetime.date.today().isoformat()} |")
        lst = os.path.join(pdir, "skills.list")
        cur = [l.strip() for l in open(lst, encoding="utf-8")] if os.path.exists(lst) else ["# Skills bundled by this plugin — source = wiki/skills/<slug>/"]
        for s in slugs:
            if s not in cur:
                cur.append(s)
        open(lst, "w", encoding="utf-8").write("\n".join(cur) + "\n")
        readme = os.path.join(pdir, "README.md")
        if not os.path.exists(readme):
            open(readme, "w", encoding="utf-8").write(
                f"# {cfg['org']} {meta['title'].lower()}\n\nBase plugin installed by Totaal on {datetime.date.today().isoformat()}, "
                f"then reshaped by use (evening tuning). Requires `{org}-core`.\n\n## For\n{meta['roles']}\n\n"
                f"## Required connectors\n{subst(meta['connectors'], cfg)}\n")
        add_row(os.path.join(plugins_dir, "index.md"), "## Plugin map",
                f"| {pname} | {meta['title']} | {', '.join(slugs)} | {meta['roles']} | {subst(meta['connectors'], cfg)} |")
    matrix = json.loads(a.matrix)
    mapped = {x for v in matrix.values() for x in v}
    for ar in filter(None, a.areas.split(",")):
        if matrix and ar not in mapped:
            print(f"NOTE: area '{ar}' is installed but no role gets it by default — add it to the matrix or to someone's preferences")
    for role, ars in matrix.items():
        plist = ", ".join([f"{org}-core"] + [f"{org}-{x}" for x in ars])
        add_row(os.path.join(plugins_dir, "index.md"), "## Role", f"| {role} | {plist} |")
    print("done — run scripts/sync_plugin_skills.py, then commit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
