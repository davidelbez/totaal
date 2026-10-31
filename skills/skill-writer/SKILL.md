---
name: skill-writer
description: Creates a new company skill for any role the right way — checks nothing already covers it, writes it in the short format (one rule per line with a link to the wiki page holding the story), keeps the description under 1024 characters, and places it in the right company plugin so the next personal builds carry it. Use on "create a skill", "make this a skill", "turn this workflow into a skill", "write a skill for". To fix an existing skill after a correction, use tuning.
---

# Skill writer

A skill is a set of instructions Claude loads when a task matches its description. Good company skills are short, precise and grounded in the wiki; the story behind each rule lives in the wiki, the rule lives in the skill.

## 1. Before creating: does it already exist?
Search three places with the subject and two synonyms:
1. installed skills (the session's skill list);
2. `wiki/skills/` and every `wiki/plugins/*/skills.list` (skills not yet installed);
3. the wiki itself — the know-how often exists without a skill.
Outcome: full overlap → modify the existing skill · partial → narrow the scope and add "complementary to X" · dependency → name the neighbour. Tell the person in two lines and write a dated note of the check.

## 2. Gather the material first
Collect real examples (a good past output, the sources used, the corrections people made) before writing. A skill written before the material is a nice template with thin content.

## 3. Write it
Location: `wiki/skills/<slug>/SKILL.md`, optional `references/` (templates, queries, recipes, identifiers), `scripts/`, `assets/`. `name` = folder name, kebab-case.

**Description** (frontmatter):
- Hard limit 1024 characters — a single skill over it makes the whole plugin fail to install. Target under 500; above 900 is tight.
- Draft it in a separate file, count it with a script (`python3 -c "print(len(open('d.txt').read()))"`), write it only when green, count again after.
- At most three sentences: what it does and for whom · when to trigger (verbs, quoted phrases people say) · optionally when not to, and which neighbour to use.
- No `<` character anywhere in the frontmatter. No uncited numbers. Never drop a trigger word to save space; cut examples and rephrasings first.

**Body** (the short format):
- Open with when to read what, and a link to the domain summary page of the wiki.
- Each rule complete in one or two lines, imperative, then `[[link]]` to the wiki page that justifies it. The rule must be complete in the skill — the model follows a link only when it thinks it needs to.
- Explain why rather than stacking MUST and NEVER. Give concrete input → output examples. Stay general, not fitted to the one case that prompted it.
- A cross-cutting rule has one home; other skills point to it in one line.
- Size: target 10–15k characters, body under ~500 lines. Above ~25k, loading gets expensive: move detail to `references/` or the wiki.
- Stories, measurements, verbatims and decision history go to a dated wiki page, never into the skill.

## 4. Register and place it
1. Ask `plugin-factory` which plugin it belongs to (the area whose people trigger it, or core if several areas use it); add the slug to exactly that `wiki/plugins/<plugin>/skills.list`.
2. Add a row to `wiki/skills/index.md`: slug · what it does · plugin · roles · trigger phrases · owner · date.
3. `python3 scripts/sync_plugin_skills.py`, then `append_log.py --action skill_update_needed --title "new skill <slug> → [[page]]"`.
4. Commit with `wiki_commit.sh`. Do not bump or package: the evening tuning ships it tonight in everyone's personal build. Until then it can be used by reading `wiki/skills/<slug>/SKILL.md`.

## 5. Test when the output can be checked
Write two or three realistic prompts and compare a run with and without the skill. Keep the prompts in `references/tests.md`.

## Changing a skill later
- Proof of no loss when slimming or moving content: list every rule-bearing line of the old version and find each one again (body, references, or a linked wiki page). Removing a rule — not moving it — is the owner's decision.
- A trimmed skill grows back without a guard: watch its size at each tuning.
