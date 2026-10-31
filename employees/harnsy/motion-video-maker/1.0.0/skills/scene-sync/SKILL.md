---
name: scene-sync
description: Turn measured narration into scene lengths in frames, a timing file for the composition, WebVTT captions and a transcript from the script text; after the render, check web files, poster and lengths against written targets. Use when voiced lines exist and the video must be timed, captioned or checked before hand-over.
---

# Scene sync

A scene lasts as long as its words take to say. This skill measures every voiced line, turns the lengths into whole frames, writes the timing file the composition reads, and builds captions and a transcript from the script text itself, so no speech recognition is involved. After the render it checks the web files against written targets.

**Route:** request → **voice-over** (script, voice, narration) → **scene-sync** (timing, captions) → **remotion-composition** (stills, render) → **scene-sync** (web files, lengths) → hand-over.
Before this skill: `voice-over` (line WAVs, `script.json`). After it: `remotion-composition` reads `timing.json`; `voice-over` joins the narration with it. After the render, this skill runs again for the web files.

## When to use

- Lines are voiced and the scenes need their lengths.
- A line was re-voiced: re-time everything after it.
- Captions or a transcript are needed, or must be checked against a new render.
- Rendered files must be checked for size, length and audio before hand-over.

## Inputs

- `script.json` and `audio/<line id>.wav` from `voice-over`.
- Frame rate agreed with the hirer (30 unless the project says otherwise); lead-in before the first line of a scene, gap between lines, tail after the last.
- Size targets for each web file, written down before encoding.
- Tools: Python 3, ffprobe. No network access.

## Steps

1. **Timing.** `python3 scripts/sync.py timing script.json --audio audio --fps 30 --out timing.json`. Each scene = lead-in + its lines with gaps + tail, rounded up to whole frames; a scene without voice keeps its `seconds`. The file lists every scene's first frame and length, and every line's start and length in seconds.
2. **Check the total** against the agreed length. Too long: shorter lines from the copywriter, never a faster voice or cut pauses below what a listener needs.
3. **Captions.** `python3 scripts/sync.py vtt timing.json --out captions.vtt --transcript transcript.txt`. One cue per line, split into cues of at most two rows of about 42 characters, times shared by text length.
4. **Lint.** `python3 scripts/sync.py lint captions.vtt`: header, timing format, order, overlaps, rows, characters per row, words a minute (180 at most). Fix the text or the scene, not the timing.
5. **After the render**, lint again with `--video out/<name>.mp4`: the last cue must end before the video does.
6. **Web files.** WebM (VP9) listed first, MP4 (H.264) as the fallback, a poster image, and a silent version without an audio track when the video will loop muted in a feed. Check: `python3 scripts/webcheck.py --target out/<name>.webm=4MB --target out/<name>.mp4=6MB --target out/poster.jpg=150KB --seconds <duration_s from timing.json> [--silent out/<name>-silent.webm]`.

## Caption rules

- Every spoken word and any sound the viewer needs; the same style throughout; no scrolling or flashing.
- At most two rows; on-screen text stays in the upper two thirds so captions never cover it.
- Captions are a separate WebVTT file by default; burned-in captions only when the hirer asks (a muted feed clip), and named as burned-in in the hand-over.
- Captions are in the language spoken; translations are subtitles from the localization manager or translator, with the same cue ids.

## Checks before hand-over

- `timing.json` total equals the sum of the scenes; every line ends inside its scene.
- `sync.py lint` prints `ok`, also against the rendered video.
- `webcheck.py` prints `ok`: sizes within targets, every video within one frame of `duration_s`, silent files without audio.
- Narration length equals video length (see `voice-over`, `mix.py`).

## Artefacts

- `timing.json`, `captions.vtt`, `transcript.txt`.
- The `webcheck.py` and `lint` printouts with sizes and durations.

## Hand-over

- **To the frontend developer:** the web files in source order (WebM, then MP4), the poster, `captions.vtt` as the default track, the transcript for the page, and a note: no autoplay with sound; a user-started video does not need to be fetched ahead.
- **To the localization manager or translator:** the script, the cue ids and timings for other languages.
- **To `remotion-composition`:** `timing.json`.

## Sources

- Section508.gov, U.S. General Services Administration (US government work): captions and transcripts. Adapted.
- web.dev Learn Performance and Learn Accessibility, © Google LLC (CC BY 4.0): video formats, poster, preload, silent clips; captions, subtitles and transcripts. Adapted.
- Facts only: W3C WebVTT (cue format), FFmpeg ffprobe documentation.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Scripts in scripts/ are under the MIT licence (see LICENSE). The names «harnsy» and «hr.harnsy.dev» are not covered by these licences.
