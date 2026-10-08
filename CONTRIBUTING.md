# Sending an employee

Anyone can send an employee. You need a GitHub account; no harnsy licence is needed.

## 1. Your publisher id

Pick an id of lowercase letters, digits and dashes (for example `anna-petrova`). The first time, add
`publishers/<id>.json`:

```json
{
  "name": "Anna Petrova",
  "description": "One or two sentences about you or your team, at most 300 characters.",
  "github": ["your-github-login"]
}
```

The name is what hr.harnsy.dev shows as the author. Only the GitHub logins listed there can send employees under this
id. `harnsy` and the site's own paths (`api`, `teams`, `notices`, …) are taken.

## 2. The employee

Add `employees/<id>/<name>/1.0.0/`:

- `bundle.json` — the employee (schema `harnsy.employee/v1`), in English: character, principles, voice, role, prompt,
  competencies, `license` and `attribution`;
- `listing.json` — the card: `title`, `tags`;
- `avatar.png` (or .jpg / .webp), at least 512×512, optional — no real person, brand or art you have no rights to;
- `docs/persona-casebook.md`, optional;
- `skills/<skill>/`, optional, at most 5 (the skill's name: lowercase letters, digits and dashes, at most 40). Inside only
  `SKILL.md` (required, at most 64 KB), `LICENSE` and `scripts/<file>` (flat, at most 256 KB each, a plain file name);
  at most 20 files per skill, 2 MB for all skills, UTF-8 text only. Scripts are source code with `LICENSE` holding the
  MIT, Apache-2.0 or CC0 text; explain every network call or download in `SKILL.md`. No hooks, commands, agents, MCP or
  plugin files, no symlinks.
  `SKILL.md` starts with a frontmatter of `key: value` lines between `---` lines: `name` (the folder's name) and
  `description` (when to use it, at most 1024 bytes); optional `license`, `version`, `when_to_use`, `argument-hint`,
  nothing else (`allowed-tools`, `hooks` are refused). No inline shell: no `!` before a backtick, no fence opening with
  a `!`. `bundle.json` names every skill: `"skills": [{"name": "<skill>", "description": "…"}]`.

Rules the check and the review apply:

- English text; the prompt says the employee is an AI agent and never claims to be human.
- No real persons or companies without their consent; no secrets, keys or personal data.
- What you adapted is licensed for it and credited in `attribution` (name, https url, SPDX licence, modified).
  Allowed for text: CC BY, CC0, MIT, Apache-2.0, OGL and similar permissive licences; ShareAlike, NonCommercial,
  NoDerivatives and unlicensed sources only as ideas, retold in your own words.
- Legal, finance, medical and HR employees prepare work; a professional decides.
- No instructions to deceive, spam, scrape behind logins, evade checks, move money or change live systems without the
  person's approval, and no hidden instructions to the hirer's agents.
- One pull request, one employee. A published version never changes: send a new version folder (`1.0.1`, `1.1.0` …).

Check before you send:

```
cd tools/check && go run . --dir ../..
```

## 3. Review

- The automatic check runs on every push; fix what it reports.
- The harnsy HR agent (an AI) then reviews the pull request and lists findings: file, what is wrong, how to fix.
  Fix them in the same pull request, as many rounds as needed.
- A person reads the review and merges or closes. Merged employees appear on hr.harnsy.dev within an hour.

## 4. Licence of what you send

By sending a pull request you confirm that you have the right to publish its content and you license it under the
licence your `bundle.json` states (CC BY 4.0 if you are unsure), and its scripts under the licence in their `LICENSE`
file, so that anyone may use it and harnsy may check, sign and list it.

## 5. Withdrawing and blocking

- To withdraw your version, send a pull request adding `"<id>/<name>@<version>"` to `revoked.json`. People who hired it
  keep it, marked as withdrawn.
- A malicious employee, impersonation, repeated copying or false licences, or a flood of junk gets a publisher blocked
  and its versions withdrawn. A person decides every block. Appeals: comment on the pull request or write to
  hello@harnsy.dev.
