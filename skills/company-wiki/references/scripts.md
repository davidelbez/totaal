# Wiki scripts — usage and exit codes

All scripts live in the wiki repository under `scripts/`. Run them from `ROOT` (the directory `wiki_start.sh` printed). Python 3 standard library; PyYAML optional but needed for frontmatter checks.

| Script | Usage | Notes |
|---|---|---|
| `wiki_start.sh` | `sh scripts/wiki_start.sh <member> [routine\|session] [slug]` | Fetch, fast-forward main, branch + working tree (team mode), sync company plugin skills, state lines, CONTEXT block. Last lines: `ROOT=` and `BRANCH=`. Prints `BASE STALE` when the tree misses commits of main: never package plugins from it. |
| `wiki_commit.sh` | `sh scripts/wiki_commit.sh [--branch b] "msg" "body" file…` | Targeted add (never `-A`), lock, short-format check, commit, push, verify. Exit 3 = on main in team mode · 9 = wrong branch · 4 = no files · 5 = lock busy · 6 = add failed · 10 = short-format check failed · 7 = commit or rebase failed · 8 = push not verified. Last line `DELIVERED=<branch> <sha>`. |
| `wiki_context.sh` | `sh scripts/wiki_context.sh <ROOT> [account…]` | The CONTEXT block alone. |
| `update_index.py` | `--path ROOT --category C --title T --page-path wiki/… [--summary S]` | Upsert by (category, title). Never chain it with `&&` before a commit. |
| `append_log.py` | `--path ROOT --action A --title T [--details D]` | Inserts at the top. Actions: ingest, query, lint, bootstrap, schema-evolve, note, update, audit, setup, restructure, decision, arbitration, routine, onboarding, skill_update_needed, skill_update_processed, tuning, review. |
| `lint_wiki.py` | `--path ROOT [--stdout]` | Exit 1 on any BLOCK. Report in `wiki/reports/lint/`. |
| `journal_guard.py` | `--journal F --line "…"` or `--stdin` | Never writes. 0 clean · 1 same fact already logged · 2 the line asserts an absence or reopens a resolved item while the fact exists · 3 journal missing (not "no collision"). |
| `expire_recos.py` | `--path ROOT [--days 14] [--dry-run]` | Archives undecided recommendations. Not rejections. |
| `rotate_log.py` | `--path ROOT [--dry-run]` | Every arbitration or hygiene run (idempotent). Refuses to write if entries would be lost. |
| `sync_plugin_skills.py` | (no args) | Projects `wiki/skills/<slug>` into `wiki/plugins/<p>/skills/`. One slug per plugin, enforced. |
| `build_plugins.py` | `--out DIR --from-prefs <member>` · or `--out DIR --plugins p [--set-version p=X.Y.Z] [--bump p] [--member m] [--drop p:skill]` | `--from-prefs` builds one employee's personal version (any session may run it). Version bumps: once a day only (tuning in simple mode, arbitration in team mode); commit the bump before building. Validates every package and deletes a bad one; writes BUILD.json (commit, member, removed skills). |
| `check_short_format.py` | `[--range A..B]` | Called by `wiki_commit.sh`. Added skill lines: one rule per line, each with an existing `[[link]]`; new log entries ≤600 characters. Escape: `<!-- short-format:exempt -->` + justification in the commit body. |
| `wiki_worktree_gc.sh` | `[--apply]` | Removes merged, clean working trees. Dry run by default. |
