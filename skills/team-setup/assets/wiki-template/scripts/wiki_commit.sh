#!/bin/sh
# wiki_commit.sh [--branch <expected>] "message" "body" file1 [file2 ...]
# Run from ROOT (the directory wiki_start.sh returned).
# Targeted add (never -A), lock, commit, push, verify the push landed.
# Team mode refuses main. Simple mode commits on main and rebases before pushing.
# Exit codes: 3 on main in team mode · 9 wrong branch · 4 no files · 5 lock busy
#             6 add failed · 10 short-format check failed · 7 commit failed · 8 push not verified
set -u
EXPECTED=""
if [ "${1:-}" = "--branch" ]; then EXPECTED="$2"; shift 2; fi
MSG="${1:-}"; BODY="${2:-}"
[ $# -ge 2 ] && shift 2 || shift $#
if [ -z "$MSG" ] || [ $# -eq 0 ]; then
  echo "usage: wiki_commit.sh [--branch b] \"message\" \"body\" file..." >&2
  echo "No files listed: refusing (never git add -A)." >&2
  exit 4
fi

TOP=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "not in a git tree" >&2; exit 2; }
cd "$TOP" || exit 2
MODE=$(python3 -c "import json;print(json.load(open('.wiki.json')).get('mode','team'))" 2>/dev/null || echo team)
MAIN=$(python3 -c "import json;print(json.load(open('.wiki.json')).get('main_branch','main'))" 2>/dev/null || echo main)
BR=$(git rev-parse --abbrev-ref HEAD)

if [ "$MODE" != "simple" ] && { [ "$BR" = "$MAIN" ] || [ "$BR" = "master" ]; }; then
  echo "REFUSED: HEAD is $BR. In team mode nobody pushes to $MAIN — only the daily arbitration does." >&2
  exit 3
fi
[ -z "$EXPECTED" ] && [ -f .wiki-run-branch ] && EXPECTED=$(cat .wiki-run-branch)
if [ -n "$EXPECTED" ] && [ "$EXPECTED" != "$BR" ]; then
  echo "REFUSED: expected branch $EXPECTED but HEAD is $BR." >&2
  exit 9
fi
[ -z "$EXPECTED" ] && echo "WARNING: no expected branch known; committing on $BR."

LOCK="$(git rev-parse --git-dir)/wiki-write.lock"
TRY=0
while ! mkdir "$LOCK" 2>/dev/null; do
  M=$(stat -c %Y "$LOCK" 2>/dev/null || stat -f %m "$LOCK" 2>/dev/null || echo 0)
  AGE=$(( $(date +%s) - M ))
  if [ "$AGE" -gt 1800 ]; then echo "orphan lock (${AGE}s) removed"; rmdir "$LOCK" 2>/dev/null; continue; fi
  TRY=$((TRY+1)); [ "$TRY" -ge 3 ] && { echo "LOCK BUSY — another writer is active." >&2; exit 5; }
  sleep 30
done
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

if [ -n "$(git diff --cached --name-only)" ]; then
  echo "Foreign staged files found (unstaged, nothing lost):"; git diff --cached --name-only | head -20
  git restore --staged . 2>/dev/null || git reset -q
fi
git add -- "$@" || { echo "git add failed" >&2; exit 6; }
if [ -f scripts/check_short_format.py ]; then
  if ! python3 scripts/check_short_format.py; then
    git reset -q -- "$@"
    echo "Short-format check failed — fix the skill lines above, then commit again." >&2
    exit 10
  fi
fi
if [ -n "$BODY" ]; then git commit -q -m "$MSG" -m "$BODY" || exit 7; else git commit -q -m "$MSG" || exit 7; fi
SHA=$(git rev-parse --short HEAD)
echo "COMMIT $SHA on $BR"
git show --stat --format='%s' HEAD | head -40

if [ "$MODE" = "simple" ]; then
  if ! git pull --rebase --autostash -q origin "$BR"; then
    echo "REBASE FAILED — a real conflict with a teammate's change: run git status, reconcile by meaning (never force-push), then git rebase --continue and push." >&2
    exit 7
  fi
fi
git push -q -u origin "$BR" || { sleep 5; git push -q -u origin "$BR"; }
if git ls-remote --exit-code --heads origin "$BR" >/dev/null 2>&1 && \
   [ "$(git ls-remote --heads origin "$BR" | cut -f1)" = "$(git rev-parse HEAD)" ]; then
  echo "DELIVERED=$BR $(git rev-parse --short HEAD)"
else
  echo "PUSH NOT VERIFIED — origin/$BR does not hold $(git rev-parse --short HEAD)." >&2
  exit 8
fi
