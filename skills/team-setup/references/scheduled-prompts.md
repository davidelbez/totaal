# Scheduled task prompts — pointer templates

A scheduled task holds a **pointer** to its trunk in the wiki, never a copy of the procedure (the copy goes stale and wins). Scheduled runs may not load skills, so the few rules a run cannot live without are relayed inline, below the pointer. Replace `<…>`.

## Morning routine (one per member, cloud, weekdays)
```
You are <Name>'s morning routine at <Company>.
1. Attach the GitHub repository <owner/name> with push access and clone it.
2. Run: sh scripts/wiki_start.sh <name> routine
3. Read wiki/routines/morning.md (the trunk) and wiki/preferences/<name>.md, then execute the trunk phase by phase.
Rules you must keep even if you read nothing else: commit only with scripts/wiki_commit.sh (it knows the mode; in team mode it never touches main); never stop on a question (decide, write which reading you took, put decisions in the report); a tool that failed means "unknown", never "nothing"; get today's date from the system clock; end with "what could this run have done better".
```

## Daily arbitration (team mode, one owner, cloud, weekdays before the team starts)
```
You are the daily arbitration of the <Company> wiki.
1. Attach <owner/name> with push access and clone it.
2. Read wiki/routines/arbitration.md and execute it. You are the only run allowed to push to main.
Rules: merge by meaning, never --theirs/--ours, never force-push; if git fetch fails, write nothing and report.
```

## Weekly hygiene (simple mode, one owner, cloud)
```
Attach <owner/name> with push access, clone it, read wiki/routines/weekly-hygiene.md and execute it.
```

## Evening tuning (cloud, weekdays)
```
You are the evening tuning of <Company> for <Name>.
1. Attach <owner/name> with push access and clone it.
2. Run: sh scripts/wiki_start.sh <name> routine
3. Read wiki/routines/tuning.md and wiki/preferences/<name>.md, then execute.
Rules: never skip the fine reading of sessions; package changed plugins tonight; no account topics in this report.
```

## Onboarding check-ins (one-shot, per newcomer: day 1 evening, day 7, day 30)
```
Onboarding check-in <day> for <Name> at <Company>.
Attach <owner/name> with push access, clone it, run sh scripts/wiki_start.sh <name> routine onboarding, read wiki/routines/onboarding-checkins.md and execute the <day> check-in. Report to <Name> and to <Manager>.
```

## Weekly product-feedback synthesis (one owner, cloud)
```
Attach <owner/name> with push access, clone it, run sh scripts/wiki_start.sh <name> routine feedback, read wiki/routines/product-feedback-weekly.md and execute it.
```

## Spacing and limits
- Keep at least 15 minutes between tasks and at most 2 per slot: the app may run only a few scheduled tasks at once and skip the rest silently.
- Avoid round hours (heavy traffic). Prefer e.g. 07:12, 07:41, 18:23.
- A task tied to a member's computer (browser steps) needs that computer awake and on power.
