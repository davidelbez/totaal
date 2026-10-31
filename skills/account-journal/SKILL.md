---
name: account-journal
description: Keeps each client, prospect or partner account in the wiki — the card (stable summary, people, key documents, risks, dates), the newest-first journal of events, and the contact pages fed in the same session. Use on "log this in the journal", "update the account", "what happened with", "new client", "new prospect", "account status", or whenever a mail, call or ticket concerns an account.
---

# Account journal

Every account lives in `wiki/entities/accounts/<status>/<slug>/` from its first mention: `<slug>.md` (card), `<slug>-journal.md`, `contacts/` (one page per contact), `meetings/`. Status folders: `active`, `prospects`, `partners`, `lost`; the folder moves when the status changes (`[[links]]` do not break).

## The journal line
- Newest first, **one line per event**:
  `- **YYYY-MM-DD [call|mail|meeting|ticket|review]** — one sentence → [[detail-page]]. Source: <mail subject / transcript / tool>.`
- **Never copy a KPI.** Give the headline and a link; numbers live in the detail page. Test: if this number changes tomorrow, does the line become false? Then it does not belong here.
- Lines are never rewritten later. Lines from mail, calls or recordings cite their source.
- Before writing, run `python3 scripts/journal_guard.py --journal <file> --line "<line>"`: exit 1 means the fact is already there; exit 2 means the line claims an absence the journal contradicts.
- Do not log noise (acknowledgements, FYIs).
- A "zero signal" sweep is one short line per account: mailbox, window, received and sent, "0 signal".

## The card
- A stable summary, overwritten when the state changes: what they buy, status, temperature, owner, main contact, risks and open actions, `## Key documents` (one line per document on the shared drive), `## Journal` (pointer + last entry).
- **Contract end and renewal decision are two separate dates.** The decision usually comes earlier.
- Freshness fields: `last_interaction` (last real exchange) and `scanned_until` (mailbox swept up to). A durable gap between them means re-sweep, not "quiet account".

## People
- Everyone named in an entry gets the fact on their own page **in the same session** — otherwise the fact is unfindable.
- A new contact page is built from everything the wiki already knows. An unsourced role or email is marked "to confirm", never guessed.

## Open commitments
- A commitment still open in the journal is not automatically an open action: check the channel where it would have been done. A promise to send is not proof it was sent — the sending tool is.

## Signals to route
- Renewal timing (90/60/30 days before contract end) → recommendation to the owner.
- Expansion signals → the card's `## Opportunities and renewal` section, dated, with the source.
- Product facts → `registers/product-feedback.md`.
