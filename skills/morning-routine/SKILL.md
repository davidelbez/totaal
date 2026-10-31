---
name: morning-routine
description: Runs or sets up a member's morning routine — sweeps mail, calendar, CRM, chat, tickets and meeting transcripts into the wiki, prepares tomorrow's meetings, queues recommended tasks, and delivers one report that starts with the decisions waiting on the member. Also applies the member's replies to that report. Use on "run my morning routine", "morning report", "what's new this morning", "set up my routine", or when the scheduled morning task fires.
---

# Morning routine

What runs is the **trunk** in the wiki: `wiki/routines/morning.md`. It is canonical once installed, and the company adapts it there. This skill explains how to run it well, how to set it up, and how to apply the replies. Never copy the trunk into a scheduled prompt.

## Run it (interactive or scheduled)
1. Open the wiki: `sh scripts/wiki_start.sh <name> routine`; read the CONTEXT block.
2. Read `wiki/routines/morning.md` and `wiki/preferences/<name>.md`. Every module runs unless the preferences page refuses it with a date and a reason. Single-owner modules run only for their owner.
3. Execute the phases in order. Gather independent sources in parallel with sub-agents in one message; each brief carries the rules it needs and the full paths, because sub-agents do not read the trunk.
4. Unattended: never stop on a question. Take the most reasonable reading, write which one, and put the decision in the report.

## What makes the sweep trustworthy
- **Watermarks, not fixed windows**: each account is swept from its `scanned_until` date. A fixed 24-hour window turns a missed run into a permanent gap.
- **Received and sent**, account by account. "Scanned, 0 signal" is written per account; a portfolio-wide zero is a suspect sweep.
- **Prove every zero**: state the total, the filter, the excluded count, then the conclusion. A tool that failed or was never called means "unknown".
- **Get the date from the system clock.** Convert tool timestamps to local time and say so.
- **Do, don't recommend**, whatever the routine can do itself (file an attachment, digest a transcript, update a card). Recommend only what needs a human decision.

## The report
Rendered inline in the conversation (or the format the preferences page asks for). Order:
0. **New personal plugin build**, when there is one: the files and the one action (install, check enabled).
1. **Waiting on your decision** — at most 3 cards: the exact action, owner, deadline (structural-debt items that concern the member come first).
2. Top 3 of the day.
3. Captured this morning — one line + link per account.
4. Shipped (always shown; if nothing, the command that proved it).
5. What teammates asked you.
6. Recommended tasks — Approve · Later · Not interested, owner selector, adjustment field.
7. Your tasks (overdue first, with age) · tomorrow's meetings with prep pages · deals.
8. Watch list.
9. **Could this run have been better?** — 3 to 5 points: missed, why, fix.
Every topic has a reply field; all replies come back in **one** message.

## Apply the replies (next turn)
- **Approve** → create the task in ~~task tracker / ~~CRM with the title format of its owner (copy the style of their last completed tasks; 2–6 word title, 2–5 bullet description: what, key date, origin, who is copied). Show the exact title before creating when the person is present.
- **Later** → write nothing; it is not a rejection.
- **Not interested** → one line in `registers/rejected-recommendations.md`.
- An instruction typed in a line wins over the block header.
- Preference answers → the member's own preferences page only.
- Commit with the three writes.

## Set it up for a member
- Create a **cloud** scheduled task with the pointer prompt (`team-setup/references/scheduled-prompts.md`), weekdays, spaced from other tasks. Record its time in the preferences page and in `wiki/routines/routines-index.md`.
- Steps that need the browser (a tool with no connector) go in a small separate task on the member's computer.
- Before the first run, load `environment-check`: a routine without the member's connectors produces an empty report.
