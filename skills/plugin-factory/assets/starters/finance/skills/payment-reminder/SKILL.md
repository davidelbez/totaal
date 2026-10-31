---
name: payment-reminder
description: Drafts payment reminders for overdue invoices in the right tone for the relationship, after checking the payment really is missing. Use on "payment reminder", "overdue invoice", "chase payment".
---

# Payment reminder

> Starter skill from Totaal, adapted to {{ORG}} at setup. It is meant to change: every correction and every new habit of the team becomes a rule here (evening tuning).

## Inputs
- ~~accounting overdue list (read live)
- the account card and journal (relationship, ongoing discussions)

## Steps
1. Pull overdue invoices; check each is really unpaid in the accounting tool.
2. Check the journal for context (dispute, renewal under way).
3. Draft a reminder per client, firmer with each step.
4. Show the drafts; send only on go-ahead.

## Output
Reminder drafts + journal lines.

## Rules
- Check the payment is missing in the tool before any reminder. → [[hard-rules]]
- Amounts never go into the wiki journal: headline and link only. → [[accounts]]
