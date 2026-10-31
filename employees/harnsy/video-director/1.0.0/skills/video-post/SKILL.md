---
name: video-post
description: Turn a recorded browser take into a master video and web files (AV1, VP9, MP4) with a poster frame, within the size and format targets of the page that shows it; fit existing caption files to the new take. Use after a clean take exists and before captions are finalised and handed over.
---

# Video post-production

**Route:** request → video-storyboard → stand request → browser-take → **video-post** → captions → hand-over.
Before this skill: `browser-take` (a take folder that passed the frame check). After it: `captions`.

## When to use

- A clean take exists and needs a master, web files and a poster.
- The take was redone and existing caption files must be checked against (or fitted to) the new shot marks.

## Inputs

- The take folder from `browser-take` (`frames/`, `frames.json`).
- Targets for the page, written down before encoding: formats (AV1, VP9, MP4), maximum size of each file, poster size, frame size, whether there is sound.
- The poster moment from the storyboard.
- Tools: see «Tools» below (ffmpeg with libsvtav1, libvpx-vp9, libx264 and libwebp; Python 3).

## Steps

1. **Assemble:** `python3 scripts/assemble.py take1 --poster-at <s>`.
   Makes a constant-frame-rate near-lossless master that starts on the first shot and ends on the last boundary, a contact sheet (the middle of each shot plus the poster), `marks.txt` and `chapters.json`.
   Any `OFF:` line means a mark is more than the tolerance from its plan: go back to `browser-take`.
2. **Look at the contact sheet.** Every shot shows what the storyboard says; the poster reads well as a still.
3. **Encode:** `bash scripts/encode.sh take1/master.mp4 out --name <name> --poster-at <s> --max-mb av1=…,vp9=…,mp4=…,poster=…`.
   Any `OVER` line: raise the CRF a step, or reduce `--width`, and encode again. Compare a crop of small text in each file against the master; if text smears, the CRF is too high.
4. **Existing captions** (when the caption files were written before this take): `python3 scripts/retime.py check take1 <files>.vtt --copy-to out`. A mismatch means retake, or ask the caption owner for new times. Use `retime.py retime` only with the caption owner's agreement.
5. **Keep the master** outside the repository and outside the files that are served. It is the source for any later re-encode and for short cuts.

## Checks

- No `OFF:` from `assemble.py`, no `OVER` from `encode.sh`.
- Duration of each web file equals the last mark (check with `ffprobe`).
- Small text is readable in every format at the size the page shows it.
- The poster contains no secret or personal data and shows a real screen of the product.
- No audio track unless the brief asked for sound. If there is music or a voice, it is licensed for this use, and no synthetic voice imitates a real person.
- Fonts in any title card are licensed for video use.

## Artefacts

- `out/<name>.av1.webm`, `out/<name>.vp9.webm`, `out/<name>.mp4`, `out/<name>-poster.webp`, `out/<name>-poster.jpg`.
- `take1/master.mp4`, `take1/contact.png`, `take1/marks.txt`, `take1/chapters.json`.
- A note with the sizes, the encoder settings used, and the poster time.

## Hand-over

- **To the captions step** (`captions`, with the copywriter or editor): `marks.txt` and the shot file.
- **To the frontend developer** (after captions): the web files, the poster, the caption files, `chapters.json`, and the page behaviour the brief asked for (no autoplay, `preload="none"`, default caption track in the page language, chapters that seek). The master stays out.
- **To the owner:** the contact sheet and the note. The video is never published or uploaded by this skill.

## Tools

`scripts/assemble.py` builds the master, contact sheet, marks and chapters; `scripts/encode.sh` makes the web files and poster; `scripts/retime.py` fits existing caption files to a take.

### Requirements

Check what your machine has:

```sh
ffmpeg -version | head -1
ffmpeg -hide_banner -encoders | grep -E 'libsvtav1|libvpx-vp9|libx264|libwebp'
python3 --version       # Python 3, standard library only
bash --version | head -1
```

- **ffmpeg** with the encoders above (on Debian or Ubuntu: `apt install ffmpeg`). The scripts call it; nothing from it is copied here.
- A format whose encoder is missing can be left out: `--formats vp9,mp4`.

### Example

Continues from `../browser-take/SKILL.md` («Tools») (a take in `work/take1`):

```sh
python3 scripts/assemble.py work/take1 --poster-at 2.0
bash scripts/encode.sh work/take1/master.mp4 work/out --name demo --poster-at 2.0 \
  --max-mb av1=0.5,vp9=0.5,mp4=0.5,poster=0.06
```

Then write the caption files with `../captions/scripts/vtt.py` (see `../captions/SKILL.md`):

```sh
python3 ../captions/scripts/vtt.py write work/take1 \
  --shots ../video-storyboard/scripts/shots.example.json --out work/out --name demo
python3 ../captions/scripts/vtt.py lint work/out/demo.*.vtt
```

If caption files already exist from an earlier take:

```sh
python3 scripts/retime.py check work/take1 old/demo.en.vtt old/demo.es.vtt --copy-to work/out
```

Exit codes: `assemble.py` 3 = `OFF:` marks or take warnings; `encode.sh` 3 = a file over its target; `retime.py check` 1 = mismatch.

### Encoder defaults

| Format | Settings | Note |
|---|---|---|
| AV1 (WebM) | SVT-AV1 CRF 44, preset 5, GOP 150 | smallest; first `<source>` |
| VP9 (WebM) | CRF 34, constant quality | above about 34, screen text ghosts |
| H.264 (MP4) | CRF 28, preset slow, faststart | fallback for every browser; `--still` for mostly still screens |
| Poster | WebP quality 80, JPEG q 4 | one real frame of the product |

Heavy machines shared with others: encode one format at a time (the default); `--parallel` runs all three at once.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Scripts in scripts/ are under the MIT licence (see LICENSE). The names «harnsy» and «hr.harnsy.dev» are not covered by these licences.
