---
name: arbitration
description: Runs the daily arbitration of a team-mode wiki — merges every run and session branch into main by meaning, settles or records contradictions, deduplicates, fixes conventions, updates index, log and hot, lints, and writes a short digest. The only run allowed to push to main. Use on "run the arbitration", "merge the wiki branches", "reconcile the wiki", or when the scheduled arbitration fires. In simple mode use the weekly hygiene trunk instead.
---

# Arbitration — one truth, merged by meaning

Execute `wiki/routines/arbitration.md` (the trunk). This skill holds the judgement behind it.

## Scope — what arbitration decides
- **Only two things**: inconsistencies in the wiki, and whether something belongs in the wiki.
- It never settles a business question, never decides who owns what. It may write "this has no owner" and surface it.

## Merging by meaning
- Read both versions; understand each intent; write the merged text. Never `--theirs` / `--ours` as a shortcut, never force-push, never rebase after the merges.
- Two members' blocks about the same account both stay, each in its own block.
- The same event logged from two mailboxes is one line: keep the fuller one, keep both sources.
- Cumulative fields (lists, history) are merged by prepending, newest first.
- Plugin manifests: keep the highest version.
- A branch that cannot be merged is listed in the digest with the file and both versions; the branch stays.

## Contradictions
- Settle only on a dated source (newest authoritative source wins, and say which).
- Otherwise record both under `## Disputes` with their sources. Never invent a compromise. Never delete content on the strength of one contribution.

## What arbitration removes (and only this)
- Sensitive HR or legal content about staff, internal company finances, secret values. Cut the passage, not the commit; leave a vague trace line in the digest.
- Someone else's declared status cleared or changed by another person → restore it and tell the owner in their next report.

## When main is protected
- If the repository uses the optional `protect-main` ruleset, the arbitration must run under an admin's account (the bypass list). A refused push of `main` means its owner lost the admin role: report it at the top of the digest, never work around it. → `team-setup/references/protect-main.md`

## Health
- Lint once at the end. A green lint is checked too: confirm it actually ran with its dependencies.
- Before merging: `rotate_log.py` (every run, idempotent). After merging: bump the plugins whose skills changed today (highest version seen + 1) and prove each packages — this is the one daily bump in team mode. After pushing: delete merged branches, `sh scripts/wiki_worktree_gc.sh --apply`.

## Digest (`wiki/reports/digests/YYYY-MM-DD.md`)
- Who contributed what · what went where · open disputes · lint state · points needing a human fact or an owner.
- Only what changed since yesterday. A point repeated 3 runs in a row moves to `registers/open-work.md`.
- 800 words max; 300 on an empty day.
- If `git fetch` failed: write nothing, report, stop.
