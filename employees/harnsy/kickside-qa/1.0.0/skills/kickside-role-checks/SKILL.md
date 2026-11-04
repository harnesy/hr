---
name: kickside-role-checks
description: Prove KickSide roles and permissions in a running dev copy - the copy treated as untrusted toward its host, fake test users created only after the Application security reviewer's clearance and with the owner's OK, a token for each role, one allowed and one refused action per role by API and page, the record boundary between members, access taken away ending sessions, MCP credentials capped by their owner, Keeper tokens revoked, and every test account removed at the end. Use when a module adds pages, endpoints or tools for signed-in people, when a criterion says who may or may not do something, or when access looks wider than it should.
---

# Roles and permissions in KickSide

In KickSide (as read from S1 and S2) a person's access is the union of the policies of their groups, and a deny wins. A module offers a public «module access» policy that an administrator puts into a scope; the scope gives a group; users get groups. On top of that, every endpoint is checked against its exact id, and every record (a component) has its own access. So there are three separate gates, and a screen that hides a menu item proves none of them. The admin sees everything, so the admin's view proves nothing about a member. This skill proves each role by what it is refused.

**Route:** a criterion about who may do what → **kickside-role-checks** → kickside-browser-checks for the same roles on screen → kickside-acceptance for the report.
Before this skill: a dev copy treated as untrusted toward its host; the Application security reviewer's clearance for extra accounts on it; the owner's OK to create test users there; the module's policies and endpoints. After it: an allowed and refused table per role, and no test account left.

## When to use

- A module adds pages, endpoints or MCP tools for signed-in people.
- A criterion says a role may or may not do something.
- A member seems to see more than they should.

## Inputs

- The roles from the criteria, and for each the groups it should have.
- The module's security entries: its public `module_access` policy, the private policies it includes, the exact endpoint ids each lists, and any separate tools or management policy. Read them in the module's source or in System > Security > Scopes.
- The copy's address in `$BASE`, and an owner-only folder `$SEC` (mode 700) for test credentials, outside any git repository.

## Steps

1. **Check the copy first.** Test users are created only on the dev copy, never on staging with client data and never on the client's copy. Treat every copy as untrusted toward its host: extra accounts are created only after the Application security reviewer has cleared this copy for them, and the KickSide DevOps engineer tells you how the copy is separated from its host. Before you add users, read on this copy what the ordinary users' policies allow (System > Security > Scopes; read from S1, not tried) and tell the owner what an ordinary account could reach. Test accounts test the module; never aim them at the host or other machines.
   Check: the reviewer's clearance, the owner's OK and what the ordinary policies allow are quoted in your notes.
2. **Build the role table.** Rows: admin, member (the default members group), a narrow user (the signed-in baseline group `app.security:user` plus the module's scope, without `app.security:members`), and a user without the module's scope. Columns: each page, each endpoint, each tool, and one record owned by another member. Fill in the expected answer before you test. Group names read from S2, not tried.
   Check: every endpoint id from the module's policies is in a column; an endpoint in no policy is admin-only on purpose or a bug.
3. **Create the test users with fake data.** Generate each password locally into `$SEC` and never type it into the chat: for example `node -e 'process.stdout.write(require("crypto").randomBytes(18).toString("base64url"))' > "$SEC/member.pw"`, then write the login body `{"email": "...", "password": "..."}` to `$SEC/member.json` with mode 600. Use addresses on the reserved `example.test` domain. Create each user in System > Users, or with the admin's token through `POST /api/v1/users` and a body of `email`, `password` and `groups`. Without `groups` a new user joins the default members group while that setting is on; give the narrow user its groups explicitly. (Users API read from S2, not tried.)
   Check: System > Users lists each test user with the groups the table expects.
4. **Get a token for each role.** `POST /api/public/user/token` with the login body from `$SEC`; keep the token in a shell variable, not a file you keep:
   `TOKEN_MEMBER=$(curl -s -X POST "$BASE/api/public/user/token" -H 'Content-Type: application/json' --data @"$SEC/member.json" | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>process.stdout.write(JSON.parse(s).token||""))')`
   The answer also lists the user's groups; compare them with the table. (Token call read from S2, not tried.)
   Check: each role has a token, and its groups match.
5. **Fill the API table.** Call every endpoint as every role: `curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOKEN_MEMBER" "$BASE/api/v1/<path>"`. Expected: the allowed calls succeed; a role without the endpoint in its policies is refused; no token is refused. Then the gates a member always meets: the users list behind System > Users is refused to a member (account administration is a separate policy that the members group does not include), and a member opening a record another member owns is refused unless it was shared. Write the exact codes into the table. (Gates read from S1 and S2, not tried.)
   Check: every cell has a code; every cell that differs from the expected answer is a bug report.
6. **See the same on the page.** Run kickside-browser-checks as each role: an item the role may not use is absent, and opening its route directly shows a refusal or nothing, never data. A hidden menu item is not a check by itself: the API cell in step 5 is. (Not tried.)
   Check: one screenshot per role for each criterion about access.
7. **Take access away, then give it back.** Remove the module's group from the narrow user in System > Users: the token from step 4 must be refused at once, because reducing access ends that user's sessions. Add the group back: the old session stays refused, and a new sign-in gets the access. Adding access does not end sessions; it shows at the next token. (Read from S1 and S2, not tried.)
   Check: both answers are in the table.
8. **MCP credentials are capped by their owner.** When the module offers MCP tools, sign in as the member, open the MCP page and make a credential with one capability, one component in its whitelist and an expiry; the token is shown once: put it straight into `$SEC`. With a client: `initialize` succeeds, `tools/list` shows the expected tool, one permitted call returns its result, and a tool the member's groups do not allow is absent or refused. An empty component list reaches the member's whole account: if the module's documentation promises less, that is a bug. Remove the member's group and call again: refused, since each call resolves the owner's current groups. Revoke the credential: refused. (Creating a credential with a capability, a whitelist and an expiry, and a revoked one refused, were tried as the admin in S4; the member's cap, the empty whitelist and the group removal are read from S1, not tried.)
   Check: four answers (allowed, refused, after the group removal, after the revoke) are in the table.
9. **Keeper tokens on the dev copy only.** A Keeper MCP token with a root preset gives full access to the copy. Use one only on the dev copy, only with the owner's OK, label it with the item and the date, and revoke it when the run ends; then show that the old token is refused. Keeper's token page and calls depend on the Keeper version installed on the copy: take them from that copy, not from memory or an older release (not tried). A Keeper token never reaches a staging or production copy.
   Check: the token list shows no token of yours left.
10. **Clean up.** Delete every test user (System > Users, or `DELETE /api/v1/users/<id>`, read from S2, not tried), revoke every credential, delete `$SEC`.
    Check: System > Users shows only the accounts that were there before the run; `$SEC` is gone.

## Rules (each with its check)

- **Dev copy, fake data, the reviewer's clearance and the owner's OK.** Check: both are quoted; every test address is on `example.test`.
- **Prove a role by a refusal.** One allowed and one refused action per role, by API. Check: the table has both for every role.
- **Three gates, three checks.** Module access, the endpoint id, the record's own access. Check: each has a row.
- **Passwords and tokens never in text.** Not in chat, notes, reports or screenshots; tokens in shell variables, passwords in `$SEC`. Check: search your notes and report for them; nothing found.
- **Nothing aimed at the host.** Test accounts test the module, not the host. Check: no call aimed at the host's or other machines' addresses or files.
- **Leave nothing behind.** Check: step 10 passed.

## Do not promise

- That passing these checks makes the copy safe for the client's staff: the Application security reviewer and the owner decide that.
- That a hidden menu item means a refused action.
- That a credential's capability opens every record: record access still applies.

## Hand-over

- **To the Application security reviewer, at once:** a refused action that succeeds, a token or secret that shows, a credential that reaches beyond its owner.
- **To the KickSide module developer:** an endpoint missing from a policy, a policy that grants too much, a record check that fails.
- **To the KickSide specialist:** group and scope setup on the client's copy.
- **To the KickSide DevOps engineer:** a dev copy that is not separated from its host.

## Sources

This employee is a harnsy product, not an official KickSide or Wippy product.

Facts only, no text taken: S1 the KickSide documentation (github.com/kicksideai/docs, commit 71a4588; CC BY 4.0: users and groups, security reference, MCP credentials) and S2 the KickSide app and its developer handbook (github.com/kicksideai/kickside, commit b7e0106; KickSide Community License 1.0, Spiral Scout LLC d/b/a Wippy.AI: module access, users API, dev loop). S4: the MCP credential checked live and revoked in the KickSide specialist's trial on Wippy 0.3.51a with KickSide 0.2.18. Every other step is marked inline where it was read and not tried.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
