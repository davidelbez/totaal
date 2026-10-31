---
type: concept
slug: tools-and-access
title: "Tools and access"
status: draft
last_updated: {{DATE}}
---

# Tools and access

> Every tool the company uses, how Claude reaches it (the tool ladder: connector → API → browser → human), and who grants access. The `environment-check` skill reads this table to tell each member what to connect.

| Category | Tool | Rung (connector / API / browser) | Connector status | Who grants access | Needed by roles |
|---|---|---|---|---|---|

## What we know
- Connectors first. A tool without a connector is reached with an API key from the secret store, then with the browser.
- Secret values never live in the wiki: write where the key is stored.
