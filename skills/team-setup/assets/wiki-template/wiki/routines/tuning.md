---
type: routine
slug: tuning
title: "Evening tuning — the trunk"
status: active
last_updated: {{DATE}}
---

# Evening tuning — the trunk

> The improvement loop. Runs on weekdays, early evening (example: 18:12), one per member or one for the team. It turns the day's sessions and corrections into skill patches and routine changes, and gets the company plugins ready to ship. Everyone receives the updated personal build in their next morning report.

## Step 0 — Continuity
Compare the task's last run with the last `tuning` log entry. A run that left no trace has four usual causes: machine asleep (local tasks), killed at dispatch, account quota hit, limit on concurrent scheduled tasks. Widen the window to every missed day.

## Step 1 — Read the sessions, in two stages
1. **Stage 1 (cheap)**: list the day's sessions with the member's turns verbatim, using the session-history tools available to this run (past-conversation search, session transcripts on the member's computer), plus the log's entries and digests. Flag heavy sessions. A run that cannot read sessions says so and works from the log and digests — never as "no signal".
2. **Stage 2 (fine reading)**: a read-only sub-agent reads the flagged sessions in full — user turns, one line per tool call, tool errors in full — and returns at most 20 lines of signals. Stage 2 is never skipped; a skipped fine reading is never summarised as "no patch".
- Cover the **work done**, not only the skills invoked: for each session, which system was touched, and does that know-how have a home? If not, propose a new skill.
- Every tool error gets a verdict: patched · recurrence · noise · no home. Verdict count = error count.
- Every "I can't", "no access", "there is no" in a transcript is a patch candidate (see the tool ladder).

## Step 2 — Skills
Signals: (1) explicit user correction or a path Claude did not try; (2) a question whose answer is stable → hard-code it; (3) a coverage gap; (4) a tool used but undocumented; (5) a description too long or carrying rules; (6) **recurrence of a rule already written** → diagnose placement before adding text (skill not loaded? rule only in personal memory? buried in prose? no reread step?).
Also process every unprocessed `skill_update_needed` log entry, then log `skill_update_processed`.
Classes:
- **Minor** (example, word, trigger, tool, typo, shorter description keeping every trigger) → apply.
- **Catch-up / meta** (propagating a decision already taken and documented — cite it; fixing the tuning machinery itself) → apply, even unattended.
- **Structural** (changed decision rule, rewritten section, scope change, split/merge, removed trigger, new always/never) → into the report with the raw diff, and into `registers/structural-debt.md`.
Each patch = the four boxes: (1) story in a dated page; (2) that page linked from the domain summary's "What we know"; (3) one line in the skill = one rule + `[[link]]`; (4) a log entry ≤600 characters. `scripts/check_short_format.py` blocks the commit otherwise.

## Step 3 — Package
- **Simple mode** (everything is on `main`): for each company plugin whose skills changed, bump to the highest version seen + 1 (`build_plugins.py --set-version <p>=<v>`), commit the bump, then build each changed plugin once into a scratch folder to prove it packages (the script deletes a bad package).
- **Team mode**: the day's patches are still on their branches, so do not bump here. List the changed plugins in the report; the daily arbitration bumps them after it merges.
- Never package from a stale base (`BASE STALE`).
- Delivery to each employee is not done here: their own morning routine builds their personal version from `main` and presents it (morning step 7). One number always means one content.

## Step 4 — Routines
- Propose trunk changes as diffs. Check each scheduled task is still a **pointer**, not a frozen copy; if a task cannot be edited from here, give the exact prompt text to paste.

## Step 5 — Environment
- Compare each member's installed plugins (enabled?), connectors and tasks with the targets (target version = the version in `wiki/plugins/<p>/.claude-plugin/plugin.json` on `main`; for Totaal itself, the version the lead installed). List what teammates shipped that this member has not adopted, measured from their **last adopted** build, never from a version number.

## Step 6 — Close
- Exit guard: no stray standalone skill files; in simple mode every changed plugin was bumped and packages cleanly.
- Commit (on the run branch in team mode, on `main` in simple mode).
- **What could this run have done better?** A point that repeats becomes a patch to this page.
- Short report: at most 3 decisions waiting, at most 5 alerts, one line per area. **No account topics in the tuning report** — they go to the account journal for tomorrow's morning run.
