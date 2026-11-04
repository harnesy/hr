---
name: video-storyboard
description: Turn a request for a product video (a demo, a how-to, a launch video, a short cut for social) into a storyboard the owner approves and a shot file the recording uses. Use when someone asks for a screen-recorded video of a web product and nothing is recorded yet, or when the product changed and an old video must be re-shot.
---

# Video storyboard

The storyboard is the contract for the video. Nothing is recorded until the owner says yes to it.
It produces two things: a storyboard document for people, and a shot file (JSON) for the recording script.

**Route:** request → **video-storyboard** → stand request → browser-take → video-post → captions → hand-over.
Before this skill: a request from the owner. After it: the demo stand request, then `browser-take`.

## When to use

- Someone asks for a video of a web product: a short loop for a landing page, a step-by-step guide, a launch video, cuts for social posts.
- The product's screens changed enough that an existing video no longer matches them.

## Inputs

Ask the owner for a brief. Do not start the storyboard without these:

- **Audience:** who watches, and what they already know.
- **Message:** the one thing a viewer should take away.
- **Length:** a target, and the hard limit of the place where it runs (a page, a social network's limit for cuts).
- **Languages:** for captions; which language is on screen.
- **Where it is shown:** the page or channel, autoplay or not, sound or not, chapters or not, the size budget for the files.
- **Source of facts:** the product build or document that says what the product really does today.

## Steps

1. **Read the facts.** Walk the real product (or its code and docs) for every screen you plan to show. Write down exact labels, button names and counts as the screen shows them. The video shows only what the build really does.
2. **Write the storyboard** (a document for people). For each shot: id, chapter title, start and end time, what is on screen, the caption draft, notes (push-in, label, what must not be clicked). Add:
   - what the video does **not** promise (features that do not exist, planned work);
   - honest labels you will put on screen: "sample data", "sped up · real time N min", "scripted" for staged parts;
   - the poster frame: which moment, and why it reads well as a still image;
   - what the demo stand must contain (made-up company, users, records in every state the shots need);
   - open questions, each with a default answer, so the owner can approve in one reply.
3. **Get reviews when the video is long or important.** A reader who acts as a new viewer (is every step clear, in the right order, where would someone stop watching) and an editor for the caption wording. Record what you took from each review and what you did not, and why.
4. **Get the owner's OK.** Send the storyboard with the open questions. Record the answer and the version approved. A later change to shots or captions is a new version and needs a new OK.
5. **Write the shot file** from the approved storyboard: `scripts/shots.example.json` shows the format. One shot per caption cue; the shot's `end` is the cue boundary. Use targets by role and accessible name or visible text, not CSS selectors, so the file survives a redesign.
6. **Check the shot file:** `python3 scripts/check-shots.py shots.json`.
7. **Write the stand request** for the people who run the product (see Hand-over).

## Rules of thumb (from practice)

- One idea per shot, and one caption per shot. Split a long step in two (2a, 2b) rather than writing a long caption.
- Captions at most 2 lines and about 15 words; reading speed at most 160–180 words per minute. `check-shots.py` checks the speed.
- Hold any screen the viewer must read (a diff, a form, a list) at least 3 seconds.
- Show the viewer's own effort honestly: if the viewer types answers, show them typed; if a step takes minutes, compress it and label it "sped up".
- Put the step where viewers most often give up at real speed, action by action.
- Start with the outcome (what the viewer will have at the end), and end on one place to go next.
- Short cuts for social come from the same master, cut on shot boundaries. Plan them in the storyboard, do not re-record for them.

## Checks before hand-over

- The owner approved this exact version; the approval is recorded.
- Every label in the shots and captions matches the build that will be recorded.
- Nothing in the storyboard needs real customer data, a live account, a real key or a real person's identity on screen.
- `check-shots.py` prints `ok`.

## Artefacts

- `storyboard.md`: the approved storyboard (version, date of approval, open questions with the answers).
- `shots.json`: the shot file for `browser-take`, with the captions in every language that is ready.
- The stand request.

## Hand-over

- **To the stand owner** (the developer who runs the product's demo environment): the stand request. A clean instance on made-up data, the states each shot needs, how to reset it between takes, and what must be off camera (licence screens, keys, account e-mails).
- **To the recorder** (`browser-take`): the approved `storyboard.md` and `shots.json`.
- **To the copywriter or editor** (`captions`): the caption drafts, for wording and translation.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Scripts in scripts/ are under the MIT licence (see LICENSE). The names «harnsy» and «hr.harnsy.dev» are not covered by these licences.
