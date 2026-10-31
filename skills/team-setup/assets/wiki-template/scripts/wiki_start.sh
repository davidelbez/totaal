#!/bin/sh
# wiki_start.sh <member> [routine|session] [slug]
# Opens the wiki for one run or session. One call does: fetch, fast-forward main,
# create the run's own branch + working tree (team mode), sync plugin skills,
# print state lines and the CONTEXT block. The two last lines are always:
#   ROOT=<where to read and write>
#   BRANCH=<branch to commit on>
# Every later read, edit and script call uses ROOT. Never edit anything else.
set -u

MEMBER="${1:-}"
KIND="${2:-session}"
SLUG="${3:-}"
if [ -z "$MEMBER" ]; then
  echo "usage: wiki_start.sh <member> [routine|session] [slug]" >&2
  exit 2
fi
# same slug rule everywhere: accents stripped, lowercase, non-alphanumerics -> '-'
MEMBER=$(python3 -c "import sys,unicodedata,re;s=unicodedata.normalize('NFD',sys.argv[1]).encode('ascii','ignore').decode().lower();print(re.sub(r'[^a-z0-9]+','-',s).strip('-'))" "$MEMBER")

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
WIKI="${WIKI:-$(cd "$SCRIPT_DIR/.." && pwd)}"
if [ ! -e "$WIKI/.git" ]; then
  echo "ERROR: $WIKI is not a git repository (the measurement is missing, not zero)." >&2
  exit 2
fi
cd "$WIKI" || exit 2

MODE=$(python3 -c "import json,sys;print(json.load(open('.wiki.json')).get('mode','team'))" 2>/dev/null || echo team)
MAIN=$(python3 -c "import json,sys;print(json.load(open('.wiki.json')).get('main_branch','main'))" 2>/dev/null || echo main)
TODAY=$(date +%Y-%m-%d)
echo "DATE $TODAY $(date +%H:%M) (system clock — never infer the date)"
echo "MODE $MODE"

if [ -z "$(git config user.email)" ] || [ -z "$(git config user.name)" ]; then
  echo "GIT IDENTITY MISSING — set it once in this clone with the person's own name and email: git config user.name \"<Name>\" && git config user.email \"<email>\""
fi
if ! git fetch origin --prune -q; then
  echo "FETCH FAILED — do not write anything that depends on fresh state; report it at the top." >&2
fi
git worktree prune 2>/dev/null || true

print_context() {
  R="$1"
  KW=""
  # infer account slugs from the run slug: wiki/entities/accounts/<status>/<slug>/
  if [ -n "$SLUG" ] && [ -d "$R/wiki/entities/accounts" ]; then
    for d in "$R"/wiki/entities/accounts/*/*/; do
      [ -d "$d" ] || continue
      n=$(basename "$d")
      case "-$SLUG-" in *"-$n-"*) KW="$KW $n";; esac
    done
  fi
  BRANCH_CURRENT="$2" sh "$R/scripts/wiki_context.sh" "$R" $KW
}

# ---------------------------------------------------------------- simple mode
if [ "$MODE" = "simple" ]; then
  CUR=$(git rev-parse --abbrev-ref HEAD)
  if [ "$CUR" != "$MAIN" ]; then
    echo "WARNING: clone is on $CUR, switching to $MAIN"
    git checkout -q "$MAIN" || { echo "CHECKOUT FAILED — clean the tree first." >&2; exit 2; }
  fi
  if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
    echo "TREE DIRTY — uncommitted edits exist:"; git status --short --untracked-files=no | head -10
    echo "Commit or restore them before pulling. Nothing was pulled."
  else
    git pull --ff-only -q origin "$MAIN" || echo "PULL FAILED — report it; work may be on a stale base."
  fi
  echo "MAIN $(git log -1 --format='%h %ad %s' --date=short)"
  [ -f scripts/sync_plugin_skills.py ] && python3 scripts/sync_plugin_skills.py >/dev/null 2>&1 && echo "SKILLS SYNCED"
  print_context "$WIKI" "$MAIN"
  echo "ROOT=$WIKI"
  echo "BRANCH=$MAIN"
  exit 0
fi

# ---------------------------------------------------------------- team mode
CUR=$(git rev-parse --abbrev-ref HEAD)
if [ "$CUR" = "$MAIN" ]; then
  git merge --ff-only -q "origin/$MAIN" 2>/dev/null || FF_FAIL=1
else
  git fetch -q origin "$MAIN:$MAIN" 2>/dev/null || FF_FAIL=1
fi
if [ "${FF_FAIL:-0}" = "1" ]; then
  AHEAD=$(git rev-list --count "origin/$MAIN..$MAIN" 2>/dev/null || echo "?")
  BEHIND=$(git rev-list --count "$MAIN..origin/$MAIN" 2>/dev/null || echo "?")
  echo "LOCAL MAIN BLOCKED (ahead $AHEAD, behind $BEHIND). Causes: local commits on $MAIN (save them to a session branch, then reset to origin/$MAIN), a dirty tree, or a stale .lock file. Report this at the top of the run's report."
fi
echo "MAIN $(git log -1 --format='%h %ad %s' --date=short "origin/$MAIN" 2>/dev/null)"

if [ "$KIND" = "routine" ]; then
  BR="run/$MEMBER/$TODAY${SLUG:+-$SLUG}"
else
  BR="session/$MEMBER/$TODAY${SLUG:+-$SLUG}"
fi
RUNS="${WIKI_RUNS:-$(dirname "$WIKI")/wiki-runs}"
mkdir -p "$RUNS"
WT="$RUNS/$(printf '%s' "$BR" | tr '/' '-')"

EXISTING=$(git worktree list --porcelain | awk -v b="refs/heads/$BR" '/^worktree /{w=$2} $0=="branch " b {print w}')
if [ -n "$EXISTING" ]; then
  WT="$EXISTING"
  echo "WORKTREE reused $WT"
  [ "$WT" = "$WIKI" ] && echo "WARNING: the shared clone itself holds $BR — no isolation."
else
  if git show-ref --verify -q "refs/heads/$BR"; then
    git worktree add -q "$WT" "$BR" || exit 2
  elif git show-ref --verify -q "refs/remotes/origin/$BR"; then
    git worktree add -q -b "$BR" "$WT" "origin/$BR" || exit 2
  else
    git worktree add -q -b "$BR" "$WT" "origin/$MAIN" || exit 2
  fi
  echo "WORKTREE created $WT"
fi
printf '%s\n' "$BR" > "$WT/.wiki-run-branch"

cd "$WT" || exit 2
BASE=$(git merge-base HEAD "origin/$MAIN" 2>/dev/null)
if [ "$BASE" != "$(git rev-parse "origin/$MAIN")" ]; then
  echo "BASE STALE — $(git rev-list --count "HEAD..origin/$MAIN") commit(s) of $MAIN missing. Do not bump or package plugins from this tree."
else
  echo "BASE OK"
fi
[ -f scripts/sync_plugin_skills.py ] && { python3 scripts/sync_plugin_skills.py >/dev/null 2>&1 && echo "SKILLS SYNCED" || echo "SKILLS SYNC FAILED"; }

echo "INDEX $(git diff --cached --name-only | wc -l | tr -d ' ') (0 expected)"
echo "TREE $(git status --porcelain --untracked-files=no | wc -l | tr -d ' ') modified"
LOCK="$(git rev-parse --git-dir)/wiki-write.lock"
if [ -d "$LOCK" ]; then
  M=$(stat -c %Y "$LOCK" 2>/dev/null || stat -f %m "$LOCK" 2>/dev/null || echo 0)
  echo "LOCK present, age $(( $(date +%s) - M ))s (over 1800s = orphan)"
else
  echo "LOCK absent"
fi
echo "OTHER RUNS $(git worktree list | wc -l | tr -d ' ') worktree(s)"

print_context "$WT" "$BR"
echo "ROOT=$WT"
echo "BRANCH=$BR"
