---
name: incident-review
description: Writes the review of an incident — timeline, impact, cause, fixes, follow-ups — without blame. Use on "incident", "outage", "post-mortem", "what went wrong".
---

# Incident review

> Starter skill from Totaal, adapted to {{ORG}} at setup. It is meant to change: every correction and every new habit of the team becomes a rule here (evening tuning).

## Inputs
- logs, alerts, messages during the incident
- accounts affected

## Steps
1. Build the timeline from the sources, with times converted to local time.
2. State impact (who, how long), cause, fixes, follow-ups with owners.
3. Record it as a dated note and link it from the product summary.

## Output
Incident note + recommended follow-up tasks.

## Rules
- Describe facts and systems, never people. → [[how-we-work]]
