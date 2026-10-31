---
name: file-document
description: Files an incoming document (contract, signed form, export, invoice) in the right account folder on the shared drive and lists it as a key document. Use on "file this", "save this attachment", "where does this go", "put it in the client folder".
---

# File document

> Starter skill from Totaal, adapted to {{ORG}} at setup. It is meant to change: every correction and every new habit of the team becomes a rule here (evening tuning).

## Inputs
- the attachment and the mail it came with
- the account folder naming convention

## Steps
1. Identify the account and the document type; if unsure, mark it to validate.
2. Save it under the account folder with the naming convention.
3. Add a line to the card's Key documents and a journal line if it is an event.
4. Register the source in `raw/manifest.md` when the wiki uses it.

## Output
File in the right folder + Key documents line.

## Rules
- Files live on the shared drive, never in the wiki. → [[how-we-work]]
- A document cited but not filed is a debt to report. → [[accounts]]
