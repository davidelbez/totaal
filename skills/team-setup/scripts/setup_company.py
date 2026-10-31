#!/usr/bin/env python3
"""One-command setup of a company, after the interview.

usage: setup_company.py --target <clone> --org "Company" --repo owner/name --mode simple|team
                        --areas sales,accounts,finance
                        --matrix '{"Founder": ["leadership", "sales"], "Finance": ["finance"]}'
                        --lead <first-name> --lead-role Founder
                        [--tools '{"CRM": "HubSpot", "email": "Outlook"}'] [--out <dir>]

Runs, in order, and stops at the first error with a plain message:
  0. preflight.py            — stops early on anything that would block (access, identity, tools)
  1. init_wiki.py            — the wiki, scripts and constitution (keeps the repository's default branch)
  2. install_base_plugins.py — the chosen base plugins + role matrix
  3. sync_plugin_skills.py   — projects skills into the plugins
  4. the lead's preferences page (plugins from their role)
  5. build_plugins.py --from-prefs <lead> — the lead's first personal build
Idempotent: re-running never overwrites existing pages or skills.
It does not commit or push: Claude reviews, then makes the bootstrap commit.
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN_SKILLS = os.path.dirname(os.path.dirname(HERE))


def run(step, cmd):
    print(f"\n== {step}")
    r = subprocess.run(cmd)
    if r.returncode:
        print(f"\nSTOPPED at: {step}. Nothing after this step was done. Fix the message above, then run the same command again (it is safe to re-run).")
        sys.exit(r.returncode)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--org", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--mode", choices=["simple", "team"], required=True)
    ap.add_argument("--areas", default="")
    ap.add_argument("--matrix", default="{}")
    ap.add_argument("--lead", required=True)
    ap.add_argument("--lead-role", default="")
    ap.add_argument("--tools", default="{}")
    ap.add_argument("--out", default="")
    ap.add_argument("--skip-preflight", action="store_true")
    a = ap.parse_args()
    try:
        matrix = json.loads(a.matrix)
        json.loads(a.tools)
    except json.JSONDecodeError as e:
        print(f"--matrix or --tools is not valid JSON: {e}")
        return 2
    py = sys.executable
    if not a.skip_preflight:
        run("0/5 Pre-flight check", [py, os.path.join(HERE, "preflight.py"), "--clone", a.target])
    # default branch: keep the repository's own (main or master); create main in an empty repository
    heads = subprocess.run(["git", "-C", a.target, "ls-remote", "--heads", "origin"], capture_output=True, text=True).stdout
    names = [l.split("refs/heads/")[-1] for l in heads.splitlines() if "refs/heads/" in l]
    main_branch = "main" if (not names or "main" in names) else ("master" if "master" in names else names[0])
    if not names:
        subprocess.run(["git", "-C", a.target, "checkout", "-q", "-b", "main"], capture_output=True)
    print(f"main branch: {main_branch}")
    run("1/5 Install the company wiki", [py, os.path.join(HERE, "init_wiki.py"), "--target", a.target, "--org", a.org,
                                         "--repo", a.repo, "--mode", a.mode, "--tools", a.tools, "--main", main_branch])
    if a.areas:
        run("2/5 Install the base plugins", [py, os.path.join(PLUGIN_SKILLS, "plugin-factory", "scripts", "install_base_plugins.py"),
                                             "--root", a.target, "--areas", a.areas, "--matrix", a.matrix])
    else:
        print("\n== 2/5 No base plugin chosen — only the core plugin is installed")
    run("3/5 Project skills into plugins", [py, os.path.join(a.target, "scripts", "sync_plugin_skills.py")])

    print("\n== 4/5 Lead's preferences page")
    cfg = json.load(open(os.path.join(a.target, ".wiki.json")))
    org = cfg["org_slug"]
    import unicodedata
    lead = re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFD", a.lead).encode("ascii", "ignore").decode().lower()).strip("-")
    plugins = [f"{org}-core"] + [f"{org}-{x}" for x in matrix.get(a.lead_role, [])]
    pref = os.path.join(a.target, "wiki", "preferences", f"{lead}.md")
    if os.path.exists(pref):
        print(f"kept existing wiki/preferences/{lead}.md")
    else:
        t = open(os.path.join(a.target, "wiki", "preferences", "_template.md"), encoding="utf-8").read()
        t = t.replace("<name>", lead)
        t = re.sub(r"^plugins: \[.*\]$", f"plugins: [{', '.join(plugins)}]", t, flags=re.M)
        open(pref, "w", encoding="utf-8").write(t)
        print(f"created wiki/preferences/{lead}.md with plugins: {plugins}")

    out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.target)), "plugin-builds")
    run("5/5 Lead's first personal build", [py, os.path.join(a.target, "scripts", "build_plugins.py"), "--out", out, "--from-prefs", lead])
    print(f"""
DONE. Next, in this order:
  - review the created pages, then make the bootstrap commit on the main branch (git add -A; git commit; git push -u origin HEAD);
  - present the lead's .plugin files from {os.path.join(out, lead)} and ask them to install and enable each one;
  - add each teammate to the GitHub repository, then onboard them ("start my onboarding").""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
