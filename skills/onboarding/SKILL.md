---
name: onboarding
description: Gets a newcomer autonomous in days, not months — prepares the arrival with the manager, sets up the newcomer's Claude (personal company plugins, connectors, wiki, morning routine), runs first-week quests answered from the wiki, schedules day 1, 7 and 30 check-ins, and handles departures. Use on "start my onboarding", "prepare the arrival of", "new hire", "newcomer", "onboarding check-in", "day-30 review", "someone is leaving", "offboarding".
---

# Onboarding — the heart of Totaal

A small team loses the most time when someone joins: colleagues repeat what is already known, the newcomer does not know what to ask, and the system half (accesses, tools, Claude) drags for weeks. This skill makes the wiki answer first, makes Claude carry the logistics, and makes every newcomer improve the onboarding for the next one.

Two halves, always run together:
- **Joining the company**: people, accounts, rules, how we work, a first real deliverable in week 1.
- **Joining the system**: Totaal enabled, their personal company plugins installed, connectors connected, wiki attached, preferences page, morning routine scheduled in the cloud.

The wiki pages this skill drives: `onboarding/onboarding.md` (hub), `newcomer-path.md` (30-day checklist), `first-week-quests.md`, `onboarding-gaps.md`, `who-is-who.md`, `glossary.md`, and `routines/onboarding-checkins.md`. Open the wiki first with the `company-wiki` skill (`wiki_start.sh <name> session onboarding-<newcomer>`).

## Mode A — Prepare an arrival (the manager, before day 1)
Trigger: "prepare the arrival of <name>", "we hire <name> on <date>".
1. Ask only what is missing: name, role (any function — load `role-packs` for it), start date, manager, buddy (not the manager), the accounts or topics they will own, the first autonomous deliverable expected in week 1.
2. Create `entities/team/<name>.md` from the person template; copy `newcomer-path.md` into its `## Onboarding` section and adapt it to the role (remove what does not apply, add role specifics).
3. Generate the **personal reading path** from the role pack: the domain summary pages of the role, the skills of the role's plugins (`wiki/skills/index.md`), the 5 accounts they will touch (card + last journal lines), `who-is-who`, `glossary`, `hard-rules`. Order it: day 1 → week 1.
4. List the **accesses** to request from `concepts/tools-and-access.md` for the role: tool, who grants it, by when. Create them as recommended tasks for the granters (never tasks created in someone else's name).
5. Draft the **first-week calendar** (~~calendar): a 30-minute intro with each teammate, team rituals, two external meetings to shadow. Propose; create events only on the manager's explicit go-ahead.
6. Draft the **welcome message** for the manager to send (short, warm, the first-day plan, the one sentence: "on day 1, open Claude and say: start my onboarding").
7. Schedule the **three check-ins** as one-shot cloud tasks (day 1 evening, day 7, day 30) with the pointer prompt from `team-setup/references/scheduled-prompts.md`.
8. Add the newcomer to `who-is-who`. Commit. Tell the manager what is ready and what is waiting on whom.

## Mode B — Day 1: join the system (the newcomer, ~1 hour)
Trigger: "start my onboarding", "I'm new", "set me up".
Go step by step; tick each box in the newcomer's page as it is proven, not as it is claimed.
1. **Identify** the person (session email). Unknown or external → do not set anything up; say so.
2. **Totaal**: installed **and enabled** (the only external plugin). If not, give the exact action.
3. **GitHub**: the newcomer has a GitHub account, has **accepted** the invitation to the private wiki repository (the email from GitHub; invitations expire), and has the Write role. They connect GitHub once in Claude; after that they never use it directly. Once the repository is attached (step 5), run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/team-setup/scripts/preflight.py --clone <clone>`. Fix every FIX line with the newcomer, in plain words (`team-setup/references/install-blockers.md`).
4. **Connectors — the push.** For every tool of the role in `tools-and-access`: is the connector loaded (ToolSearch, then one read call to prove it)? If not, search the registry and show it with SuggestConnectors, with the one-line reason from `environment-check/references/connector-pitch.md`. Insist once per connector: a newcomer who connects their mail, calendar and CRM on day 1 gets a useful morning report on day 2; one who does not gets an empty one. Refusals are written with the date, never re-asked that week.
5. **Wiki**: attach the repository with push access, clone, run `wiki_start.sh <name> session onboarding`, and show the newcomer what Claude just read (the state of the company, their accounts) in plain words.
6. **Preferences page**: create `wiki/preferences/<name>.md` from the template — `plugins:` from the role matrix (`wiki/plugins/index.md`), report format, language, morning time, modules refused (none by default).
7. **Personal plugins**: `python3 scripts/build_plugins.py --out <dir> --from-prefs <name>`, present the `.plugin` files, and check each one is enabled once installed. Record the adopted build in the preferences page. Explain in one line that these plugins will change with their use: corrections become rules, and updates arrive in their morning report.
8. **Morning routine**: create the cloud scheduled task with the pointer prompt; space it from existing tasks (see `wiki/routines/routines-index.md`). Tuning task only if the role patches skills.
9. **First question**: the newcomer asks the wiki one real question; answer with sources and the date of the newest one. Then show the 5 things Claude can take off their plate this week (role pack) and run the first one.
10. Commit with the three writes; mark `setup_done: true` in the preferences page.

## Mode C — Week 1: learn by doing
- Run the **quests** of `first-week-quests.md` as a conversation: the newcomer asks, Claude answers from the wiki with pages and dates.
- **The wiki answers first.** When it cannot, say so plainly ("the wiki has nothing on this — not proof that nothing exists"), add a row to `onboarding-gaps.md` (date, newcomer, question, who probably knows), and recommend a task to that person to write the answer. Never invent an answer to fill a gap.
- Each shadowed meeting is digested from its transcript with `meeting-digest`.
- Guide the newcomer's **first three writes** on a real event: a dated note, a journal line, a rule proposed for a skill.
- Help ship the **first autonomous deliverable** named by the manager, starting from what already exists in the wiki.

## Mode D — Check-ins (scheduled: day 1, day 7, day 30)
Execute `wiki/routines/onboarding-checkins.md`. Prove each box with a tool where possible; a box that cannot be proven is "to confirm". Report to the newcomer and the manager: done, late (blocker and who can unblock), next 3 steps, gaps opened and closed.

## Mode E — Day-30 review
Write `notes/YYYY-MM-DD-onboarding-review-<name>.md`: milestones reached, days to the first autonomous deliverable, share of questions the wiki answered, gaps closed and still open, what slowed them down, and **diffs proposed to `newcomer-path.md`** for the manager to accept. Link it from `onboarding.md`.

## Mode F — Departure
Trigger: "<name> is leaving", "offboarding".
- Every account or topic they own gets a new owner on its card (ask the lead; never decide it).
- Review their preferences page and, with them, anything durable that lives only in their personal Claude memory → move it into the wiki.
- List their scheduled tasks to stop, their accesses to remove (with who removes each), their open tasks and recommendations to reassign.
- Write a dated handover note linked from their person page.

## Rules
- Never create a task, event or message in someone else's name without their explicit go-ahead on the final text.
- Never store personal data beyond role and scope: no address, no health, no evaluation.
- A newcomer's question the wiki could not answer is a gift: log it, every time.
