# Totaal

> *"For the strength of the Pack is the Wolf, and the strength of the Wolf is the Pack."* — Rudyard Kipling, *The Law of the Jungle* (1895)

## Why "Totaal"
In the early 1970s, Ajax and the Dutch national team played what became known as *totaalvoetbal*, Total Football. A defender could step into midfield and a forward could drop back to defend, because every player understood every role. Those teams did not rely on one star. What one player knew, all of them knew, and that made them very hard to beat.

Small companies live the opposite story. Knowledge sits in one person's head or inbox. When that person is busy, on leave or gone, the team slows down: newcomers wait, clients repeat themselves, and the same mistakes come back. Every correction you give Claude helps only the person who gave it.

Totaal is built to reverse that. Every task starts from a shared company memory and ends by writing what was learned. Every correction becomes a rule in the company's own plugins. Each person's improvement reaches everyone the next morning. One person's knowledge and another's expertise become the whole team's, and anyone can take any position.

## What it is
**The only external plugin your company installs.** Totaal builds your own plugins: base plugins chosen for your business, then a personal version for each employee. It keeps improving them through daily use, the way the best small teams already work with Claude.

It is for companies of fewer than 100 people and for every job in them: leadership, sales, account management, support, operations, finance, marketing, people and product. It is not a developer tool. People talk to Claude in plain language, and Claude handles the machinery.

See **BENEFITS.md** for everything it brings and how.

## How it works
1. **Install Totaal once.** It brings the method: a shared company wiki, cloud routines, onboarding, and the improvement loop.
2. **Claude asks about your business.** It asks what you sell, which functions your team has, and which work comes back every week. From the answers it installs the **base plugins** that fit, out of nine available: leadership, sales, account management, support, operations, finance, marketing, people and product. A **core plugin** with your company context is always included.
3. **Each employee gets a personal version.** Their role's plugins, minus the skills they don't want, plus their own settings. They are built automatically from a preferences page.
4. **The plugins change with use.** Base plugins are starting points:
   - every correction becomes a rule;
   - every recurring task without a skill becomes a new skill;
   - the plugins are updated every day, and each employee finds their new personal build in their morning report.

Within a few weeks, the plugins describe how *your* company works.

```
Totaal (external, the method)
   └── builds ──> <org>-core            (everyone)
                  <org>-sales           (sales team)
                  <org>-accounts        (account managers)
                  <org>-finance         (finance)
                  …                         (the areas your business needs)
                     └── personal build per employee (role plugins − refused skills + settings)
```

## Built for every role
| Role | Base plugin starts with | What else Claude takes off the plate |
|---|---|---|
| Leadership | weekly company update, decision memo, board update | following up every decision with its owner |
| Sales | call prep, meeting follow-up, proposal | prospect folders from the first mail, deal stages moved on clear signals |
| Account management | client report, renewal prep, client kickoff | journals kept from mail and calls, renewals 90/60/30 days ahead |
| Support | support reply, bug report | recurring issues logged once, weekly trends |
| Operations | file a document, supplier follow-up, monthly admin | documents filed and registered |
| Finance | payment reminder, monthly close, cash position | numbers always read live and dated |
| Marketing | campaign brief, newsletter, customer story | messaging consistent with the company's rules |
| People / HR | job post, interview loop | onboarding and departures, end to end |
| Product | feature spec, release notes, incident review | feedback consolidated every week |

## The five principles
1. **Read before acting, write before closing.** Every task starts from the company memory and ends with three writes: a dated page, a rule in the right skill if it will come back, and a line in the client's journal.
2. **Onboarding is the heart.** The wiki answers first, Claude handles the logistics, and every newcomer improves the path for the next one.
3. **Don't babysit Claude.** Routines run in the cloud. They never stop on a question; they put decisions in one morning report, and they prove their zeros.
4. **The tool ladder.** Claude uses a connector first, then an API, then the browser (Claude in Chrome) when there is no connector. A human comes last. Connect everything you can.
5. **Never the same mistake twice.** A correction becomes one rule in the right plugin, and everyone concerned gets it in their next personal build.

## Before you install (5 minutes that save a week)
- **Claude plan**: every member's plan must allow plugins and scheduled tasks. Check with your Claude admin.
- **Admin rights**: someone who can install plugins and enable connectors in your Claude organisation, plus the IT admin of any tool that needs approval (often email and calendar suites).
- **GitHub**: a free account for every member, and a private repository for the wiki, created by the installer. Each member accepts the GitHub invitation and connects GitHub once in Claude. After that, nobody uses GitHub directly: Claude does.
- **Data policy**: make sure your company and client contracts allow company knowledge on GitHub. The wiki never holds personal data, salaries, health information or secrets.
- **Optional security**: in team mode, GitHub can guarantee that each member writes only on their own branches and only admins can change the shared version (`main`). On a private repository this needs a paid GitHub plan. It is recommended above ~10 people, and never required.
- **Optional**: Claude in Chrome, for tools that have no connector. Obsidian, to browse the wiki as a graph.

During setup, Claude runs a pre-flight check and stops on anything that would block: access, write rights, git identity, missing tools. Every known blocker and its fix, in plain words, is listed in `skills/team-setup/references/install-blockers.md`.

## What Totaal runs, reads and sends
Totaal is transparent by design, so you can check every point below in the source:
- **It runs only bundled, readable scripts**, and only when Claude runs them during setup, onboarding or a routine. They are Python 3 (standard library, with optional PyYAML) and POSIX shell. They copy templates, edit Markdown files, run `git` against **your own** wiki repository (fetch, commit, push), and build `.plugin` zip files locally. There are no hooks, no bundled MCP servers, no package downloads and no compiled code.
- **Its only network traffic is git**, to the wiki repository you created on GitHub. The scripts make no other HTTP calls, collect no telemetry and phone home to no one.
- **It reads your tools only through the connectors you choose to connect**, with your own permissions. If no connector exists, Claude uses the browser when you allow it.
- **It never sends, signs, pays or publishes on anyone's behalf** without that person's explicit go-ahead on the final version. It drafts, prepares and recommends.
- **Your data stays yours.** Company knowledge lives in your private GitHub repository. Nothing is sent to the authors of Totaal. By rule, the wiki never stores personal data about colleagues, HR matters, health information, named evaluations or secret values.

## Install
- **From the Claude plugin directory** (once listed): search for "Totaal" and add it.
- **From this repository, right now**, in Claude Code:
  ```
  /plugin marketplace add davidelbez/totaal
  /plugin install totaal@totaal
  ```
- **As a file**: download this repository as a zip, rename it to `totaal.plugin`, and upload it in Claude (Customize → Plugins).

## Getting started
1. Install Totaal and make sure it is **enabled**.
2. Connect GitHub (where the wiki lives; every member connects it once), then as many tools as possible: mail, calendar, chat, CRM and drive. See CONNECTORS.md.
3. The lead says: **"Set up Totaal for my company."** Claude first checks what could block (5 minutes), then asks about the business, installs the base plugins and builds everyone's personal version.
4. Every teammate, whatever their job, says: **"Start my onboarding."**

## Skills
| Skill | What it does |
|---|---|
| `team-setup` | Interview, connectors, company wiki, choice of base plugins, personal builds, cloud routines |
| `plugin-factory` | Builds the company's plugins (core and areas), personal builds per employee, nightly updates |
| `role-packs` | What Claude does for each job, and which base plugin and connectors each role needs |
| `onboarding` | Arrivals, day-1 setup with the newcomer's personal plugins, first-week quests, check-ins, departures |
| `environment-check` | Pushes connectors, checks every plugin is installed and enabled, keeps routines in the cloud |
| `company-wiki` | Reads, answers, ingests and writes the company memory |
| `account-journal` | Client, prospect and partner cards and journals, contacts, renewal and expansion signals |
| `meeting-digest` | Transcripts turned into decisions and actions, with catch-up of missed recordings |
| `morning-routine` | The daily sweep and the one report that starts with your decisions |
| `midday-check` | What is done, what was promised, and what must close today |
| `team-review` | The review every two weeks: completion score, DESC, decisions with owners |
| `write-clearly` | Writing rules and the register of rejected phrasings |
| `skill-writer` | Turns recurring work into a new skill, placed in the right company plugin |
| `tuning` | Turns corrections into rules; updated personal builds reach everyone the next morning |
| `arbitration` | Merges everyone's work into the shared memory every day (larger teams) |

## Under the hood (for the person who installs it)
- The company memory is a private GitHub repository. It contains:
  - `CLAUDE.md`, the constitution;
  - `wiki/`, which holds onboarding, accounts, routines, registers, `skills/` (the single source of every company skill) and `plugins/` (the plugin map and the role-to-plugins matrix);
  - `scripts/`, the mechanics in Python 3 and POSIX shell (plugin builds included).
- Two modes:
  - **simple**, for up to about 5 members: everything is committed on `main`, and a weekly hygiene run tidies up.
  - **team**, for more members: each person and routine works on its own branch, and a daily arbitration merges them by meaning.
- Vocabulary:
  - **trunk**: a routine's procedure, kept in the wiki;
  - **three writes**: what closes every task;
  - **arbitration**: the daily merge;
  - **watermark**: the date up to which a source was swept;
  - **DESC**: Describe, Express, Specify, Consequences;
  - **tool ladder**: connector, API, browser, human.

## Privacy
Totaal collects nothing for its authors. Read the [Privacy policy](https://github.com/davidelbez/totaal/blob/main/PRIVACY.md) for what it reads, stores and sends.
