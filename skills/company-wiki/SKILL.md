---
name: company-wiki
description: Operates the company wiki that Claude maintains on GitHub — opens it before acting, answers business questions from it with sources and dates, ingests mails, calls and documents, and closes every task with the three writes. Use on any question or task about the company, its accounts, people, decisions or rules, and on "ingest", "file this", "what do we know about", "update the wiki", "write it down", "lint the wiki".
---

# Company wiki — read before acting, write before closing

The wiki is the company's only reference memory. It compounds: every session that reads first and writes last makes the next one faster. `CLAUDE.md` at the repository root is the constitution; its first section is mandatory reading. Script usage and exit codes: `references/scripts.md`.

## 1. Open it (every session, step 0)
- Cloud: attach the repository with push access (add_repo), clone it. Desktop: use the existing clone. Never read stale copies found in synced folders.
- `sh scripts/wiki_start.sh <first-name> session <slug>` — the slug names the account or topic. Read the whole **CONTEXT** block: `hot.md`, unmerged work of colleagues, the account card and journal head.
- Work only inside the printed `ROOT=`; commit only with `scripts/wiki_commit.sh`.
- An account or topic appears mid-way → `sh scripts/wiki_context.sh <ROOT> <slug>`.

## 2. Answer a question from it
1. **Grep the index**, never read it whole: `grep -i "term\|synonym1\|synonym2" wiki/index.md`.
2. Read the matching section, then 3–5 candidate pages **in full**.
3. Zero results is not an answer: rephrase, read the plausible domain summary, then grep the whole `wiki/`.
4. **Absence is not negation.** The wiki says what was recorded, not what happened. "Was it sent / received / held?" is answered by the system of record (~~email, shared drive, ~~CRM, ~~calendar) — or by "not checked".
5. **Date the answer**: cite the newest source's date; if it is older than 7 days, say so first and offer to check live.
6. A number read in the wiki is a photo at a date, never served as current.
7. An answer that combines 3+ sources or finds a non-obvious link → file it as `notes/YYYY-MM-DD-<slug>.md`.

## 3. Ingest a source (mail, call, document)
1. Register it in `raw/manifest.md` (anchored path → page → date). Files stay on the shared drive; the wiki holds the knowledge.
2. Rich source → `sources/YYYY-MM-DD-<slug>.md` from the template (facts, decisions, actions, links).
3. **Cross-reference aggressively**: every account, person and concept named gets the fact on its own page in the same session.
4. Account events → one journal line each (load `account-journal`).
5. First ingestion for a new account: summarise in 4–6 lines and confirm before filing; after that, file directly.

## 4. Close every task: the three writes
Done = learned and written.
1. A dated page (`notes/`, `concepts/` or `entities/`) — always.
2. A rule in the domain skill if it will happen again: edit `wiki/skills/<slug>/SKILL.md`, one rule + `[[link]]`, then `append_log.py --action skill_update_needed`. Never bump a plugin version here.
3. A journal line + `[[link]]` for the account concerned — never a copied KPI.
Plus: a product fact → its line in `registers/product-feedback.md`. A wording correction → `registers/rejected-phrasings.md`. Nothing to write → say "nothing to write" explicitly.
Then: `update_index.py` for each new or changed page · `append_log.py` (one title + link, ≤600 characters) · rewrite `hot.md` if the state changed · `wiki_commit.sh "<action>: <object>" "<body>" <files…>`.

## 5. Conventions that break things when ignored
- Frontmatter values starting with `{` are double-quoted. Anchors (`{DRIVE}`, `{ROOT}`) are text, never link targets.
- Slugs: lowercase kebab, no accents; dated pages `YYYY-MM-DD-slug.md`. Links: `[[slug]]`.
- Contradictions are never overwritten: `## Disputes` with both versions and sources.
- A debate longer than 3 lines → `notes/decision-<slug>.md` (context, options, decision, owner, date).
- Each person owns their own entries (preferences page, declared statuses): never clear or rewrite someone else's.
- Out of scope: colleagues' personal data, HR disputes, sensitive personal data, named evaluations, secret values. In doubt, do not write — and say so.

## 6. Git
- **Team mode**: each run writes on its own branch (`run/…` or `session/…`) in its own working tree and pushes it; only the daily arbitration pushes `main`. Need a colleague's work of today? `git show origin/<their-branch>:<path>`.
- **Simple mode**: commits go to `main`; the commit script rebases first.
- A conflict is reconciled by meaning — read both, understand both intents, merge. Never `--theirs`/`--ours` blindly, never force-push.
- A "command failed" from a remote shell or connector does not prove failure: check the state before re-running, or you double the write.

## 7. Health
- `python3 scripts/lint_wiki.py --path <ROOT>`: fix every BLOCK. A lint that did not run, or ran without PyYAML, is reported as such — never as "0 block".
- A zero must be proven: "scanned, 0 signal" is written; a silent account is re-swept, not assumed calm.
