# What can block an installation — and the fix

Read this before phase 1 and whenever something fails. Say the fix to the person in plain words; never paste an error message without its meaning. Run `scripts/preflight.py` first: it catches most of the technical rows below.

## Before starting (check these with the lead in phase 0)
| Blocker | How to spot it | Fix |
|---|---|---|
| The Claude plan does not allow plugins or scheduled tasks for everyone | The install button or scheduling is missing for some members | Check each member's plan with the Claude admin before onboarding them. A member without plugins can still use the wiki, but not their personal build. |
| Only an admin may install plugins in the organisation | "Install" is refused, or the plugin does not appear | The Claude organisation owner installs Totaal or allows uploaded plugins. Then each member's personal builds follow the same rule. |
| Connectors are disabled by the organisation | A connector is not offered, or "not allowed by your admin" | The Claude owner enables the connector for the organisation. Until then, use the next rung of the tool ladder. |
| Some tools need IT approval (admin consent) | The connector connects but every call is refused, or asks for an admin | The tool's IT admin grants consent once for the organisation. Read-only access is a valid start. |
| Nobody has a GitHub account | — | Each member creates a free GitHub account (one minute). Only the installer creates the repository. |
| The company may not store client knowledge on GitHub | Legal, client contracts or a data policy say so | Ask before creating anything. The wiki never holds personal data, salaries, health or secrets, which removes most concerns. If hosting is still a problem, check GitHub's data-residency offers with the admin. Do not start until it is settled. |

## GitHub and the wiki repository
| Blocker | How to spot it | Fix |
|---|---|---|
| Claude cannot attach the repository | Attaching it is refused, or the tool names a missing app or permission | The GitHub owner installs Claude's GitHub app on the repository (or the organisation), or allows third-party apps in the organisation settings. Relay the exact reason the tool gives. |
| A teammate's invitation was never accepted | The teammate cannot attach the repository; `preflight.py` shows read refused | They open the invitation email from GitHub (or github.com/notifications) and accept it. Invitations expire after a few days: resend if needed. |
| Read access but no write access | Attaching works, the first commit is refused on push | Give the member the "Write" role on the repository. |
| The repository is empty | `preflight.py` says EMPTY | Nothing to do: setup creates the `main` branch. |
| The default branch is `master`, not `main` | `preflight.py` says so | Nothing to do: setup detects it and records it in `.wiki.json`. |
| Git does not know who is committing | "Please tell me who you are" | Set the identity once, in the clone only: `git config user.name "<Name>"` and `git config user.email "<email>"`. Use the person's own name and email. |
| Push to `main` refused for a member | `remote rejected … protected` | Expected when the optional protection is on: members write on their branches, and `wiki_commit.sh` already does. |
| The daily arbitration cannot push `main` | The digest reports a refused push | Its owner is not an admin, so not in the ruleset's bypass list. Give them the Admin role, or move the arbitration to an admin's account. |
| Protection cannot be enabled | The Rules menu refuses it on a private repository | Rulesets on private repositories need a paid GitHub plan (Pro, Team or Enterprise). On Free, the scripts' convention still applies. Say that plainly: never claim the protection is on. |
| A teammate changed the same page at the same time | `wiki_commit.sh` says REBASE FAILED (simple mode) | Claude reads both versions and merges them by meaning, then continues. Never force-push. |

## The plugins
| Blocker | How to spot it | Fix |
|---|---|---|
| Installed but not enabled | The skills never trigger | Enable the plugin in the plugin settings. `environment-check` checks this for every member. |
| Too many files to install at each update | People stop installing updates | Keep 3 to 6 area plugins. The morning report only shows the plugins whose version changed (`build_plugins.py --from-prefs <me> --plugins <changed>`). |
| A plugin refuses to install | An install error that mentions the description or the manifest | A skill description is over 1024 characters, or contains a `<` character. Fix it in `wiki/skills/`, then rebuild. One bad skill blocks the whole plugin. |
| A personal build is missing a skill | The person expected it | Check `removed_skills` in their preferences page. Check that the skill is listed in the plugin's `skills.list`. |
| `${CLAUDE_PLUGIN_ROOT}` is empty | The setup commands cannot find their scripts | `find / -path "*totaal/skills/team-setup" -type d 2>/dev/null \| head -1` gives the folder. |

## Scheduled routines
| Blocker | How to spot it | Fix |
|---|---|---|
| Runs stop waiting for an approval nobody gives | The task fired but the log has no entry; the run asked to approve an action | Switch the task to automatic approval in its settings if the organisation allows it. Otherwise, connectors that need approval are dropped from unattended runs: the report names the lost phases. |
| Some runs never happen | Gaps in the log | The app runs only a few scheduled tasks at once and skips the rest silently. Space them at least 15 minutes apart, never on round hours. Run the arbitration first, then the morning routines. |
| Wrong hour | Runs come too early or too late | Write schedules in the team's own time zone (`CRON_TZ=<zone>`). |
| The morning report is empty | Few or no captured items | The member's connectors are missing. Run `environment-check`; an empty report is a connector problem, not a calm day. |
| A routine needs the browser | It fails in the cloud | Split it. The browser step goes in a small task tied to the member's computer, which must be awake and on power. |

## The tool ladder in the cloud
| Blocker | How to spot it | Fix |
|---|---|---|
| The API rung cannot reach the tool from the cloud | The request is refused before it reaches the site (network allowlist) | Ask the Claude admin to allow that domain, or use the browser rung for that tool. Never retry the same request through another command. |
| Claude in Chrome is not available | No browser tools in the session | The extension must be installed and Chrome open on the member's computer. The built-in browser needs the desktop app open. Otherwise go to the human rung, with the exact action. |

## Language and people
| Blocker | How to spot it | Fix |
|---|---|---|
| The team does not work in English | Pages and reports in English | At setup, translate the text of the template pages into the team's language. Keep file names and frontmatter keys as they are, because the scripts rely on them. Reports and skills follow the person's language. |
| "I don't have time to set it up" | Onboarding stalls on day 1 | Day 1 takes one hour, and Claude does it with the person. Book that hour in the calendar during mode A of onboarding. |
| "It doesn't know anything" | Disappointing first answers | The wiki starts nearly empty. Seed it in phase 4 from the drive and the CRM. Every unanswered question is logged in the onboarding gaps and answered within the week. |
| Fear of Claude acting on people's behalf | Reluctance to connect mail or CRM | Say the rule: Claude never sends, signs, pays or publishes without the person's go-ahead on the final version. It drafts, prepares and recommends. |
