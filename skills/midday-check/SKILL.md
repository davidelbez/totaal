---
name: midday-check
description: A quick, honest midday check-in — what was actually done since the morning (with proof), promises not kept, what remains ordered by what must close today, and what could not be checked. Reads the live sources, never the morning report. Writes nothing. Use on "midday check", "where am I", "what's left today", "what did I forget".
---

# Midday check

## Gather (in parallel, from the live sources)
- ~~email: today's sent and received mail — count the full set before concluding anything ("nothing sent" needs the total of today's sent items).
- ~~task tracker / ~~CRM: tasks closed and created today; tasks due today.
- The wiki: commits on all branches today (`git log --all --since=midnight`).
- ~~ticketing: tickets due this morning.
- ~~chat: requests addressed to the member today.
- ~~calendar: the rest of the day.
Never reread the morning report: the point is what happened since.

## Answer — 4 blocks, about 20 lines
1. **Done since this morning** — each item with its proof (sent mail, closed task, commit).
2. **Promises not kept** — today's and yesterday's commitments not done, with who is waiting.
3. **What remains** — ordered by what must close today, each with its estimated duration.
4. **Not checked** — sources that failed or were not reachable (that is "unknown", not "nothing").

## Rules
- Writes nothing. Credits work done by someone else to them.
- A promise to send is not proof it was sent: the sending tool is the proof.
