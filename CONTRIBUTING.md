# Sending an employee

Anyone can send an employee. You need a GitHub account and must be at least 18; no harnsy licence is needed. The public
repository keeps its whole history: what you send here, and your GitHub name, can be read by everyone for good.

## 1. Your publisher id

Pick an id of lowercase letters, digits and dashes (for example `anna-petrova`). The first time, add
`publishers/<id>.json`:

```json
{
  "name": "Anna Petrova",
  "description": "One or two sentences about you or your team, at most 300 characters.",
  "github": ["your-github-login"],
  "github_ids": [1234567]
}
```

The name is what hr.harnsy.dev shows as the author. `github_ids` holds the numeric id of each account in `github`
(the `id` at `https://api.github.com/users/<login>`): only those accounts can send employees under this id, even after
a login is renamed. `harnsy` and the site's own paths (`api`, `teams`, `notices`, …) are taken.

## 2. The employee

Add `employees/<id>/<name>/1.0.0/`:

- `bundle.json` — the employee (schema `harnsy.employee/v1`), in English: character, principles, voice, role, prompt,
  competencies, `license` (`CC-BY-4.0` or `CC0-1.0`; an SPDX expression may add the scripts' licence, e.g.
  `CC-BY-4.0 AND MIT`) and `attribution`;
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

## 4. Licence and terms of what you send

By opening a pull request with the confirmation boxes ticked you accept the [contributor terms](TERMS.md) in the
version named in the template. In short:

- You confirm you have the right to publish everything you send. If you work for a company or used a tool, you have
  their permission and the tool's terms allow it.
- You license the **text** (and the avatar) to everyone under **CC BY 4.0 or CC0-1.0** (as `bundle.json` says) and the
  **scripts** under **MIT, Apache-2.0 or CC0** (as the skill's `LICENSE` says). No other licence is accepted.
- You also let harnsy check, sign, list and display the employee on hr.harnsy.dev, with your shown name and GitHub link.
- The licence cannot be taken back for copies already taken, and the git history and forks stay: withdrawing stops us
  offering the employee, it does not erase it.
- Our signature means «checked against our rules», not «safe».

## 5. Withdrawing, blocking, appeals

- To withdraw your version, send a pull request adding `"<id>/<name>@<version>"` to `revoked.json`. People who hired it
  keep it, marked as withdrawn.
- A harmful employee, impersonation, repeated copying or false licences, or a flood of junk gets the publisher blocked
  and its versions withdrawn. A person decides every block. We always say why in a comment on the pull request.
- **Appeals:** comment on the pull request or open an Issue (Issues are public: no personal data). Reports of unlawful
  content: write to hello@harnsy.dev, not in an Issue.

## 6. Your data

We collect no e-mail. Your GitHub name, shown name and description are public, and so are the names and e-mails in your
commits: use GitHub's private «noreply» address for commits. If you committed a secret, change it at once; it stays in
the history. Deleting or correcting: hello@harnsy.dev; we cannot erase git history or forks. Full terms:
[TERMS.md](TERMS.md).
