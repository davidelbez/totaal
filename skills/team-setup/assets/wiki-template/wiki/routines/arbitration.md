---
type: routine
slug: arbitration
title: "Daily arbitration — the trunk"
status: active
last_updated: {{DATE}}
---

# Daily arbitration — the trunk

> Team mode only. Runs once a day in the cloud, just before the team starts (example: 07:15). It is the **only** run that pushes to `main`. In simple mode, the weekly hygiene routine replaces it.

## What arbitration decides — and what it never decides
- It decides two things only: **inconsistencies in the wiki** and **whether something belongs in the wiki**.
- It never settles business questions and never decides who owns what. It may say "this has no owner".

## Steps
1. **Fetch.** `git fetch origin --prune`. If it fails: write nothing, report, stop.
2. **Log rotation**: `python3 scripts/rotate_log.py --path .` every run (it only moves entries older than the previous month's last week, and is idempotent).
3. **Clean tree.** Assess leftovers of an interrupted run before discarding anything.
4. **Merge every `origin/run/*` and `origin/session/*` branch** into `main`, oldest first, `--no-ff`. Conflicts are resolved by meaning — never `--theirs`/`--ours`, never force-push:
   - two members' blocks on the same account both stay;
   - the same event logged from two mailboxes is deduplicated, keeping the fuller line;
   - cumulative fields are merged by prepending;
   - plugin versions: keep the highest.
   A branch that cannot be merged is listed in the digest with the file and both versions. A direct commit on `main` outside arbitration is reported as an anomaly.
5. **Review the day's commits** (window = since the last commit whose subject starts with `arbitration:`):
   - contradictions → settle on a dated source, or record both under `## Disputes`. Never invent a compromise. Never delete content on the strength of one contribution;
   - someone else's declared status cleared or changed → restore it and tell the person in their next report;
   - the only content arbitration deletes: sensitive HR/legal content about staff, internal company finances, secret values. It cuts the passage, not the commit, and leaves a vague trace in the digest;
   - housekeeping: deduplicate, check frontmatter, `[[links]]`, anchors; no KPI copied into a journal.
6. **Index, log, hot**: every new page is in the index with a one-line summary; one log entry `arbitration`; `hot.md` rewritten if the state changed.
7. **Lint once** at the end: `python3 scripts/lint_wiki.py --path .`. Apply unambiguous fixes; anything needing judgement goes to the digest. A green lint is checked too: confirm it ran with its dependencies (PyYAML).
8. **Bump the changed plugins** once: for each company plugin whose skills changed since the last arbitration, version = highest seen on `main` and every branch + 1; then `python3 scripts/build_plugins.py --out <scratch> --plugins <p>` to prove each one packages. Members receive their personal build in their next morning report.
9. **Commit and push `main`** with plain git (`wiki_commit.sh` refuses `main` by design), as a fast-forward. Never rebase after the merges. Then delete the merged branches and run `sh scripts/wiki_worktree_gc.sh --apply`.
10. **Digest** in `wiki/reports/digests/YYYY-MM-DD.md`: who contributed what, what went where, open disputes, lint state, points that need a human fact or have no owner. Only what changed since yesterday. A point repeated 3 runs in a row moves to `registers/open-work.md`. 800 words max, 300 on an empty day.
