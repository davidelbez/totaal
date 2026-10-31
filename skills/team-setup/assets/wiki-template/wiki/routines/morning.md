---
type: routine
slug: morning
title: "Morning routine — the trunk"
status: active
last_updated: {{DATE}}
---

# Morning routine — the trunk

> This page is what every member's morning scheduled task executes. The task prompt is only a pointer: "read wiki/routines/morning.md and wiki/preferences/<me>.md, then run". Never copy this procedure into a prompt: the copy goes stale and wins.
> Modules are ON by default. A member turns one off only with a dated refusal and a reason in their preferences page. Silence means the module runs.
> **Single-owner modules** act on a shared object (one CRM pipeline, one shared system). They run for exactly one person, so two runs never act twice. Owners (filled at setup):

| Module | Owner |
|---|---|
| 5. Deals | (to fill) |
| 6. Health of shared systems | (to fill) |

## Guards (read before step 1)

- **Self-check**: is my prompt a pointer or a frozen copy of this procedure? If it is a copy, run THIS page instead, phase by phase, and report the drift at the top of the report. Only the running task can see its own prompt.
- **Continuity**: compare the last run date in `wiki/log.md` with today. If runs were missed, widen every window to cover the missed days.
- **Date**: take it from the system clock (`date`), never infer it. Convert tool timestamps (often UTC) to local time and say so.
- **Never stop on a question.** Take the most reasonable reading, write which one, put decisions in the report.
- **Prove every zero**: a tool that failed or was never called means "unknown", never "nothing". State the total, the filter, the excluded count, then the conclusion.
- **Name the lost phases**: connector never installed → note once; was working and now fails → incident; tools stripped in an unattended run → name the phases that were lost.
- **Run independent gathering in parallel** (sub-agents in one message). A sub-agent's brief carries the rules it needs and the full paths: sub-agents do not read this page.

## 1. Prepare
1. Attach the wiki repository, clone it, run `sh scripts/wiki_start.sh <me> routine`. Work only in `ROOT`.
2. Read the CONTEXT block and `wiki/preferences/<me>.md`.

## 2. Tasks (~~task tracker / ~~CRM)
- Pull ALL my open tasks with pagination and a full count. Regenerate only my section of `wiki/entities/team/tasks.md` (created on first use, one `## <member>` section each) (verbatim titles, links, due dates). Never edit another member's section.
- A box I ticked in the wiki while the task is still open in the tool becomes a "close it in the tool" recommendation, never a direct close.

## 3. Calendar and meeting prep (~~calendar)
- For each external meeting of the next working day: one prep page in `entities/accounts/<status>/<slug>/meetings/YYYY-MM-DD-<slug>.md` (logistics, goal, agenda, talking points, what is decided already). The same page receives the minutes afterwards.
- Write prep AFTER step 4, so already-settled topics are not presented as open.

## 4. Account signals (~~email, ~~chat, ~~meeting recorder, ~~ticketing)
- **Window = each account's watermark** (`scanned_until`), never a fixed 24h: a fixed window turns a missed run into a permanent gap.
- **Mail**: received AND sent, account by account. Write "scanned, 0 signal" when there is nothing. A portfolio-wide "0 external signal" is a suspect sweep, not a quiet day.
- **Chat**: 1:1, group, meeting chats and channels. List chats without a title too: a search by name does not find them.
- **Meetings**: digest transcripts with the meeting-digest method (catch-up by difference, never the AI recap).
- **Tickets**: notable tickets to journals; trends compare two disjoint 7-day windows, in the users' words.
- **Releases**: what shipped since last run, in two plain lists (features, fixes), naming the accounts that asked for them when known.
- **Teammates' requests**: what colleagues asked me over the last 2–3 weeks and is still open.
- Then for each account touched: journal line(s), card summary if the state changed, contact pages fed, `scanned_until` and `last_interaction` updated, product-feedback lines, upsell/renewal signals routed, recommended tasks queued.
- Attachments seen in an exchange are filed on the shared drive and listed in the card's `## Key documents`.

## 5. Deals (single owner, ~~CRM)
- Stage moves on a clear signal are done directly and announced. Every deal has a dated next action. Renewal cadence (90/60/30 days before contract end) produces recommendations. Contract end and renewal decision are two distinct dates.

## 6. Health of shared systems (single owner)
- Check that the instruments ran, not only what they say: when volume drops close to zero, every rate looks healthy.

## 7. Is my environment up to date?
- **My personal plugins**: if `main` holds a newer version of any plugin in my `plugins:` than my last adopted build (preferences page), build only those — `python3 scripts/build_plugins.py --out <dir> --from-prefs <me> --plugins <the changed ones>` — and present the files at the top of the report with the one action: install, then check each is enabled. Record the build as adopted only once I confirm.
- Compare installed plugins (and check they are **enabled**, not only installed), connectors and my scheduled tasks with the targets. **Propose** the changes, never apply them unasked. Missing connectors are proposed every time until connected or refused. A choice is stored in my preferences page so nothing is asked twice; a critical reminder at most once every 7 days.

## Before commit
- Self-review against the known error classes above. Optionally hand the diff to a read-only verifier sub-agent.
- `python3 scripts/journal_guard.py --journal <file> --line "<line>"` on every new journal line (exit 1 = already logged; exit 2 = asserts an absence that the journal contradicts).
- `python3 scripts/expire_recos.py --path <ROOT>` (recommendations older than 14 days are archived, not counted as rejections).
- Update index, log (one entry listing every active phase and its result), rewrite `hot.md`.
- `sh scripts/wiki_commit.sh "routine: morning <me> <date>" "<phases>" <files…>`.

## 8. The report (read-only, inline)
Order:
1. **Waiting on your decision** — at most 3 cards: exact action, owner, deadline. Structural-debt items from `registers/structural-debt.md` that concern me come first.
2. Top 3 of the day (never repeats a waiting client request).
3. What was captured this morning (per account, one line + link).
4. What shipped (always shown; if nothing, the command that proved it).
5. What teammates asked me.
6. Recommended tasks — each with **Approve · Later · Not interested**, an owner selector and an adjustment field.
7. My tasks (overdue first, with their age) · tomorrow's meetings and prep pages · deals.
8. Watch list.
9. **Could this run have been better?** 3–5 points: what was missed, why, the fix.
Every topic carries a reply field. All answers come back in ONE message, applied on the next turn. A line's own instruction wins over the block header.

## 9. Alert
- Only if something failed: one card to ~~chat. Nothing is sent otherwise.

## Recommended tasks — rules
- The AI recommends, the human validates. An inferred task (from mail, transcript, ticket, cadence) goes to `wiki/registers/recommended-tasks.md` under the owner's section, never straight into the tool. A task the member explicitly ordered is created at once.
- Each line: `- [ ] <title> — owner, due, account, source (added YYYY-MM-DD)`. Unknown → "to confirm", never invented.
- Before proposing: dedupe against the queue and open tasks, search `rejected-recommendations.md`, and check other channels for the action already being done.
- Filter before display: is it the routine's own job (then do it)? Right owner? Can they do it? Does the source name someone?
- Approve = create. Later = nothing written, never a rejection. Not interested = one line in the rejection register.
- Never create a task for a teammate: recommend it into their section.
