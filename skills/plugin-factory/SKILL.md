---
name: plugin-factory
description: Builds the company's own plugins — a shared core plugin plus plugins by area of activity, designed around the company's business and roles — and derives a personal version for each employee from their preferences, then ships updates every day. Totaal is the only external plugin; everything else is built here. Use on "create our plugins", "build a plugin for our sales team", "personalise my plugin", "remove this skill from my plugin", "which plugins should I have", "package the plugins", "my plugin is out of date".
---

# Plugin factory — your plugins, for your business, for each person

Two layers:
- **Totaal** (this plugin): the method. Installed once from outside, the same for every company.
- **The company's plugins**: built here, from the company wiki, for the company's own activity. A **core** plugin every employee installs, plus **area plugins** (for example sales, accounts, finance, people, product). Each employee installs **their own derived version**: the plugins of their role, minus the skills they refused, plus their settings.

Source of truth, always: one folder per skill in `wiki/skills/<slug>/`. Plugins only declare which skills they bundle (`wiki/plugins/<plugin>/skills.list`). Their `skills/` folders are generated, never edited. Registry: `wiki/plugins/index.md`.

## The base plugins (starting points)
A catalogue of nine base plugins ships with Totaal, each with real starter skills: leadership, sales, accounts (account management), support, operations, finance, marketing, people, product. List them: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/plugin-factory/scripts/install_base_plugins.py --list`.
- **Choose them by asking about the business**, not by installing everything: what the company sells, which functions exist in the team, which work recurs every week, which hurts most.
- **Tell the lead they will change**: they are starting points, reshaped by use — every correction becomes a rule, every recurring task without a skill becomes a new skill, and each employee gets the updated build in their morning report.
- Install: `install_base_plugins.py --root <ROOT> --areas <a,b> --matrix '{"Role": ["area"]}'` — it copies the starters into `wiki/skills/`, creates `<org>-<area>` plugins, and fills the plugin map, the role matrix and the skill catalogue. It never overwrites an existing skill.

## Mode 1 — Design the plugin map (at setup, or when the business changes)
1. Start from the base plugins chosen above, then inventory the activity: what the company sells and delivers, its account lifecycle, its roles (load `role-packs`), the recurring work people named, and the tools of each area.
2. Propose a map, then validate it with the lead:
   - **`<org>-core`** — the stable shared base every plugin depends on: company context (offer, proof points, hard rules, customer-facing names), the company's tools and where things live, writing style, and the skills several areas delegate to.
   - **Area plugins**, named after the company's own areas of activity, not after tools — usually 3 to 6 for a team under 100. A new area may start with 2 skills; above ~15, split it.
   - **Role → plugins matrix**: which plugins each role gets by default.
3. Create each plugin folder: `.claude-plugin/plugin.json` (name `<org>-<area>`, version `0.1.0`, description that names the area and its roles), `skills.list`, and a `README.md` listing the **connectors it requires** (connectors are connected at workspace level, never embedded).
4. Write the map and the matrix in `wiki/plugins/index.md`. Commit.
Rules: a slug lives in exactly one `skills.list` (the sync script refuses duplicates). A plugin is a unit of installation, not of execution: skills compose across plugins. A skill several areas need goes to core. Change core carefully: every plugin depends on it, so test the change and announce it.

## Mode 2 — Add or move a skill
- `skill-writer` writes the skill. This skill decides **which plugin** it goes to, with the map: the area whose people trigger it, or core if several areas use it.
- Add the slug to that plugin's `skills.list`, run `python3 scripts/sync_plugin_skills.py`, log `skill_update_needed`. Do not bump or package here: the evening tuning ships it tonight.
- Until the package is installed, the skill can already be used by reading `wiki/skills/<slug>/SKILL.md` and following it.

## Mode 3 — Personalise per employee
Each person's version is **derived**, never hand-made:
- Their preferences page (`wiki/preferences/<name>.md`) holds, in its frontmatter:
  - `plugins: [...]` — defaults from the role matrix, plus any extra plugin they asked for;
  - `removed_skills: [plugin:skill, ...]` — skills they refused, each with a dated reason in the body.
- Their settings (report format, language, schedule, focus) also live in the preferences page. The package carries a generated `MEMBER-PREFS.md` that points to it.
- Build: `python3 scripts/build_plugins.py --out <dir> --from-prefs <name>`. It writes one `.plugin` file per plugin in `<dir>/<name>/`, each stamped with the commit it was built from. Any session may run it (setup, onboarding, the member's morning routine); only the daily bump changes version numbers.
- Present the files to the person and give them the one action: install, and check each one is **enabled**.
- Record the adopted build in their preferences page (`## Plugins`: plugin · version · build commit · date). Adoption is measured from that commit, never from a version number.
- Any difference between two employees' plugins must come from their preferences. Hand edits to an installed plugin are forbidden: they are lost at the next build.

## Mode 4 — Ship updates (every day)
- Versions are bumped once a day, on `main` only: by the evening tuning in simple mode, by the daily arbitration in team mode (right after it merges the day's branches, so every patch of the day is in). Each employee receives their personal build through **their own morning routine** (step 7), which builds it from `main` and presents the files in the report.
- New version for each changed plugin = the highest version seen on `main` and on every `origin/run/*` and `origin/session/*` branch, plus 1. Commit the bump before building, so the build stamp (`BUILD.json`) names a commit that holds exactly what was packaged.
- Never build from a stale base (`wiki_start.sh` prints `BASE STALE`).
- Never write "remember to reinstall": present the files themselves.
- Changes made by one employee are proposed to everyone concerned (peer to peer). A version already proposed is not proposed again, and a refusal is respected.

## Package checks (done by the build script)
- Size above 0, zip integrity, manifest at the root, projected skills equal `skills.list` minus the employee's removed skills. A failed package is deleted.
- Never hand out a standalone skill file: the unit of adoption is the `.plugin` file.
- Hooks, if any, only validate (warn, or block on one explicit hard rule). They never rewrite files.
