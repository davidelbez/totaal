---
name: environment-check
description: Audits a member's Claude environment and pushes it to the maximum — connectors connected, plugins installed and enabled, scheduled tasks in the cloud and holding pointer prompts, every tool reached by the highest rung of the tool ladder (connector, API, browser, human). Use on "is my environment up to date", "what should I connect", "check my setup", "why is my morning report empty", "connect my tools", or when a session hits "no access".
---

# Environment check — connect everything, run in the cloud

The principle behind it: **don't babysit Claude.** A member gets value while away only if Claude can reach their tools without them. Every missing connector is work someone will do by hand; every routine tied to a laptop is a routine that fails when the lid is closed.

## The tool ladder (for any system, any time)
Go down and stop at the first rung that works:
1. **Connector (MCP).** Search for it with ToolSearch (the exact tool name, then the category). Loaded → prove it with one read call. Not loaded → search the registry (SearchMcpRegistry with the tool name and its category) and show it with SuggestConnectors.
2. **API** with a key from the team's secret store. The wiki says where the key is stored, never its value.
3. **Browser**: Claude in Chrome, or the built-in browser. Use it for tools with no connector, missing permissions, sign-ins, forms and admin pages. It runs on the member's computer, so it is the one rung that is not cloud.
4. **Human**: the exact action, and why the three rungs above failed.
Never write "impossible", "no access" or "there is no tool" without listing the rungs tried, the date, and that the list may be incomplete. A tool search that returns nothing proves nothing: search again with the exact name.

## The check (run in this order)
1. **Identify** the member and read `wiki/preferences/<name>.md` and `wiki/concepts/tools-and-access.md`.
2. **Connectors**: for each tool of their role, report connected (proven by a call) · available but not connected · no connector (next rung). Push for each missing one with its reason (`references/connector-pitch.md`). Respect a dated refusal; re-propose a critical one at most once every 7 days.
3. **Plugins**: Totaal (the only external plugin) and every company plugin listed in the member's `plugins:` are installed **and enabled**, at the target version (company plugins: the version on `main`; Totaal: the version the lead installed). If their personal build is behind, build it with `--from-prefs` and present it. Third-party plugins that duplicate what the company plugins do are listed as candidates to remove. If the wiki's plugin source changed since their last adopted build, propose the new package.
4. **Scheduled tasks**: list them (the session's scheduling tools, through ToolSearch). Each must:
   - hold a **pointer** to its trunk in `wiki/routines/`, not a copy of the procedure;
   - run in the **cloud** unless it needs the browser or local files;
   - be spaced at least 15 minutes from the others, avoiding round hours;
   - have a recent run in `wiki/log.md`. A task that fired but left no log entry is a lost run: name the likely cause (quota, concurrency limit, killed at dispatch, computer asleep for local tasks).
5. **Placement**: anything running locally that could run in the cloud → propose moving it. Anything in the cloud that needs the browser → split it into a small local task.
6. **Report** in one table: item · state · the one action to fix it. Store each answer in the preferences page (`## Proposals already answered`) so nothing is asked twice.

## When something blocks
Find the symptom in `team-setup/references/install-blockers.md` (plan, admin rights, IT consent, GitHub invitation, approvals, network allowlist, browser availability) and give the fix in plain words. `python3 ${CLAUDE_PLUGIN_ROOT}/skills/team-setup/scripts/preflight.py --clone <clone>` checks the technical part.

## Rules
- Propose, never apply unasked: installing, connecting and scheduling need the member's yes.
- Connector never installed → note it once, no alert. Working connector now failing → incident. Tools stripped in an unattended run (approval setting) → name the phases lost; it is not a failure of the tool.
- Measure adoption on the member's own installation, never on a cloud session's own install.
