---
name: role-packs
description: What Claude takes off each role's plate across the whole team, and which base plugin serves each role — leadership, sales, account management, customer support, operations, finance, marketing, people, product and engineering — with the connectors to push and the morning-routine focus for that role. Use at setup, when onboarding someone, and on "what can Claude do for my role", "set Claude up for our sales team", "what should finance use Claude for", "my job is X, help me".
---

# Role packs — every job in the team

Totaal is for the whole company, not only developers. Nobody needs to know git, scripts or the wiki's structure: people talk to Claude, Claude reads and writes the wiki, runs the routines and uses the tools. This skill turns that into concrete help per role. Full packs: `references/roles.md`.

## Use it at setup (`team-setup`, phase 5)
1. Map each team member to one or two roles; this gives the role → plugins matrix.
2. Each role maps to a **base plugin** of the catalogue (`plugin-factory/assets/starters/`: leadership, sales, accounts, support, operations, finance, marketing, people, product). Propose the ones the business needs; `plugin-factory` installs them.
3. Add the role's connectors to the setup push (phase 2).

## Use it at onboarding (`onboarding`, modes A and B)
- Build the newcomer's reading path and first-week quests from their role pack.
- Push the role's connectors on day 1, each with its reason.
- Set the morning-routine focus for the role in their preferences page (`## Report` → focus).

## Use it on demand ("what can Claude do for me?")
- Identify the role from the person's page in `entities/team/`, or ask in one question.
- Answer with the 5 things Claude can take off their plate this week, what is already connected, what to connect to unlock more, and which skills their plugins already hold (`wiki/skills/index.md`). Missing a plugin their work needs? Propose adding it to their preferences.
- Offer to run the first one now. Doing beats explaining.

## Rules
- Every role gets the same foundation: the wiki, the morning report, meeting digests, recommended tasks, the midday check, writing rules. The pack only changes the focus and the plugins.
- Never send, sign, pay, publish or change someone's records without their explicit go-ahead on the final version. Claude drafts and prepares; the person decides.
- Sensitive roles (finance, people) keep sensitive data out of the wiki: amounts per person, salaries, health, evaluations stay in their system of record; the wiki says where, never what.
