---
type: routine
slug: onboarding-checkins
title: "Onboarding check-ins — the trunk"
status: active
last_updated: {{DATE}}
---

# Onboarding check-ins — the trunk

> Three one-shot cloud scheduled tasks per newcomer (day 1 evening, day 7, day 30), created by the `onboarding` skill. Prompt = pointer: "read wiki/routines/onboarding-checkins.md, newcomer <name>, check-in <day>". Each run writes in a branch and reports to the newcomer AND to the manager.

## Every check-in
1. Open the wiki (`wiki_start.sh <name> routine onboarding`).
2. Read the newcomer's page, section `## Onboarding`, and [[onboarding-gaps]].
3. Verify each ticked box against reality where a tool can prove it (Totaal and personal company plugins enabled, connectors connected, routine task exists and ran, commits by the newcomer, journal lines). A box ticked but not provable is marked "to confirm", never "done".
4. Report: done · late (with the blocker and who can unblock) · next 3 steps · gaps opened and closed.
5. Never stop on a question: put decisions in the report.

## Day 1 evening
- Focus: the system half. Anything missing (connector, routine, plugin enabled) is listed with the one action to fix it.

## Day 7
- Focus: quests, first three writes, first autonomous deliverable. Gaps still open after 3 days get an owner proposed (recommended task to the person who knows).

## Day 30
- Prepare the day-30 review page `notes/YYYY-MM-DD-onboarding-review-<name>.md`: milestones, time to first deliverable, share of questions answered by the wiki, gaps closed, what to change in [[newcomer-path]]. Proposed changes to the path are diffs for the manager to accept.
