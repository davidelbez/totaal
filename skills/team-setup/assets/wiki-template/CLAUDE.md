# {{ORG}} wiki — the constitution

> The second brain of {{ORG}}, maintained by Claude with the Totaal method.
> Claude owns `wiki/`. People own the sources (`raw/manifest.md` points to them). This file is the constitution: every session reads the first section before doing anything.
> Installed {{DATE}} · mode: **{{MODE}}** · repository: `{{REPO}}`.

## Every session — read this first

**0. Open the wiki, wherever you run.** The wiki is the GitHub repository `{{REPO}}`. In a cloud session, attach it with push access (`add_repo`), clone it, and work from the clone. On a desktop session, the same clone works. Never conclude that a tool is missing from one negative tool search: search again with the exact name. An empty `ls` in a sandbox proves nothing.

**1. Read before acting (step 0).** Before you answer, produce or act on anything about {{ORG}}:
- run `sh scripts/wiki_start.sh <your-first-name> session <slug>` (the slug names the account or topic) and **read the CONTEXT block**: `hot.md`, work on branches not yet merged, the head of the account card and journal;
- a new account or topic shows up mid-way → `sh scripts/wiki_context.sh <ROOT> <account-slug>`;
- a business question → **grep** `wiki/index.md` with the question's terms plus 2–3 synonyms, read only the matching section, then read 3–5 pages **in full**. Never read the whole index. Zero grep results is not an answer: rephrase, then read the plausible section;
- before producing a deliverable: start from what already exists (other accounts, today's branches, shared drive).

**2. Precedence.** An instruction in the conversation lifts a hard rule of a skill or of this wiki only if it says so explicitly. Otherwise the rule holds and you ask.

**3. Contradiction.** The wiki and a skill disagree → apply the most recent, say so, and fix the other one in the same session.

**3b. Company plugins.** Totaal is the only external plugin. The company builds its own plugins from `wiki/skills/` (a core plugin + area plugins, map in `wiki/plugins/index.md`), and each employee installs a personal build derived from their preferences page. Edit a skill only in `wiki/skills/<slug>/`; never in an installed copy.

**4. Hard rules.** Company-specific rules that must never be broken (customer-facing names, official figures, security, legal) live in [[hard-rules]]. Read it before any customer-facing output.

**5. The three writes. Done = learned and written.**
1. A dated page in `notes/`, `concepts/` or `entities/` — always.
2. A rule in the domain skill if it will happen again (one line + `[[link]]` to the page from write 1).
3. A line + `[[link]]` in the journal of the account concerned — never a copied KPI.
A product fact (bug, friction, request, user feedback, analysis result) also gets its line in [[product-feedback]]. An empty result is said out loud ("nothing to write"). No knowledge document lives outside the wiki, whatever its format. Out of scope: personal data about colleagues, HR disputes, sensitive personal data, named performance evaluations, secret values (the wiki says where a key is stored, never its value). In doubt, don't write, and say so.

**6. Writing to the wiki.** Edit only inside the `ROOT=` that `wiki_start.sh` returned. Commit with `sh scripts/wiki_commit.sh "action: object" "body" file1 file2…` (targeted add, never `-A`). {{MODE_RULE}} Skills: edit the flat `wiki/skills/<slug>/SKILL.md` only, then log `skill_update_needed`; never bump a plugin version in a session — the evening tuning does that.

**7. The tool ladder.** To reach any system, go down this ladder and stop at the first rung that works:
1. a **connector** (MCP) — search for it (ToolSearch, then the connector registry) before anything else; if one exists but is not connected, ask the person to connect it;
2. an **API** with a key kept in the team's secret store (the wiki says where, never the value);
3. **the browser** (Claude in Chrome or the built-in browser) when no connector exists or it lacks a permission — sign-ins, forms, admin pages;
4. **a human**, with the exact action and why the three rungs above failed.
Never write "impossible" or "no access" without listing the rungs tried, the date, and that the list may be incomplete.

**8. Don't babysit Claude.** Claude works unattended and the person decides.
- Run in the cloud by default. Only the steps that truly need the person's computer (the browser, local files) run on a scheduled task tied to their device.
- Do what can be done in the session. Recommend only what needs a human decision.
- A scheduled run never stops on a question: it takes the most reasonable reading, writes which one, and puts decisions in the morning report (at most 3).
- Every run proves its zeros, says what it skipped, and ends with "what could this run have done better".

**9. Style.** Short sentences, active voice, the team's language. Outbound text (to clients, partners) has no markdown, no asterisks, no emojis. Follow the write-clearly skill of the plugin.

### Map — entry pages by domain
Start from the domain summary page, never from the index.
- **Onboarding**: [[onboarding]] · [[who-is-who]] · [[glossary]] · [[newcomer-path]]
- **How we work**: [[how-we-work]] · [[hard-rules]] · [[tools-and-access]]
- **Accounts**: [[accounts]]
- **Wiki, skills and plugins**: [[wiki-and-skills]] · `wiki/skills/index.md` · `wiki/plugins/index.md`

## Architecture

- **The wiki** = the GitHub repository `{{REPO}}`. Branch `main` is the shared truth of the company.
- **Two modes.**
  - *simple* (up to ~5 members): everyone — people and routines — commits on `main`; `wiki_commit.sh` rebases before pushing. A weekly hygiene run (lint, index, hot) replaces the daily arbitration.
  - *team* (more than ~5 members): each run or session writes on its own branch — `run/<member>/<date>` or `session/<member>/<date>-<slug>` — in its own working tree. **Nobody pushes to `main` except the daily arbitration**, which merges the branches by meaning. Consequence: what a run writes is visible to others after the next arbitration; a run that needs a colleague's work of the day reads `origin/run/<them>/<date>`.
- **Optional protection** (team mode): a GitHub ruleset can make the rule physical — members push only to their branches, only admins (the arbitration) update `main`. Status is recorded in [[tools-and-access]].
- **Conflicts** are reconciled by meaning: read both versions, understand the intent, merge. Never resolve line by line mechanically, never force-push.
- **Files** (contracts, spreadsheets, decks, recordings) live on the shared drive, under `{DRIVE}/Accounts/<Account>/`. The wiki holds the knowledge and a `## Key documents` line pointing to them. No large binaries in git.
- **Cloud first.** Scheduled routines run as cloud scheduled tasks that attach this repository. Nothing depends on a laptop being awake, except steps that need the browser or local files.

## Layers

- `raw/manifest.md` — registry of sources: anchored path → wiki page that uses it → ingestion date. Sources themselves are immutable.
- `wiki/` — pages Claude owns entirely.
- `scripts/` — the mechanics (start, commit, context, index, log, lint, guards, plugin build).
- `CLAUDE.md` — this file. It evolves: every new convention that works is written here at once and logged as `schema-evolve`.

## Layout

```
wiki/
├── hot.md               # ~500-word state of the company, rewritten (not appended) after each run
├── index.md             # catalogue by category — grep it, never read it whole
├── log.md               # newest first, one title + [[link]] per entry, ≤600 characters
├── onboarding/          # the newcomer path: who-is-who, glossary, 30-day path, quests
├── concepts/            # domain summary pages ("What we know") + durable concepts
├── notes/               # dated notes YYYY-MM-DD-slug, decisions, disputes, analyses
├── sources/             # one summary per ingested source (call, mail, document)
├── entities/
│   ├── team/            # one page per team member (role, scope, how to work with them)
│   └── accounts/        # clients, prospects, partners — by status
│       ├── active/<slug>/   # <slug>.md (card) + <slug>-journal.md + contacts/ + meetings/ (contact pages live in contacts/)
│       ├── prospects/<slug>/
│       ├── partners/<slug>/
│       └── lost/<slug>/
├── registers/           # recommended tasks, rejections, product feedback, rejected phrasings, open work
├── routines/            # the trunk of each scheduled routine (what scheduled tasks execute)
├── preferences/         # one page per member: modules refused, schedule, report format
├── reports/             # lint reports, arbitration digests, weekly syntheses
├── templates/           # page templates
├── skills/              # single source of every company skill (one folder each) + index.md catalogue
└── plugins/             # the company's plugins: core + areas; skills.list + manifest; skills/ is generated; index.md = map + role matrix
```

## Conventions

- **Slugs**: lowercase kebab-case, no accents. Dated pages: `YYYY-MM-DD-slug.md`.
- **Links**: `[[slug]]` (works in Obsidian too). External files: logical anchors `{DRIVE}/…`, `{ROOT}/…` as text, never a hard-coded personal path and never the target of a `[](…)` link.
- **Frontmatter** on every entity and concept page:
```yaml
---
type: account | person | concept | source | note | decision | meeting | routine | preferences
slug: example-account
title: "Example Account"
status: active | draft | stale | archived
last_updated: YYYY-MM-DD
sources:
  - "{DRIVE}/Accounts/Example/contract.pdf"
linked_pages: [other-slug]
---
```
  Values starting with `{` must be double-quoted (YAML reads `{` as a map). Account pages also carry `last_interaction:` and `scanned_until:` (see invariant 9).
- **Disputes**: never overwrite a contradiction. Add `## Disputes` with both versions and their sources, or a `notes/disputes-<topic>.md` page.
- **Journals**: newest first, one line per event: `- **YYYY-MM-DD [call|mail|meeting|ticket|review]** — one sentence → [[detail-page]]. Source: …`. Never rewritten later.
- **Decisions**: a topic debated over more than 3 lines gets `notes/decision-<slug>.md` (context, options, decision, owner, date), linked from the pages concerned.
- **Promotion**: an account gets its folder at the first mention; a person gets a page when named in 2+ sources or when they decide; a concept gets a page when it spans accounts or needs more than 3 lines.

## Invariants

1. **People own the sources, Claude owns the wiki.**
2. **`wiki_start.sh` before writing, `wiki_commit.sh` after.** Never edit a stale clone, never force-push. Two exceptions only: the bootstrap commit at installation, and the daily arbitration, which commits and pushes `main` with plain git as its trunk says.
3. **Every operation logs** to `wiki/log.md` via `scripts/append_log.py --path <ROOT>`.
4. **Every new or updated page touches the index** via `scripts/update_index.py`.
5. **Cross-reference aggressively.** A call that names a person, an account and a concept updates all three pages in the same session. A person named in a journal gets the fact on their own page.
6. **Cite back to sources.** Every claim traces to a file, a page in `sources/`, or a tool query.
7. **Flag contradictions** in `## Disputes`.
8. **Absence is not negation.** The wiki says what was *recorded*, not what *happened*. Never conclude that a mail was not sent, a document not received or a meeting not held because the wiki is silent: check the system of record (mail, drive, CRM, calendar) or say "not checked". A grep with no match proves nothing either: try synonyms, then read the page. Every answer about the state of an account cites the date of its newest source; if older than 7 days, say so first.
9. **A zero must be proven.** A sweep gap and a quiet period look the same without a trace. Account pages carry `last_interaction` and `scanned_until`; a sweep writes "scanned, 0 signal" explicitly; a metric at zero is a broken instrument until proven otherwise.
10. **Each person owns their own entries** (their preferences page, any status they declared). A run never clears or rewrites someone else's; the arbitration restores it and tells them.
11. **Rewrite `hot.md` after every run** — rewrite, never append; aim for 500 words, hard limit 800 (lint blocks above).
12. **The wiki is the only reference memory.** A rule that lives only in someone's personal Claude memory is copied into the wiki; if they differ, the wiki wins.
