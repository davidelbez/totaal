---
name: client-report
description: Produces the periodic report for a client — usage or delivery numbers, highlights, issues, next steps — from the source data and the account journal. Use on "client report", "monthly report", "quarterly review", "report for", "business review".
---

# Client report

> Starter skill from Totaal, adapted to {{ORG}} at setup. It is meant to change: every correction and every new habit of the team becomes a rule here (evening tuning).

## Inputs
- the last report sent to this client (start from its structure)
- numbers read live from ~~BI, dated with their scope
- the account journal since the last report

## Steps
1. Pull the numbers for the period; state totals and scope; flag anything incomplete.
2. Pick 3 highlights and the issues with their status.
3. Write next steps with owners and dates.
4. Draft the cover mail; never send without go-ahead.

## Output
Report (client's language, customer-facing name) + cover mail.

## Rules
- A period still running is labelled incomplete. → [[how-we-work]]
- Customer-facing names and figures only. → [[hard-rules]]
