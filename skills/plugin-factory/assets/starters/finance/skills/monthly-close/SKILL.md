---
name: monthly-close
description: Runs the monthly close checklist — invoices issued, payments matched, expenses collected, anomalies — and reports what blocks the close. Use on "monthly close", "close the month", "month end", "bookkeeping checklist".
---

# Monthly close

> Starter skill from Totaal, adapted to {{ORG}} at setup. It is meant to change: every correction and every new habit of the team becomes a rule here (evening tuning).

## Inputs
- the close checklist page (create it on first use)
- ~~accounting, ~~email (receipts), ~~shared drive

## Steps
1. Go through the checklist; prove each step in the accounting tool.
2. List anomalies and missing documents with who must provide them.
3. Draft the requests for missing receipts.

## Output
Close status + list of blockers + request drafts.

## Rules
- Numbers are read live and dated; never reused from an older page. → [[how-we-work]]
- No salaries or personal amounts in the wiki. → [[hard-rules]]
