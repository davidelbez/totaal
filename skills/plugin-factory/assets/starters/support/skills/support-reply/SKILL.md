---
name: support-reply
description: Drafts the reply to a support request in the tone of past answers, after checking the requester in the records — left as a draft, never sent. Use on "answer the ticket", "support reply", "reply to this user", "handle the support queue".
---

# Support reply

> Starter skill from Totaal, adapted to {{ORG}} at setup. It is meant to change: every correction and every new habit of the team becomes a rule here (evening tuning).

## Inputs
- the ticket and its history
- the requester's record (read-only)
- 3 past answers to similar tickets

## Steps
1. Check who the requester is and what they have; never guess.
2. Find similar past answers; reuse their tone and facts.
3. Draft the reply: the answer first, then the steps, then a kind close.
4. Leave it as a draft; log a product fact if the ticket reveals one.

## Output
A draft reply in the ticketing tool + a product-feedback line if relevant.

## Rules
- Never send: drafts only, a person sends. → [[hard-rules]]
- A recurring issue is logged once in the register, a repeat adds a date. → [[product-feedback]]
