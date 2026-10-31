---
type: routine
slug: weekly-hygiene
title: "Weekly hygiene — the trunk (simple mode)"
status: active
last_updated: {{DATE}}
---

# Weekly hygiene — the trunk

> Simple mode replaces the daily arbitration with this weekly cloud run.

1. `sh scripts/wiki_start.sh <owner> routine hygiene`.
2. Review the week's commits: contradictions → settle on a dated source or `## Disputes`; duplicates; frontmatter, links, anchors; no KPI in journals.
3. `python3 scripts/lint_wiki.py --path .` — fix unambiguous issues, list the rest.
4. `python3 scripts/expire_recos.py --path .` and `python3 scripts/rotate_log.py --path .` (both idempotent, every run).
5. Close onboarding gaps that have an answer somewhere in the wiki.
6. Rewrite `hot.md`, log one `arbitration` entry, commit.
7. Digest in `wiki/reports/digests/YYYY-MM-DD.md`: what changed, open disputes, points needing a human.
