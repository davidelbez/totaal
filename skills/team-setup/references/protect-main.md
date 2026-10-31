# Optional security: only admins can change main

**Recommended, not required.** By default the scripts already enforce a convention: in team mode, `wiki_commit.sh` refuses to write on `main`, and only the daily arbitration merges. The convention protects against mistakes, not against someone (or something) that ignores it. This option makes GitHub itself enforce it:
- each member can push **only to their own branches** (`run/…`, `session/…`);
- **only admins** can update `main`, which in practice means the daily arbitration running under an admin's account;
- nobody can force-push or delete `main`.

Propose it at setup (phase 3), in one sentence: "Do you want GitHub to guarantee that only admins can change the shared version of the wiki? It is optional and takes two minutes." Recommend it for teams above ~10 people, or when the wiki holds sensitive client knowledge.

## Conditions
- **Team mode only.** In simple mode everyone writes on `main`, so protecting it would block every save. Switch to team mode first (`"mode": "team"` in `.wiki.json`, then schedule the daily arbitration).
- **GitHub plan.** GitHub rulesets on a **private** repository need GitHub Pro, Team or Enterprise Cloud. On the Free plan they only exist for public repositories. On Free, keep the convention and say so; never pretend the protection is on.
- **Roles.** Members get the **Write** role. The lead and the owner of the daily arbitration get the **Admin** role, because the arbitration must be allowed to bypass the rule.

## Set it up
Prefer the browser (Settings of the repository); use the API only if `gh` is authenticated with admin rights.

**In the browser** (repository → Settings → Rules → Rulesets → New ruleset → New branch ruleset):
1. Name: `protect-main`. Enforcement status: **Active**.
2. Bypass list: add the **Repository admin** role.
3. Target branches: **Include default branch**.
4. Rules: tick **Restrict updates**, **Restrict deletions**, and **Block force pushes**.
5. Create.

**With the API** (same result):
```bash
gh api repos/<owner>/<repo>/rulesets -X POST --input - <<'JSON'
{
  "name": "protect-main",
  "target": "branch",
  "enforcement": "active",
  "bypass_actors": [{ "actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always" }],
  "conditions": { "ref_name": { "include": ["~DEFAULT_BRANCH"], "exclude": [] } },
  "rules": [{ "type": "update" }, { "type": "deletion" }, { "type": "non_fast_forward" }]
}
JSON
```
(`actor_id: 5` is the built-in repository admin role.)

## Check it works
- As a member (Write role): `git push origin HEAD:main` must be refused; `wiki_commit.sh` on their session branch must succeed.
- The next daily arbitration must push `main`. If it is refused, its owner is not an admin: fix the role, or move the arbitration to an admin's account.
- Write the setting and the date in `wiki/concepts/tools-and-access.md` ("main protected: yes, ruleset protect-main").
