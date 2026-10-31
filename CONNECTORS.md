# Connectors

## How tool references work
Plugin files use `~~category` as a placeholder for whatever tool your company connects in that category. At setup, `team-setup` asks which tool you use for each category and writes the real names into your wiki (`concepts/tools-and-access.md`), so your routines name your tools.

## The tool ladder
For every tool, Claude takes the highest rung available:
1. **Connector** — connected at workspace level in Claude. Cloud, unattended, best.
2. **API** — with a key kept in your team's secret store (the wiki records where, never the value).
3. **Browser** — Claude in Chrome or the built-in browser, for tools with no connector. Runs on a member's computer.
4. **Human** — the exact action, as a last resort.

## Categories used by this plugin
| Category | Placeholder | Typical options |
|---|---|---|
| Email | `~~email` | Microsoft 365 / Outlook, Gmail |
| Calendar | `~~calendar` | Outlook Calendar, Google Calendar, a booking tool |
| Chat | `~~chat` | Microsoft Teams, Slack |
| CRM | `~~CRM` | HubSpot, Pipedrive, Salesforce, Attio |
| Task tracker | `~~task tracker` | CRM tasks, Asana, Linear, Jira, Notion |
| Meeting recorder | `~~meeting recorder` | Teams or Zoom recordings, Fireflies, Fathom, Otter |
| Ticketing | `~~ticketing` | Helpdesk, shared support inbox, chat widget |
| Shared drive | `~~shared drive` | SharePoint / OneDrive, Google Drive, Dropbox |
| BI / product analytics | `~~BI` / `~~product analytics` | Metabase, Looker, Power BI, Amplitude |
| Email marketing | `~~email marketing` | Mailchimp, Klaviyo, ActiveCampaign |
| E-signature | `~~e-signature` | DocuSign, Dropbox Sign |
| Accounting | `~~accounting` | Xero, QuickBooks, Sage |
| Code and wiki host | (required) | GitHub — the wiki repository |

GitHub is the only required connection: the wiki lives in a private repository that cloud sessions attach.
