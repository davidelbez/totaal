#!/usr/bin/env python3
"""Install the company wiki from the template into a (cloned, empty or new) repository.

usage: init_wiki.py --target DIR --org "Company" --repo owner/name --mode team|simple
                    [--tools '{"CRM":"Pipedrive","email":"Gmail"}'] [--main main] [--force]

Idempotent: never overwrites an existing file unless --force. Replaces {{ORG}},
{{ORG_SLUG}}, {{DATE}}, {{MODE}}, {{REPO}}, {{MODE_RULE}} and, when --tools is given,
the ~~category placeholders (e.g. ~~CRM -> Pipedrive). Writes .wiki.json.
Prints every file created and the list of ~~placeholders left to fill.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import sys
import unicodedata

KNOWN = ["CRM", "email", "calendar", "chat", "task tracker", "meeting recorder", "ticketing",
         "shared drive", "BI", "product analytics", "email marketing", "e-signature", "accounting"]


def sub_tools(text, tools):
    """Replace ~~category by the company's tool. Longest category wins, so
    ~~email marketing is never turned into '<email tool> marketing'."""
    lower = {k.lower(): v for k, v in (tools or {}).items()}
    cats = sorted(set(c.lower() for c in KNOWN) | set(lower), key=len, reverse=True)
    pat = re.compile(r"~~(" + "|".join(re.escape(c) for c in cats) + r")\b", re.I)
    return pat.sub(lambda m: lower.get(m.group(1).lower(), m.group(0)), text)
HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(os.path.dirname(HERE), "assets", "wiki-template")

MODE_RULE = {
    "team": "Team mode: each run writes on its own branch and pushes it; **nobody pushes to `main`** — the daily arbitration merges.",
    "simple": "Simple mode: everyone commits on `main`; the commit script rebases before pushing. Reconcile any conflict by meaning.",
}


def slugify(s):
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--org", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--mode", choices=["team", "simple"], default="team")
    ap.add_argument("--tools", default="{}")
    ap.add_argument("--main", default="main")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    tools = json.loads(a.tools)
    org_slug = slugify(a.org)
    subs = {
        "{{ORG}}": a.org, "{{ORG_SLUG}}": org_slug, "{{DATE}}": datetime.date.today().isoformat(),
        "{{MODE}}": a.mode, "{{REPO}}": a.repo, "{{MODE_RULE}}": MODE_RULE[a.mode],
    }
    created, skipped, left = [], [], set()
    for dp, dn, fn in os.walk(TEMPLATE):
        rel_dir = os.path.relpath(dp, TEMPLATE)
        out_dir = os.path.join(a.target, *[subs.get(x, x) for x in rel_dir.replace("{{ORG_SLUG}}", org_slug).split(os.sep)]) if rel_dir != "." else a.target
        os.makedirs(out_dir, exist_ok=True)
        for f in fn:
            src, dst = os.path.join(dp, f), os.path.join(out_dir, f)
            if os.path.exists(dst) and not a.force:
                skipped.append(os.path.relpath(dst, a.target))
                continue
            try:
                text = open(src, encoding="utf-8").read()
            except UnicodeDecodeError:
                shutil.copy2(src, dst)
                continue
            for k, v in subs.items():
                text = text.replace(k, v)
            text = sub_tools(text, tools)
            left |= {c for c in KNOWN if re.search(r"~~" + re.escape(c) + r"\b", text, re.I)}
            open(dst, "w", encoding="utf-8").write(text)
            if f.endswith((".sh", ".py")):
                os.chmod(dst, 0o755)
            created.append(os.path.relpath(dst, a.target))
    cfg = os.path.join(a.target, ".wiki.json")
    if not os.path.exists(cfg) or a.force:
        json.dump({"org": a.org, "org_slug": org_slug, "repo": a.repo, "mode": a.mode,
                   "main_branch": a.main, "tools": tools,
                   "installed": subs["{{DATE}}"], "method": "totaal"},
                  open(cfg, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        created.append(".wiki.json")
    print(f"CREATED {len(created)} file(s), SKIPPED {len(skipped)} existing")
    for s in skipped[:20]:
        print("  kept:", s)
    if left:
        print("PLACEHOLDERS LEFT (map them with --tools or edit the pages):", ", ".join("~~" + x for x in sorted(left)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
