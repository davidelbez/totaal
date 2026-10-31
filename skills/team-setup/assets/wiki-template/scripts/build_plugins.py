#!/usr/bin/env python3
"""Build installable .plugin packages of the company's own plugins.

usage:
  build_plugins.py --out DIR --from-prefs <member>
      One employee's personal build: the plugins listed in wiki/preferences/<member>.md
      (frontmatter `plugins: [...]`) minus `removed_skills: [plugin:skill, ...]`.
      Written to DIR/<member>/. Any session may run it. Add --plugins a,b to build only
      those (e.g. the ones whose version changed), so people install fewer files.
  build_plugins.py --out DIR --plugins a,b [--set-version a=X.Y.Z] [--bump a] [--member m] [--drop a:skill]
      Reference builds. Version changes happen once a day only (evening tuning in
      simple mode, daily arbitration in team mode): new version = highest version
      seen on main and on every run/session branch + 1. Commit the bump BEFORE
      building, so BUILD.json names a commit that holds exactly what was packaged.

Everything is validated before anything is built. Post-checks (a failed package is
deleted): size > 0, zip integrity, manifest at the zip root, projected skills ==
skills.list minus removed skills. Each package carries BUILD.json (commit, dirty
flag, date, member, removed skills). Never package from a stale base.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDIR = os.path.join(ROOT, "wiki", "plugins")


def slug(s):
    import unicodedata
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def fail(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    return 1


def bump(v):
    parts = [int(x) for x in v.split(".")]
    parts[-1] += 1
    return ".".join(map(str, parts))


def read_prefs(member):
    f = os.path.join(ROOT, "wiki", "preferences", f"{member}.md")
    if not os.path.exists(f):
        raise ValueError(f"wiki/preferences/{member}.md not found")
    text = open(f, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    fm = m.group(1) if m else ""
    data = {}
    try:
        import yaml
        data = yaml.safe_load(fm) or {}
    except ImportError:
        for key in ("plugins", "removed_skills"):
            mm = re.search(rf"^{key}:\s*\[(.*?)\]", fm, re.M)
            data[key] = [x.strip().strip("'\"") for x in mm.group(1).split(",") if x.strip()] if mm else []
    except Exception as e:
        raise ValueError(f"preferences frontmatter is not valid YAML: {e}")
    return list(data.get("plugins") or []), list(data.get("removed_skills") or [])


def skills_of(p):
    lst = os.path.join(PDIR, p, "skills.list")
    return [l.strip() for l in open(lst, encoding="utf-8") if l.strip() and not l.lstrip().startswith("#")]


def git(*args):
    try:
        return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--plugins", default="")
    ap.add_argument("--from-prefs", default="")
    ap.add_argument("--bump", default="")
    ap.add_argument("--set-version", default="", help="p=X.Y.Z,q=X.Y.Z")
    ap.add_argument("--member", default="")
    ap.add_argument("--drop", default="")
    a = ap.parse_args()

    member = slug(a.from_prefs or a.member)
    if a.from_prefs:
        try:
            plugs, removed = read_prefs(member)
        except ValueError as e:
            return fail(str(e))
        if not plugs:
            return fail(f"no `plugins: [...]` in wiki/preferences/{member}.md — set it from the role matrix (wiki/plugins/index.md)")
        if a.plugins:  # narrow to the plugins that changed, e.g. for the morning report
            only = {x.strip() for x in a.plugins.split(",") if x.strip()}
            plugs = [p for p in plugs if p in only]
            if not plugs:
                print("nothing to build: none of the requested plugins is in this person's plugins")
                return 0
        a.plugins, a.drop = ",".join(plugs), ",".join(removed)
        a.out = os.path.join(a.out, member)
    if not a.plugins:
        ap.error("--plugins or --from-prefs is required")

    # ---- validate everything before building anything
    plugins = [p.strip() for p in a.plugins.split(",") if p.strip()]
    available = sorted(d for d in os.listdir(PDIR) if os.path.isfile(os.path.join(PDIR, d, "skills.list")))
    unknown = [p for p in plugins if p not in available]
    if unknown:
        return fail(f"unknown plugin(s) {unknown}. Available: {available}")
    drops = {}
    for d in filter(None, (x.strip() for x in a.drop.split(","))):
        if ":" not in d:
            return fail(f"removed skill '{d}' must be written plugin:skill (e.g. {plugins[0]}:{d})")
        p, s = d.split(":", 1)
        if p not in available or s not in skills_of(p):
            print(f"WARNING: removed skill '{d}' does not exist (typo?) — ignored")
            continue
        drops.setdefault(p, set()).add(s)
    try:
        setv = dict(x.split("=") for x in a.set_version.split(",") if x)
    except ValueError:
        return fail("--set-version expects p=X.Y.Z[,q=X.Y.Z]")

    for p in sorted(set(filter(None, a.bump.split(","))) | set(setv)):
        if p not in available:
            return fail(f"cannot bump unknown plugin {p}")
        mf = os.path.join(PDIR, p, ".claude-plugin", "plugin.json")
        data = json.load(open(mf, encoding="utf-8"))
        data["version"] = setv.get(p) or bump(data.get("version", "0.1.0"))
        json.dump(data, open(mf, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"version {p} -> {data['version']}  (commit this bump before handing out the packages)")

    if subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "sync_plugin_skills.py")]).returncode:
        return fail("sync failed — no package built")

    commit = git("rev-parse", "HEAD") or "unknown"
    dirty = bool(git("status", "--porcelain", "--untracked-files=no", "--", "wiki/skills", "wiki/plugins"))
    if dirty:
        print("WARNING: uncommitted changes in wiki/skills or wiki/plugins — BUILD.json will say dirty: true")

    os.makedirs(a.out, exist_ok=True)
    failed = 0
    for p in plugins:
        src = os.path.join(PDIR, p)
        expected = [s for s in skills_of(p) if s not in drops.get(p, set())]
        missing = [s for s in expected if not os.path.isdir(os.path.join(src, "skills", s))]
        if missing:
            print(f"KO {p}: skills missing in projection: {missing}")
            failed += 1
            continue
        stage = tempfile.mkdtemp()
        shutil.copytree(os.path.join(src, ".claude-plugin"), os.path.join(stage, ".claude-plugin"))
        for extra in ("README.md", "CONNECTORS.md", "agents", "hooks", "commands"):
            s = os.path.join(src, extra)
            if os.path.isdir(s):
                shutil.copytree(s, os.path.join(stage, extra))
            elif os.path.isfile(s):
                shutil.copy2(s, stage)
        for s in expected:
            shutil.copytree(os.path.join(src, "skills", s), os.path.join(stage, "skills", s))
        json.dump({"commit": commit, "dirty": dirty, "built": datetime.datetime.now().isoformat(timespec="seconds"),
                   "member": member or None, "removed_skills": sorted(drops.get(p, []))},
                  open(os.path.join(stage, "BUILD.json"), "w"), indent=2)
        if member:
            open(os.path.join(stage, "MEMBER-PREFS.md"), "w").write(
                f"# Personal build\n\nmember: {member}\nplugin: {p}\nremoved skills: {sorted(drops.get(p, []))}\n"
                f"source: wiki/preferences/{member}.md — never edit this installed copy; change the preferences page.\n")
        target = os.path.join(a.out, f"{p}.plugin")
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
            for dp, _, fn in os.walk(stage):
                for f in fn:
                    if f != ".DS_Store":
                        full = os.path.join(dp, f)
                        z.write(full, os.path.relpath(full, stage))
        shutil.rmtree(stage)
        ok = os.path.getsize(target) > 0
        with zipfile.ZipFile(target) as z:
            names = z.namelist()
            ok = ok and z.testzip() is None and ".claude-plugin/plugin.json" in names
            got = {n.split("/")[1] for n in names if n.startswith("skills/")}
            ok = ok and got == set(expected)
        version = json.load(open(os.path.join(src, ".claude-plugin", "plugin.json"))).get("version", "?")
        if ok:
            print(f"OK {target} (v{version}, {len(expected)} skills)")
        else:
            os.remove(target)
            print(f"KO {p}: post-checks failed, package deleted")
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
