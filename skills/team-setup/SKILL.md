---
name: team-setup
description: Installs Totaal in a company of under 100 people — every role, not only developers — and builds the company's own plugins. Interviews the lead, connects the company's tools, creates the shared wiki on GitHub, seeds it from existing sources, chooses and installs the base plugins that fit the business, builds each employee's personal version, and schedules the cloud routines. Use on "set up Totaal", "install the team wiki", "set up our company brain", "configure Claude for my team". For one person joining an installed system, use onboarding instead.
---

# Team setup — install the method in a company

The goal: in one working session, the whole company — leadership, sales, account management, support, operations, finance, marketing, people, product — gets a wiki Claude maintains, its tools connected, its routines running in the cloud, its own plugins (a core plugin plus base plugins chosen for its activity, each employee getting a personal version), and a path for every member. Totaal is the only external plugin; every other plugin is the company's own, built here and reshaped by use. Nobody on the team needs to know git or the wiki's structure. The person who installs it is the **lead** (founder, ops, team lead).

Doctrine that shapes every step:
- **Don't babysit Claude.** Everything that can run unattended runs as a cloud scheduled task. Only steps that need the browser or local files run on a member's computer.
- **Connectors first.** Every tool the company uses is reached by the highest rung of the tool ladder: connector → API → browser (Claude in Chrome / built-in browser) → human. Push for connectors: each one connected is a task nobody does by hand again.
- **Build from what exists.** Seed the wiki from the company's documents, CRM and drive before asking people to type.

Track the phases with a task list. Ask questions with AskUserQuestion, at most 4 at a time, only where the answer changes what you build.

## Phase 0 — Clear the blockers first (5 minutes)
Most failed installations stop on access, not on Claude. Before the interview, check with the lead the "Before starting" rows of `references/install-blockers.md`: every member's Claude plan allows plugins and scheduled tasks; who can install plugins and enable connectors in the Claude organisation; tools that need IT approval; a GitHub account for everyone; whether client knowledge may be stored on GitHub. A "no" on the last one stops the installation until it is settled. After the repository is cloned (phase 3), `setup_company.py` runs `preflight.py` and stops on anything that would block. When something fails later, find the symptom in `references/install-blockers.md` and give the fix in plain words.

## Phase 1 — Interview (10 minutes)
Ask, skipping what the lead already said (the method serves every role, so ask about the whole team, not only the technical side):
1. Company name, what it sells, to whom (one sentence each).
2. Team: names, roles, who leads what. Size decides the mode: up to ~5 members → **simple** (people and routines commit on `main`, rebasing first; weekly hygiene); more → **team** (branch per run, daily arbitration). Recommend, then confirm. Also ask who owns the single-owner modules (deals, shared systems) and write them in `wiki/routines/morning.md`.
3. Working language of the team and of clients. If it is not English, translate the text of the template pages into it at phase 4, but keep file names and frontmatter keys as they are, because the scripts rely on them.
4. Tools by category: email, calendar, chat, CRM, task tracker, meeting recorder, ticketing, shared drive, BI or product analytics, any other system of record. See `references/interview.md` for the full question set.
5. **Which base plugins to install.** Load `plugin-factory` and `role-packs`; show the catalogue (`python3 ${CLAUDE_PLUGIN_ROOT}/skills/plugin-factory/scripts/install_base_plugins.py --list`). Ask which functions exist in the team, which work comes back every week and which hurts most; propose the areas and the role → plugins matrix; confirm.
6. **Say it plainly**: "These base plugins are a starting point. They will change as your team uses them: every correction, every new habit, every recurring task becomes a rule or a new skill, and everyone receives the updated plugins in their morning report."

## Phase 2 — Connect the tools (the push)
For each tool named:
1. Look for a loaded connector (ToolSearch with the tool's name). If found, call one read tool to prove it works.
2. If absent, search the registry (SearchMcpRegistry with the tool name and its category) and show the match with SuggestConnectors. Say in one line what it unlocks (`environment-check/references/connector-pitch.md`).
3. No connector exists → the next rung: an API with a key in the team's secret store, else the browser. Write the rung in `tools-and-access`.
4. Refused → record the refusal with its date; never re-ask in the same week.
Never write "impossible" for a tool without listing the rungs tried.

## Phase 3 — Create the wiki repository (cloud)
1. Ask the lead to create an **empty private GitHub repository** (or create it with `gh repo create` if the CLI is authenticated). Name suggestion: `<company>-wiki`.
2. Attach it with push access (add_repo, access push) and clone it into the working directory. If access is refused, relay the tool's exact reason and the remedy it names.
3. Install everything in one command (wiki, chosen base plugins, role matrix, the lead's preferences page and first personal build):
   `python3 ${CLAUDE_PLUGIN_ROOT}/skills/team-setup/scripts/setup_company.py --target <clone> --org "<Company>" --repo <owner/name> --mode <team|simple> --areas <a,b,c> --matrix '<{"Role": ["area"]}>' --lead <first-name> --lead-role <Role> --tools '<json of category → tool>'`
   It stops at the first error with a plain message and is safe to re-run. If `${CLAUDE_PLUGIN_ROOT}` is not set, locate the plugin folder with `find / -path "*totaal/skills/team-setup" -type d 2>/dev/null | head -1`. (Step by step instead: `init_wiki.py`, then `plugin-factory/scripts/install_base_plugins.py`, then `scripts/sync_plugin_skills.py`.)
4. The bootstrap commit is made directly on `main` (the only exception besides the daily arbitration): `git add -A && git commit -m "bootstrap: Totaal" && git push -u origin main`.
5. Present the lead's personal `.plugin` files and ask them to install and enable each one.
6. **GitHub seats**: every member needs a GitHub account added to this private repository with write access (the lead adds them; say it in one plain sentence). They connect GitHub once in Claude and never use it directly.
7. **Optional security (team mode)**: propose that GitHub itself guarantees only admins can change `main` (members push only to their branches). Recommended above ~10 people or with sensitive client knowledge; not required. Needs a paid GitHub plan for a private repository. Steps and checks: `references/protect-main.md`.
8. From now on, every write goes through `scripts/wiki_start.sh` and `scripts/wiki_commit.sh` (load the `company-wiki` skill).

## Phase 4 — Seed the knowledge
Open a session (`wiki_start.sh <lead> session setup`) and fill, from connected sources first and questions second:
- `concepts/how-we-work.md` — offer, clients, lifecycle, rituals, where things live.
- `concepts/hard-rules.md` — ask explicitly: customer-facing names, figures that may be quoted, security, client-writing rules. These rules protect the company; never guess them.
- `onboarding/who-is-who.md` and one page per member in `entities/team/`.
- `onboarding/glossary.md` — the company's words, product names, acronyms.
- `concepts/tools-and-access.md` — the table from phase 2.
- Accounts: from the CRM, the 5–15 most active accounts → one folder each from the template (card + journal), with `last_interaction` and `scanned_until` set honestly (unknown → leave empty; lint will flag it).
- Existing knowledge (shared drive docs, an old wiki, notes): ingest source by source with the `company-wiki` skill; register each in `raw/manifest.md`.
- Add 3–5 company-specific quests to `onboarding/first-week-quests.md`.
Commit with the three writes. Rewrite `hot.md`.

## Phase 5 — Make the base plugins yours
The base plugins chosen in phase 1 are installed (phase 3); the core plugin (`<org>-core`, with the company-context skill) is always there. Another area later: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/plugin-factory/scripts/install_base_plugins.py --root <ROOT> --areas <x> --matrix '<{"Role": ["x"]}>'`.
1. Adapt the starters to the company: for each installed skill, ask for one real past example (a sent proposal, a monthly report) and fold what it shows into the skill — names, structure, tone. Leave the rest to use: the tuning reshapes them.
2. Add any company-specific plugin the business needs beyond the catalogue (`plugin-factory`, mode 1), then `python3 scripts/sync_plugin_skills.py`, commit.

## Phase 6 — Schedule the routines (cloud)
Create scheduled tasks with the session's scheduling tool (load it through ToolSearch; never the local cron tools). Each prompt is a **pointer** — templates in `references/scheduled-prompts.md`. Default plan, spaced at least 15 minutes apart:
- team mode: daily arbitration on weekdays before the team starts (one owner);
- simple mode: weekly hygiene (one owner);
- evening tuning on weekdays (the lead, or each member who patches skills);
- weekly product-feedback synthesis if the company ships a product (`wiki/routines/product-feedback-weekly.md`);
- each member's morning routine is created during their onboarding (phase 7).
Steps that need a browser (tools with no connector) go in a separate task tied to the owner's computer, never in the cloud tasks. Tell the lead which approval setting each task got. A task whose runs ask for approval will stall unattended: propose switching it to automatic approval in its settings if the organisation allows it; otherwise say which phases will be skipped. Order: the arbitration first, then the morning routines, at least 15 minutes apart, in the team's time zone (`CRON_TZ=<zone>`).

## Phase 7 — Onboard every current member
Load `onboarding` and run its **system half** for each member present (GitHub seat first): preferences page with `plugins:` from the role matrix, their personal build (`python3 scripts/build_plugins.py --out <dir> --from-prefs <name>`) presented to install, plugins enabled, connectors, morning routine. For absent members, prepare it and leave the "start my onboarding" instruction in their page.

## Phase 8 — Verify and hand over
- Team mode: run the arbitration once now (load `arbitration`), so the setup branch lands on `main` before anyone is onboarded.
- `python3 scripts/lint_wiki.py --path <ROOT>`: 0 block (and PyYAML present).
- Each scheduled task exists, holds a pointer prompt, and its first run is dated.
- Every tool of `tools-and-access` has a rung and a status.
- Report to the lead in 10 lines: what runs when, what is connected and what is not (with the one action to fix it), what to fill this week, and the sentence to give each newcomer: "ask Claude: start my onboarding".
