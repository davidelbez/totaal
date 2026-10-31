---
type: routine
slug: product-feedback-weekly
title: "Weekly product-feedback synthesis — the trunk"
status: active
last_updated: {{DATE}}
---

# Weekly product-feedback synthesis — the trunk

> For companies that ship a product. One owner, cloud, weekly (start of the week).

1. `sh scripts/wiki_start.sh <owner> routine feedback`.
2. Read [[product-feedback]] (all lines since the last synthesis) and the account journals of the week.
3. Cross-check with ~~ticketing, the issue tracker and releases: a shipped fix updates the line's status.
4. Write `wiki/reports/YYYY-MM-DD-product-feedback.md`: top issues by number of accounts and severity, new requests, what shipped, verbatims (no end-user names), and 3 recommendations for the product owner.
5. Merge duplicate lines (dates added to the existing line), commit, log `review`.
