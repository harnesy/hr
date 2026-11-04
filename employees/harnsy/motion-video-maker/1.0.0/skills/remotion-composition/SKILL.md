---
name: remotion-composition
description: Build a new Remotion project, or add to one, for a short animated video: one component per scene, lengths from the timing file, licensed assets in public/, a still of every scene checked before the full render to MP4 and WebM. Use when the narration is timed and the picture must be built or re-rendered, after the hirer has confirmed the Remotion licence.
---

# Remotion composition

The picture is code: every scene is a component, every length comes from data, and anyone can render it again. This skill builds or extends the project, checks one still of every scene, and renders the video.

**Route:** request → **voice-over** (script, voice, narration) → **scene-sync** (timing, captions) → **remotion-composition** (stills, render) → **scene-sync** (web files, lengths) → hand-over.
Before this skill: `scene-sync` (`timing.json`) and the narration from `voice-over`. After it: `scene-sync` checks the web files.

## When to use

- A timed narration exists and the picture must be built.
- The script or timing changed and the video must be rendered again.
- A new destination needs another shape (16:9, 1:1, 9:16) of the same video.

## Inputs

- The hirer's answer on the Remotion licence (step 1). No render before it.
- Destination, shape, frame size and frame rate; `timing.json`; `narration.wav`.
- Brand assets from the presentation designer or ui designer; every font, image, icon and music file with its licence.
- Tools: Node.js 16 or newer, npx, Python 3, ffprobe.

## Steps

1. **Licence first.** Quote the free groups of the Remotion License as read on 16 October 2026 (an individual; a non-profit; a for-profit organisation with up to 3 employees; someone evaluating it without commercial use yet), say that Remotion's Terms and FAQ count everyone in the organisation, part-timers and contractors included, and can add a client who owns or runs the project, that they define non-profit narrowly, that a real video for a business is not an evaluation, and that a paid Company License is per person who uses Remotion, also through an AI agent like you, so everyone else needs one and the terms may change (Remotion 5.0 is announced); then ask the hirer which applies and wait for the answer. Write the answer into the licence list. Never say the hirer is covered; never buy a licence. Doubts go to the contract reviewer or the hirer's lawyer.
2. **Ask before installing.** A new project (`npx create-video@latest`) or `npm install` fetches packages from the npm registry, and the first still or render downloads a headless browser into `node_modules` (`npx remotion browser ensure` does it ahead). List this and wait for the hirer's yes. Inside the hirer's own repository, use its existing setup.
3. **Shape.** One composition per destination: width, height (even numbers), fps from `timing.json`, length `total_frames` from `timing.json`, never a typed number.
4. **Scenes.** One component per scene, placed in sequence with the frame counts from `timing.json`; text and numbers come in as props or data, not baked into graphics. Motion from the current frame (fades, slides, springs), nothing that flashes more than three times a second. Keep the bottom third free for captions.
5. **Assets.** Copy each file into `public/` and load it with `staticFile()`; add one row per file to the licence list (name, source, licence, credit line if required). Fonts keep their own licence (for example an OFL file); anything without a licence stays out. The narration is `public/narration.wav`.
6. **Plan.** `python3 scripts/plan.py public/timing.json --entry src/index.ts --comp <Name> --size 1920x1080 --audio public/narration.wav` checks the timing and the narration length and prints the still and render commands; it runs nothing itself.
7. **Stills.** Run one `npx remotion still … --frame=<n>` per scene and look at every image: text spelled right and readable, numbers as approved, enough contrast, nothing in the caption area, brand assets as supplied. Show the stills to the owner if the look is new.
8. **Preview** in `npx remotion studio` when the owner wants to scrub through (a preview, not a render).
9. **Render** both formats with the printed commands: MP4 with H.264 and WebM with VP9. Note frames, fps, duration and file size from the output.

## Checks before hand-over

- The licence answer is written down with its date and who gave it.
- `plan.py` prints `ok`; every still was looked at; the stills match the final render at those frames.
- Both files render without errors; their length is `duration_s` from `timing.json` (checked by `scene-sync`).
- The licence list has a row for every file in `public/` and for the voice.

## Artefacts

- The project source (or the changes in the hirer's repository) with the render commands.
- `out/still-<scene>.png`, `out/<Name>.mp4`, `out/<Name>.webm`, the render log.
- The licence list: Remotion status, voice engine and voice, fonts, music, images, icons.

## Hand-over

- **To `scene-sync`:** the rendered files for size, length and caption checks.
- **To the owner:** stills, renders and the licence list, with a note that the voice is generated and which engine made it.
- **To the frontend developer:** the project and render commands when the video is rebuilt from data on their side.
- **To the video director:** any request for real screen recordings of the product.

## Sources

- Section508.gov, U.S. General Services Administration (US government work): on-screen text and caption area. Adapted.
- Social media playbook, GDS, © Crown copyright (OGL v3.0): shape and captions per destination. Adapted. Contains public sector information licensed under the Open Government Licence v3.0.
- Facts only, read 16 October 2026: the Remotion License, licence FAQ and Terms and Conditions (Remotion AG); command and function names from the Remotion documentation, in our own steps.
- Independent tool; not affiliated with or endorsed by Remotion, ElevenLabs or the model publishers.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Scripts in scripts/ are under the MIT licence (see LICENSE). The names «harnsy» and «hr.harnsy.dev» are not covered by these licences.
