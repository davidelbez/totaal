#!/usr/bin/env python3
"""Health check of the wiki. Writes wiki/reports/lint/lint-YYYY-MM-DD.md.

usage: lint_wiki.py --path ROOT [--stdout] [--stub-words 50] [--hot-max-words 800]
                    [--stale-days 21] [--log-gap-days 30]
Exit 1 if any BLOCK issue, else 0.

Rule: a lint that did not run, or ran without PyYAML, is reported as such —
never as "0 block". A green result is checked too.
"""
import argparse
import datetime
import os
import re
import sys

try:
    import yaml  # optional
except Exception:  # pragma: no cover
    yaml = None

EXCLUDE_TOP = {"index.md", "log.md", "hot.md"}
EXCLUDE_DIRS = ("reports/", "skills/", "plugins/", "log/", "templates/")
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9\-]*\.md$")
MDLINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")


def split_fm(text):
    if not text.startswith("---\n"):
        return None, text, None
    end = text.find("\n---", 4)
    if end == -1:
        return None, text, "unclosed frontmatter"
    return text[4:end], text[end + 4:], None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True)
    ap.add_argument("--stdout", action="store_true")
    ap.add_argument("--stub-words", type=int, default=50)
    ap.add_argument("--hot-max-words", type=int, default=800)
    ap.add_argument("--stale-days", type=int, default=21)
    ap.add_argument("--log-gap-days", type=int, default=30)
    a = ap.parse_args()
    root = os.path.abspath(a.path)
    wiki = os.path.join(root, "wiki")
    today = datetime.date.today()
    block, quality, sugg, notes = [], [], [], []
    if yaml is None:
        notes.append("PyYAML missing: frontmatter parsing was SKIPPED (not '0 issue'). pip install pyyaml")

    pages = {}
    for dp, dn, fn in os.walk(wiki):
        rel_dir = os.path.relpath(dp, wiki).replace("\\", "/") + "/"
        if rel_dir == "./":
            rel_dir = ""
        if any(rel_dir.startswith(x) or x in rel_dir for x in EXCLUDE_DIRS):
            continue
        for f in fn:
            if f.endswith(".md") and not f.startswith("_") and not (rel_dir == "" and f in EXCLUDE_TOP):
                pages[os.path.join(dp, f)] = open(os.path.join(dp, f), encoding="utf-8").read()
    stems = {}
    for p in pages:
        stems.setdefault(os.path.basename(p)[:-3], []).append(p)
    aliases = set()

    inbound = {p: 0 for p in pages}
    for p, text in pages.items():
        rel = os.path.relpath(p, root)
        fm, body, err = split_fm(text)
        if err:
            block.append(f"frontmatter_bad: {rel}: {err}")
        elif fm is not None and yaml is not None:
            try:
                data = yaml.safe_load(fm) or {}
                for k, v in (data.items() if isinstance(data, dict) else []):
                    vals = v if isinstance(v, list) else [v]
                    if any(isinstance(x, dict) and set(x) & {"ROOT", "DRIVE"} for x in vals):
                        block.append(f"frontmatter_bad: {rel}: unquoted anchor in '{k}' (quote values starting with {{)")
                if isinstance(data, dict):
                    for al in data.get("aliases") or []:
                        aliases.add(str(al))
                    slug = data.get("slug")
                    if slug and slug != os.path.basename(p)[:-3] and slug not in (data.get("aliases") or []):
                        quality.append(f"alias_missing: {rel}: slug '{slug}' != filename and not in aliases")
                    if data.get("type") == "account" and data.get("status") not in ("archived", "draft"):
                        for fld in ("last_interaction", "scanned_until"):
                            val = data.get(fld)
                            if not val:
                                quality.append(f"freshness: {rel}: '{fld}' missing")
                            else:
                                try:
                                    d = datetime.date.fromisoformat(str(val))
                                    if (today - d).days > a.stale_days and fld == "scanned_until":
                                        quality.append(f"freshness: {rel}: scanned_until {d} older than {a.stale_days} days — re-sweep, not 'calm'")
                                except ValueError:
                                    quality.append(f"freshness: {rel}: '{fld}' is not a date")
            except Exception as e:
                block.append(f"frontmatter_bad: {rel}: YAML error {str(e).splitlines()[0]}")
        if not SLUG_RE.match(os.path.basename(p)) and not os.path.basename(p).startswith("_"):
            quality.append(f"slug_mismatch: {rel}")
        words = len(re.findall(r"\w+", body))
        if words < a.stub_words and "/registers/" not in p:
            quality.append(f"stub: {rel} ({words} words)")
        for m in MDLINK_RE.finditer(body):
            t = m.group(1)
            if t.startswith(("http", "mailto:", "#")) or "{" in t:
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(p), t.split("#")[0]))
            if not os.path.exists(target):
                block.append(f"broken_link: {rel} -> {t}")
            elif target in inbound:
                inbound[target] += 1
        for m in WIKILINK_RE.finditer(text):
            for tp in stems.get(m.group(1).strip(), []):
                if tp != p:
                    inbound[tp] += 1

    # index, hot
    idx = os.path.join(wiki, "index.md")
    idx_text = open(idx, encoding="utf-8").read() if os.path.exists(idx) else ""
    if not idx_text:
        block.append("index_missing_file: wiki/index.md")
    for m in MDLINK_RE.finditer(idx_text):
        t = m.group(1)
        if not t.startswith("http") and not os.path.exists(os.path.normpath(os.path.join(wiki, t))):
            block.append(f"index_dead: {t}")
    hubs = idx_text
    for extra in ("hot.md",):
        fp = os.path.join(wiki, extra)
        if os.path.exists(fp):
            hubs += open(fp, encoding="utf-8").read()
    for p in pages:
        stem = os.path.basename(p)[:-3]
        relw = os.path.relpath(p, wiki)
        in_index = relw in idx_text or f"[[{stem}]]" in idx_text
        if not in_index:
            quality.append(f"index_missing: {os.path.relpath(p, root)}")
        if inbound[p] == 0 and not in_index and f"[[{stem}]]" not in hubs:
            quality.append(f"orphan: {os.path.relpath(p, root)}")
    hot = os.path.join(wiki, "hot.md")
    if os.path.exists(hot):
        _, hb, _ = split_fm(open(hot, encoding="utf-8").read())
        n = len(hb.split())
        if n > a.hot_max_words:
            block.append(f"hot_oversize: {n} words > {a.hot_max_words}")

    # conflict markers anywhere
    for dp, dn, fn in os.walk(root):
        if "/.git" in dp or dp.endswith(".git"):
            continue
        for f in fn:
            if f.endswith((".md", ".json", ".yaml", ".yml", ".py", ".txt", ".sh")):
                try:
                    for i, line in enumerate(open(os.path.join(dp, f), encoding="utf-8"), 1):
                        if line.startswith(("<<<<<<< ", ">>>>>>> ")):
                            block.append(f"conflict_marker: {os.path.relpath(os.path.join(dp, f), root)}:{i}")
                except UnicodeDecodeError:
                    pass

    # log gaps
    logf = os.path.join(wiki, "log.md")
    if os.path.exists(logf):
        dates = sorted({d for d in re.findall(r"(?m)^## \[(\d{4}-\d{2}-\d{2})\]", open(logf, encoding="utf-8").read())})
        for x, y in zip(dates, dates[1:]):
            gap = (datetime.date.fromisoformat(y) - datetime.date.fromisoformat(x)).days
            if gap > a.log_gap_days:
                sugg.append(f"log_gap: {gap} days between {x} and {y}")

    report = [f"# Lint {today.isoformat()}", "",
              f"Pages checked: {len(pages)} · BLOCK {len(block)} · QUALITY {len(quality)} · SUGGESTION {len(sugg)}", ""]
    for n in notes:
        report.append(f"> {n}")
    for title, items in (("BLOCK", block), ("QUALITY", quality), ("SUGGESTION", sugg)):
        report.append(f"\n## {title}\n")
        report += [f"- {i}" for i in items] or ["- none"]
    out = "\n".join(report) + "\n"
    if a.stdout:
        print(out)
    else:
        d = os.path.join(wiki, "reports", "lint")
        os.makedirs(d, exist_ok=True)
        fp = os.path.join(d, f"lint-{today.isoformat()}.md")
        open(fp, "w", encoding="utf-8").write(out)
        print(f"LINT pages={len(pages)} block={len(block)} quality={len(quality)} suggestion={len(sugg)} -> {os.path.relpath(fp, root)}")
        for n in notes:
            print("NOTE:", n)
    return 1 if block else 0


if __name__ == "__main__":
    sys.exit(main())
