---
name: browser-take
description: Record a scripted screen take of a web product in a headless browser, shot by shot on the approved cue boundaries, on a demo stand with made-up data, then check every frame for secrets and personal data. Use after a storyboard and shot file are approved and the demo stand is up.
---

# Browser take

A take is one scripted run through the product, recorded frame by frame with exact timestamps.
The script pads every shot to its planned end, so captions and chapters fit without editing.

**Route:** request → video-storyboard → stand request → **browser-take** → video-post → captions → hand-over.
Before this skill: `video-storyboard` (approved `shots.json`) and a running demo stand. After it: `video-post`.

## When to use

- A shot file is approved and a demo stand is ready.
- A take must be redone: a shot ran late, a frame shows something it must not, or the product changed a label.

## Inputs

- `shots.json` from `video-storyboard`, approved by the owner.
- The demo stand's URL. The stand is prepared and owned by others (the product's developers), runs on made-up data, and can be reset between takes.
- Tools: see «Tools» below (Node.js, Playwright with Chromium, Python 3).

## Never

- Never record a live account, production data, or a real customer's workspace. Only the demo stand.
- Never type, paste or show a real key, token or password on camera. If the stand needs a licence or key, it is set off camera by the stand owner.
- Never fake the product: no edited numbers, no injected UI, no screens the build cannot show. The script may add only the drawn cursor, a push-in (zoom), honest labels ("sample data", "sped up"), and a blur over an incidental detail (a version string, a clock). Never use blur or labels to change what the product says.
- Never publish or upload the take anywhere.

## Steps

1. **Rehearse.** Run the take with `--until <first shots>` and `--headed`, fix targets that do not match, and confirm every screen in the storyboard exists on this build.
2. **Reset the stand** the way the stand owner described (state changes in a take cannot be undone by the script).
3. **Record:** `node scripts/take.mjs --shots shots.json --out take1 --base-url <stand URL>`.
   Any `WARN` line means a shot ran late or an action failed: reset and retake. One clean take per run; do not stitch partial takes unless the storyboard says so.
4. **Check the frames:** `python3 scripts/check-frames.py take1 --deny names.txt`.
   - Fix every `FOUND` line (retake, or ask the stand owner to change the data).
   - Look at every frame in `take1/review/` for what text scanning cannot see: images, canvas, terminal output, browser chrome, notifications.
5. **Hand over** the take folder to `video-post`.

## Checks

- `take.mjs` exited 0: no `WARN`, every mark on its target.
- `check-frames.py` exited 0, and every review frame was looked at.
- No key, token, password, e-mail, phone, real person's or real customer's name, account picture or private URL in any frame.
- The screens match the storyboard; any difference is reported to the owner with the reason (the screen wins over the storyboard, the caption follows the screen).
- Staged parts carry the label promised in the storyboard.

## Artefacts

- `take1/frames/*.jpg`, `take1/frames.json` (frame times, marks, targets, warnings), `take1/texts.json` (visible page text per shot), `take1/review/` (frames for the privacy check).
- A short take note: the stand build, the date, warnings, and any difference from the storyboard.

## Hand-over

- **To the post-production step** (`video-post`, often the same recorder): the take folder and the take note.
- **To the stand owner:** "recording done, the stand can be stopped", once the owner of the video has accepted the cut.
- **To the owner:** any difference between the screen and the storyboard that changes a caption.

## Tools

`scripts/take.mjs` records a scripted take; `scripts/check-frames.py` checks it for secrets and personal data.

### Requirements

Check what your machine has; no fixed versions are required beyond what Playwright itself needs:

```sh
node --version          # Node.js with ES modules and node:util parseArgs (18 or newer)
npx playwright --version
python3 --version       # Python 3, standard library only
```

- **Playwright** (`playwright` or `playwright-core`) with a Chromium build. The scripts import it; nothing from it is copied here.
- The screencast uses the Chrome DevTools Protocol, so the browser must be Chromium or Chrome.

### Install

```sh
mkdir -p ~/video-tools && cd ~/video-tools
npm init -y && npm i playwright
npx playwright install chromium
```

Run `take.mjs` from that folder (so `playwright` resolves), or pass `--playwright /path/to/playwright-core/index.mjs`.
To use an installed Chrome instead of Playwright's Chromium: `--browser /path/to/chrome`.

### Example

The sample shot file is in `../video-storyboard/scripts/shots.example.json`. It expects a small page with a project list; any page with the same labels works.

```sh
node scripts/take.mjs --shots ../video-storyboard/scripts/shots.example.json \
  --out work/take1 --base-url http://localhost:8000/
python3 scripts/check-frames.py work/take1 --deny names.txt --allow '@example\.(com|org)$'
```

Exit codes: `take.mjs` 0 = clean, 3 = warnings (retake), 2 = bad arguments. `check-frames.py` 0 = nothing found, 3 = findings.
Then continue with `../video-post/SKILL.md` («Tools»).

### Shot file reference

Top level: `baseUrl`, `start` (path opened first), `viewport` `{width, height}`, `deviceScaleFactor`, `colorScheme`, `locale`, `cursor` (draw the soft cursor, default true), `zoom` (default push-in scale), `zoomRoot` (CSS selector scaled by a push-in, default `body`), `localStorage` (keys set before every page load), `prelude` (actions off camera), `ready` (a target to wait for before recording), `poster` (seconds; used by `video-post`), `shots`.

Shot: `id`, `title`, `end` (seconds from the start of the video) or `duration`, `caption` (string or `{lang: text}`), `actions`.

Target (in `target`, or directly on the action): one of `role` + `name`, `label`, `placeholder`, `testId`, `text`, `selector` (last resort); optional `exact`, `hasText`, `nth`.

| `do` | Fields | What it does |
|---|---|---|
| `goto` | `url` | open a path relative to `baseUrl` |
| `point` | target | move the drawn cursor onto the target |
| `hover` | target | point, then a real hover |
| `click` | target, `after` | point, press animation, click |
| `type` | target, `text`, `delay` | click the field, type key by key |
| `press` | `key` | a key, e.g. `Enter` |
| `wait` | target or `ms`, `state`, `timeout` | wait for an element or a time |
| `waitText` | `pattern` | wait until the page text matches a regex |
| `hold` | `ms` | keep the screen still |
| `scroll` | `dy` | wheel scroll in the middle of the page |
| `zoom` / `unzoom` | target, `scale`, `ms` | push in on a target with a CSS transform / back out |
| `label` | `text`, `corner` | an honest on-screen label; `text: null` removes it |
| `blur` | target, `px` | blur an incidental detail (version string, clock) |
| `cursor` | `x`, `y` | move the drawn cursor to a point |
| `exec` | `cmd` (array), `timeout` | run a local command, e.g. the stand's own step script; needs `--allow-exec` |

Use `--allow-exec` only with a shot file you wrote or read yourself: an `exec` action runs a command on your machine.

Every action may have `at` (seconds from the shot's start: wait until then), `settle` (ms after pointing), and `optional: true` (a failure is a warning, not the end of the take).

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Scripts in scripts/ are under the MIT licence (see LICENSE). The names «harnsy» and «hr.harnsy.dev» are not covered by these licences.
