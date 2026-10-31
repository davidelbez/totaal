#!/bin/sh
# wiki_context.sh [ROOT] [account-slug ...]
# Prints the CONTEXT block every run must read before acting:
# hot page, work on branches not yet merged into main, and the head of each
# named account's card and journal.
set -u
R="${1:-$(cd "$(dirname "$0")/.." && pwd)}"; [ $# -gt 0 ] && shift
cd "$R" || exit 2
MAIN=$(python3 -c "import json;print(json.load(open('.wiki.json')).get('main_branch','main'))" 2>/dev/null || echo main)
OWN="${BRANCH_CURRENT:-}"

echo "=== CONTEXT — step 0: read this before acting ==="
echo "--- HOT ---"
if [ -f wiki/hot.md ]; then
  awk 'BEGIN{fm=0} /^---$/{fm++; next} fm>=2 && NF>0' wiki/hot.md
else
  echo "(no wiki/hot.md)"
fi

echo "--- WORK NOT YET MERGED ---"
N=0
for B in $(git for-each-ref --sort=-committerdate --format='%(refname:short)' refs/remotes/origin/run refs/remotes/origin/session 2>/dev/null); do
  SHORT=${B#origin/}
  [ "$SHORT" = "$OWN" ] && continue
  C=$(git rev-list --count "origin/$MAIN..$B" 2>/dev/null || echo 0)
  [ "$C" = "0" ] && continue
  STAR=""
  for kw in "$@"; do
    git diff --name-only "origin/$MAIN...$B" -- wiki 2>/dev/null | grep -q "$kw" && STAR=" * $kw"
  done
  echo "  $SHORT ($(git log -1 --format='%cd' --date=format:'%Y-%m-%d %H:%M' "$B"), $C commit(s))$STAR — $(git log -1 --format=%s "$B" | cut -c1-90)"
  git diff --name-only "origin/$MAIN...$B" -- wiki 2>/dev/null | head -6 | sed 's/^/      /'
  N=$((N+1)); [ "$N" -ge 10 ] && { echo "  … more branches (git branch -r)"; break; }
done
[ "$N" = "0" ] && echo "  (none — or simple mode)"
echo "  read one with: git show origin/<branch>:<path>"

for kw in "$@"; do
  CARD=$(find wiki/entities -path "*/$kw/$kw.md" 2>/dev/null | head -1)
  [ -z "$CARD" ] && CARD=$(find wiki/entities -name "$kw.md" 2>/dev/null | head -1)
  [ -z "$CARD" ] && { echo "--- ACCOUNT $kw: no page found (absence is not proof — search synonyms) ---"; continue; }
  STATUS=$(basename "$(dirname "$(dirname "$CARD")")")
  echo "--- ACCOUNT $kw (status: $STATUS) ---"
  [ "$STATUS" = "lost" ] && echo "  WARNING: this account is in lost/"
  awk 'BEGIN{fm=0} /^---$/{fm++; next} fm>=2 && NF>0' "$CARD" | head -25 | cut -c1-250
  J="$(dirname "$CARD")/$kw-journal.md"
  if [ -f "$J" ]; then
    echo "  -- journal (newest first) --"
    awk 'BEGIN{fm=0} /^---$/{fm++; next} fm>=2 && NF>0 && !/^<!--/' "$J" | head -13 | cut -c1-300
  fi
done
echo "=== END CONTEXT ==="
