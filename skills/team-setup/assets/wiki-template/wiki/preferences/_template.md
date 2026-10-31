---
type: preferences
slug: <name>
title: "Preferences — <name>"
member: <name>
setup_done: false
plugins: [{{ORG_SLUG}}-core]
removed_skills: []
last_updated: {{DATE}}
---

# Preferences — <name>

## Report
- Format: inline report (default) · document · direct questions
- Language: 

## Schedule
- Morning routine: weekdays at <hh:mm>, cloud task id <…>
- Tuning: <none | weekdays hh:mm>

## Modules refused (silence = the module runs)
- <module> — refused YYYY-MM-DD — reason

## Connectors
- Connected: 
- Refused (with date and reason): 

## Plugins
- Personal build: `python3 scripts/build_plugins.py --out <dir> --from-prefs <name>` (plugins and removed skills come from the frontmatter above; defaults from the role matrix in `wiki/plugins/index.md`).
- Adopted builds (plugin · version · build commit · date):
- Skills removed, with date and reason:

## Proposals already answered (never asked again)
- 
