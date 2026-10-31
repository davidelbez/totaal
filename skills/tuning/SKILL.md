---
name: tuning
description: The self-improvement loop — turns user corrections and the day's sessions into skill patches, routine changes and updated company plugins, so a correction never has to be given twice. Use on an explicit correction ("no, that's not it", "I already told you", "wrong again"), on "tune the skills", "run the evening tuning", "update the plugin", "why does Claude keep doing this", and when the scheduled tuning fires.
---

# Tuning — never make the same mistake twice

Every correction a person gives is the most valuable signal the system receives. Tuning captures it in the right place, ships it in the next daily build, and checks it is not broken again. The scheduled version executes `wiki/routines/tuning.md` (the trunk); this skill is the method behind it and the inline mode.

## Mode 1 — Inline, on a correction (right now)
Trigger: the person corrects Claude ("no", "that's not what I said", "I already told you X", or points to a path Claude did not try).
1. Fix the work first.
2. Find the one skill (or routine trunk) that should have prevented it.
3. Apply **one** patch with the four boxes (below), commit, log it.
4. Say in one line where the rule now lives.
If the rule already existed, this is **signal 6** — see placement below.

## Mode 2 — The evening run
Execute `wiki/routines/tuning.md`. The essentials it encodes:
- **Read the raw sessions, not the log** — the log is a summary of a summary. Stage 1 lists sessions and the person's verbatim turns; stage 2 has a read-only sub-agent read the flagged sessions in full and return at most 20 lines of signals. Never skip stage 2; never summarise a skipped reading as "no patch".
- **Cover the work, not only the skills invoked.** Which system was touched in each session, and does that know-how have a home? If not, propose a new skill (load `skill-writer`).
- **Every tool error gets a verdict**: patched · recurrence · noise · no home. Every "I can't" or "no access" is a patch candidate: was the tool ladder walked?
- Process every unprocessed `skill_update_needed` entry, then log `skill_update_processed`.

## Signals
1. Explicit correction, or a path Claude did not try.
2. A question Claude asked whose answer is stable → hard-code the answer.
3. A coverage gap.
4. A tool or connector used but not documented in the skill.
5. A description that is too long or carries rules.
6. **A rule already written, broken again.** Diagnose placement before adding text: the rule is in a skill that was not loaded (move it, or add a pointer where it is needed) · it lives only in someone's personal memory (bring it into the shared skill) · it is buried in prose (promote it) · it is well placed but no step rereads it (patch the routine). Count full reads of very large pages as recurrence too.

## Classes
- **Minor** (example, word, trigger, tool name, typo, shorter description keeping every trigger) → apply.
- **Catch-up / meta** (propagating a decision already taken and documented — cite it; fixing the tuning machinery itself) → apply, even unattended. Without this class, a fix to the tuner waits for a validation that never comes and the loop closes on itself.
- **Structural** (changed decision rule, rewritten section, reordered workflow, scope change, split or merge, removed trigger, new always/never) → the person validates, one question at a time with the raw diff. Unattended runs never ask: the item goes to the report and to `registers/structural-debt.md`.

## A patch = the four boxes
1. The story in a dated wiki page.
2. That page linked from its domain summary's "What we know".
3. One line in the skill: one rule + `[[link]]`, with a dated marker comment in the body (e.g. `<!-- PATCH-<topic>-<date> -->`), never in the frontmatter.
4. A log entry: title + link, ≤600 characters.
`scripts/check_short_format.py` (run by `wiki_commit.sh`) blocks the commit otherwise.

## Shipping
- Sessions and routines never bump versions; they log `skill_update_needed`.
- Versions are bumped once a day, on `main` only: by the evening tuning in simple mode, by the daily arbitration in team mode (right after it merges the day's branches, so every patch of the day is in). Each employee receives their personal build through **their own morning routine** (step 7), which builds it from `main` and presents the files in the report.
- New version = highest version seen for that plugin on `main` and on every `origin/run/*` and `origin/session/*` branch, + 1. One number always means one content.
- Never package from a stale base (`BASE STALE`).
- Any session may build a personal version at any time (`build_plugins.py --from-prefs <name>`): it packages the current version on `main` for that person, without bumping. Present the `.plugin` files themselves — never "remember to reinstall".
- A member's plugin is derived from the reference plugin plus their preferences (skills removed); hand edits to an installed plugin are forbidden.

## Routines (the routine half)
- A scheduled task holds a pointer to its trunk; check it still does. A frozen copy is replaced by the pointer text, given for the person to paste if the task cannot be edited from here.
- Changes anyone makes are proposed to everyone (peer to peer). A version already proposed is not proposed again; refusals are respected; a critical reminder at most once every 7 days. Adoption is measured from the member's **last adopted build**, never a version number.
- **Extend before creating**: a phase added to an existing routine costs far less than a new scheduled task, which pays its start-up cost on every run. Every new-routine proposal carries that comparison.

## Close
- "What could this run have done better?" — a point that repeats becomes a patch to the trunk.
- Short report: at most 3 decisions waiting, at most 5 alerts, one line per area. No account topics here: they go to the account journal.
