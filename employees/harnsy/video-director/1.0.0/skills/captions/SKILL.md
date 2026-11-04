---
name: captions
description: Write and check per-language caption files (WebVTT) for a recorded product video, timed on the take's shot marks, readable and true to what the screen shows. Use when a take is assembled and its captions must be produced, translated, re-checked after a retake, or reviewed for readability.
---

# Captions

Captions carry the message when the video has no sound, and make it accessible when it has one.
They say only what the screen shows.

**Route:** request → video-storyboard → stand request → browser-take → video-post → **captions** → hand-over.
Before this skill: `video-post` (`marks.txt`) and the shot file from `video-storyboard`. After it: hand-over to the frontend developer and the owner.

## When to use

- A take is assembled and needs caption files in one or more languages.
- A retake moved the shot marks, or the wording changed.
- Someone asks whether existing captions are readable.

## Inputs

- `marks.txt` from `video-post` and `shots.json` from `video-storyboard` (caption text per shot and language).
- The copywriter's or editor's final wording. The recorder drafts; the copywriter owns the words.
- The page's style: caption position, font size, colours.
- Tool: Python 3 (no extra packages).

## Steps

1. **Compare the screen with the text.** Watch the master. If the screen shows something different from the caption (a label renamed, a step the product skips), the caption follows the screen. Send the change to the copywriter, and to the owner if it changes the message.
2. **Get the final wording** from the copywriter or editor for every language, and put it in `shots.json`.
3. **Write the files:** `python3 scripts/vtt.py write take1 --shots shots.json --out out --name <name>`.
   One cue per shot, timed on the marks, ids equal to the shot ids, lines broken at about 32 characters.
4. **Lint:** `python3 scripts/vtt.py lint out/<name>.*.vtt`. Fix every problem by shortening the text or splitting the shot in the storyboard; do not squeeze the timing.
5. **Check in a player** at the size the page shows the video: the default track is the page language, and each cue is readable before it changes.

## Readability rules

- At most 2 lines per cue, about 32 characters per line.
- Reading speed at most 160–180 words per minute; at least 1 second on screen.
- Readable size and contrast: on a solid or semi-opaque background, at least 4.5:1 contrast between text and background; size set by the page's `::cue` style, not burnt into the video.
- No flashing: no cue or on-screen label blinks or flashes, and nothing in the video flashes more than three times a second.
- Captions cover what is spoken and every on-screen text the viewer needs to follow (a label that is too small to read, a key message in a terminal).
- Exact interface labels are kept as the screen shows them, in quotes if needed.
- The same cue ids in every language, so chapters and analytics line up.

## Checks

- `vtt.py lint` prints `ok` for every file.
- Each caption says only what the screen shows; nothing promises a feature the build does not have.
- The copywriter or editor approved the wording in every language.
- Files are UTF-8, start with `WEBVTT`, and the page serves them as `text/vtt`.

## Artefacts

- `out/<name>.<lang>.vtt` for every language.
- Chapter list for the page (from `chapters.json` in `video-post`, titles translated).

## Hand-over

- **To the frontend developer:** the caption files with the web files, poster and chapters from `video-post`, and the page's default caption language.
- **To the owner:** the finished set for a last look on a test page. The owner, not this skill, publishes or uploads the video.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Scripts in scripts/ are under the MIT licence (see LICENSE). The names «harnsy» and «hr.harnsy.dev» are not covered by these licences.
