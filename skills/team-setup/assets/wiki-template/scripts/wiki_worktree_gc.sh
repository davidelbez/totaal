#!/bin/sh
# wiki_worktree_gc.sh [--apply]
# Removes run/session working trees whose branch is already merged into main
# and whose tree is clean. Dry run by default. Run after the daily arbitration.
set -u
APPLY=0; [ "${1:-}" = "--apply" ] && APPLY=1
WIKI="${WIKI:-$(cd "$(dirname "$0")/.." && pwd)}"
cd "$WIKI" 2>/dev/null && git rev-parse --git-dir >/dev/null 2>&1 || { echo "Repo unreadable — the measurement is missing, not zero." >&2; exit 2; }
MAIN=$(python3 -c "import json;print(json.load(open('.wiki.json')).get('main_branch','main'))" 2>/dev/null || echo main)
git fetch -q --prune origin; git worktree prune
TOTAL=0
git worktree list --porcelain | awk '/^worktree /{w=$2} /^branch /{print w" "$2}' > /tmp/.wiki-wt.$$
while read -r W REF; do
  B=${REF#refs/heads/}
  [ "$W" = "$WIKI" ] && continue
  case "$B" in "$MAIN"|master) continue;; esac
  DIRTY=$(git -C "$W" status --porcelain --untracked-files=no | grep -v '.wiki-run-branch' | wc -l | tr -d ' ')
  if [ "$DIRTY" != "0" ]; then echo "KEEP $W (dirty)"; continue; fi
  if ! git merge-base --is-ancestor "$B" "origin/$MAIN" 2>/dev/null; then echo "KEEP $W (not merged)"; continue; fi
  if [ "$APPLY" = "1" ]; then
    git worktree remove "$W" && echo "REMOVED $W" || echo "FAILED $W"
  else
    echo "TO REMOVE $W"
  fi
  TOTAL=$((TOTAL+1))
done < /tmp/.wiki-wt.$$
rm -f /tmp/.wiki-wt.$$
echo "TOTAL $TOTAL working tree(s)"
