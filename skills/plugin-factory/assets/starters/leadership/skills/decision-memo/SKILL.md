---
name: decision-memo
description: Turns a discussion into a decision page — context, options, decision, owner, date, consequences — and links it everywhere it applies. Use on "we decided", "write the decision", "decision memo", "let's settle this", after any debate longer than a few lines.
---

# Decision memo

> Starter skill from Totaal, adapted to {{ORG}} at setup. It is meant to change: every correction and every new habit of the team becomes a rule here (evening tuning).

## Inputs
- the discussion (meeting transcript, thread, mail)
- related wiki pages and earlier decisions on the topic

## Steps
1. Check no earlier decision covers it; if one does, this is an update, say so.
2. Write `notes/decision-<slug>.md`: context, options considered, decision, owner, date, who applies it.
3. Link it from every page concerned; add a line to the domain summary's What we know.
4. Recommend the follow-up tasks with owner and deadline.

## Output
The decision page + its links + recommended tasks.

## Rules
- A decision has one owner and a date, or it is not a decision yet. → [[how-we-work]]
- Contradicting an older decision is stated explicitly, never silently overwritten. → [[how-we-work]]
