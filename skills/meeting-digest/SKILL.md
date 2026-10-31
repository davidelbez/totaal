---
name: meeting-digest
description: Digests meeting recordings from their full transcript (never the AI recap) into decisions, actions, risks and facts filed in the right account, contact and register pages, and catches up on every recording missed by comparing IDs rather than time windows. Use on "digest this meeting", "process the transcript", "what was decided in the call", "catch up on recordings", or inside the morning routine.
---

# Meeting digest

## Read the transcript, never the recap
AI recaps invent commitments and due dates. A recap proves only that a meeting happened. An unreadable or missing transcript is reported "not digested" — never digested from the recap.

## Check completeness first
- Read the last lines: ending mid-sentence means truncated.
- Compare with the real duration (a few minutes of gap is normal).
- One participant or two minutes of audio → the meeting did not really happen; say so.

## Identify the account
In this order: meeting title · known participants · email domains · content. Several candidates → mark "to validate". None → put it in an "untagged" list in the report; never force an account.

## Extract
- Decisions · data · actions (owner and due date) · risks · context. Prefer precision to completeness.
- An action stated by a participant → recommended task for its owner (`registers/recommended-tasks.md`), unless the person explicitly asked to create it.
- Names: the wiki's spelling wins; facts: the transcript wins. A contact's role is taken from what they say themselves.

## File it (in the same run)
- A rich meeting → `sources/YYYY-MM-DD-<slug>.md`; then one journal line pointing to it (load `account-journal`).
- A meeting with a prep page → fill its `## Minutes`.
- Every person named gets the fact on their own page.
- Product signals → `registers/product-feedback.md`. Renewal or expansion signals → the account card's `## Opportunities and renewal`.
- Internal meetings → commitments routed to the next team review (load `team-review`).
- The transcript file is stored with the account's files on the shared drive in the same run; a personal recording library is not shared storage.

## Catch up by difference, every run
- List at least the last ~60 recordings of each library (~~meeting recorder, recordings in ~~shared drive, ~~calendar meeting chats) and compare each ID with the processed-ID register (`wiki/registers/processed-recordings.md`, created on first use).
- An unknown ID is first searched in the wiki (another run may have digested it), then digested.
- Proving "nothing new" needs more than an ID count: check the newest item is processed; record the newest date and the visible count; a newest date that moves backwards or a count that drops means the view changed — conclude nothing.
- When the recorder also sends recap emails, they are a second, independent path to detect meetings (never to digest them): sweep them first; any disagreement between the two paths means a broken tool.
- Report per library: total listed, excluded, caught up.
