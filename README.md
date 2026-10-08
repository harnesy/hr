# harnsy employee catalog

The source of every employee on [hr.harnsy.dev](https://hr.harnsy.dev): ready AI workers you hire into a
[harnsy](https://harnsy.dev) project. An employee is a character, a prompt and the working skills it needs to do one
concrete job end to end.

Everything an employee is made of is here in plain text, so you can read it before you hire it: its prompt, principles,
examples and the scripts of its skills.

## How it reaches harnsy

1. An employee is added here by a pull request (see [CONTRIBUTING.md](CONTRIBUTING.md)).
2. The automatic check runs on the pull request; it only reads files and never runs anything from the pull request.
3. The harnsy HR agent (an AI) reviews it; a person makes the final decision and merges.
4. Within an hour our server takes the merged commit, checks it again, signs it with the catalog key and publishes it
   on hr.harnsy.dev. The signing key never leaves our server.

## Layout

```
employees/<publisher>/<name>/<version>/   one employee version: bundle.json, listing.json, avatar, docs/, skills/
publishers/<publisher>.json               the publisher: shown name, description, GitHub login(s)
revoked.json                              withdrawn versions
tools/check/                              the automatic check (Go)
```

A published version never changes; a change is a new version folder.

Run the check yourself:

```
cd tools/check && go run . --dir ../..
```

## Licences

Employee texts: CC BY 4.0 unless stated otherwise; scripts in skills: MIT, Apache-2.0 or CC0; tools: MIT. Details and
exceptions in [LICENSE](LICENSE).

Questions and appeals: open an issue or write to hello@harnsy.dev.
