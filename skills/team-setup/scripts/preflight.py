#!/usr/bin/env python3
"""Pre-flight check before installing Totaal, or before onboarding a member.

usage: preflight.py [--clone <path to the cloned wiki repository>]

Prints one line per check — OK, NOTE or FIX — with the fix in plain words,
and exits 1 if anything must be fixed first. Safe: it changes nothing.
"""
import argparse
import os
import shutil
import subprocess
import sys

problems = 0


def say(kind, msg):
    global problems
    if kind == "FIX":
        problems += 1
    print(f"{kind:4s} {msg}")


def git(clone, *args):
    r = subprocess.run(["git", "-C", clone, *args], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clone", default="")
    a = ap.parse_args()

    v = sys.version_info
    say("OK" if v >= (3, 8) else "FIX", f"Python {v.major}.{v.minor}" + ("" if v >= (3, 8) else " — Python 3.8 or newer is needed"))
    say("OK" if shutil.which("git") else "FIX", "git is installed" if shutil.which("git") else "git is missing — install git")
    say("OK" if shutil.which("sh") else "FIX", "a POSIX shell is available" if shutil.which("sh") else "no POSIX shell — run Totaal from a cloud session, not from a Windows terminal")
    try:
        import yaml  # noqa: F401
        say("OK", "PyYAML is installed (frontmatter checks will run)")
    except ImportError:
        say("NOTE", "PyYAML missing — the lint will skip frontmatter checks. Install: pip install pyyaml (add --break-system-packages in a managed environment)")

    if not a.clone:
        say("NOTE", "no --clone given: repository checks skipped")
        return 1 if problems else 0
    c = os.path.abspath(a.clone)
    if not os.path.isdir(os.path.join(c, ".git")) and not os.path.isfile(os.path.join(c, ".git")):
        say("FIX", f"{c} is not a git clone — attach the wiki repository with push access, then clone it")
        return 1
    code, out = git(c, "remote", "get-url", "origin")
    say("OK" if code == 0 else "FIX", f"remote origin: {out}" if code == 0 else "no remote 'origin' — clone the repository instead of creating a folder")
    code, out = git(c, "ls-remote", "--heads", "origin")
    if code != 0:
        detail = out.splitlines()[-1][:160] if out else "no detail"
        say("FIX", "cannot read the repository on GitHub — the repository is not attached, the invitation was not accepted, or Claude's GitHub app is not installed for it. Detail: " + detail)
    else:
        heads = [l.split("refs/heads/")[-1] for l in out.splitlines() if "refs/heads/" in l]
        if not heads:
            say("NOTE", "the repository is EMPTY — setup will create the main branch")
        else:
            code2, head = git(c, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
            default = head.split("/", 1)[-1] if code2 == 0 else ("main" if "main" in heads else heads[0])
            say("OK" if default == "main" else "NOTE", f"default branch: {default}" + ("" if default == "main" else " — setup will use it (recorded in .wiki.json)"))
    name = git(c, "config", "user.name")[1]
    email = git(c, "config", "user.email")[1]
    if name and email:
        say("OK", f"git identity: {name} <{email}>")
    else:
        say("FIX", "git does not know who commits — run in the clone: git config user.name \"<Name>\" && git config user.email \"<email>\" (the person's own)")
    code, out = git(c, "rev-parse", "HEAD")
    if code == 0:
        code, out = git(c, "push", "--dry-run", "origin", "HEAD:refs/heads/preflight-write-check")
        say("OK" if code == 0 else "FIX", "write access to the repository" if code == 0 else "no write access — give this person the Write role on the repository. Detail: " + (out.splitlines()[-1][:160] if out else ""))
    else:
        say("NOTE", "no commit yet: write access will be proven by the bootstrap push")
    for f in ("CLAUDE.md", "wiki/index.md"):
        if os.path.exists(os.path.join(c, f)):
            say("NOTE", f"{f} already exists — setup keeps it and never overwrites; merge by hand if it is not a Totaal wiki")
    dirty = git(c, "status", "--porcelain")[1]
    if dirty:
        say("NOTE", f"{len(dirty.splitlines())} uncommitted change(s) in the clone — commit or set them aside before setup")
    print("\nRESULT:", "ready" if not problems else f"{problems} thing(s) to fix first (lines marked FIX)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
