---
type: concept
slug: wiki-and-skills
title: "Wiki and skills — how this system works and improves"
status: active
last_updated: {{DATE}}
---

# Wiki and skills

## What we know
- Three levels of knowledge, all in the wiki: the index (level 0) → one domain summary page per domain with "What we know" (level 1) → dated detailed pages (level 2).
- A skill holds rules, one per line, each with a `[[link]]` to the page that tells its story. Stories never go into skills.
- Company skills live once in `wiki/skills/<slug>/` (catalogue: `wiki/skills/index.md`). Company plugins (`wiki/plugins/`: a core plugin + area plugins) list them in `skills.list`; their `skills/` folder is generated.
- Each employee installs a personal build: the plugins of their role minus the skills they refused (`wiki/preferences/<name>.md`). Differences between two employees come only from their preferences.
- Totaal is the only external plugin. Sessions and routines never bump plugin versions; they log `skill_update_needed`. The tuning turns corrections into patches; versions are bumped once a day on `main`; each employee receives their personal build in their morning report.
- A scheduled task holds a pointer to its trunk in `wiki/routines/`, never a copy.
- A rule broken twice is a placement problem before it is a content problem.
