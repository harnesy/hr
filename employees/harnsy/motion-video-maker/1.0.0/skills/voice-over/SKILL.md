---
name: voice-over
description: Write a narration script that is easy to say and voice it line by line with the hirer's text-to-speech engine (ElevenLabs with the hirer's key, the hirer's OpenAI-compatible speech server, or Kokoro on the CPU as the no-key fallback, which downloads models on first use), then measure, normalise and join the narration. Use when an animated video needs a voice-over, or a line of an existing one changed.
---

# Voice-over

The narration carries the message; the picture follows it. This skill writes the words so they are easy to say and easy to follow, turns them into one audio file per line with the engine the hirer has set up, and joins them into a single narration track with measured loudness.

**Route:** request → **voice-over** (script, voice, narration) → **scene-sync** (timing, captions) → **remotion-composition** (stills, render) → **scene-sync** (web files, lengths) → hand-over.
Before this skill: an approved message or copy from the copywriter or product marketing manager. After it: `scene-sync` measures the lines and times the scenes; the narration is joined with `mix.py` once the timing file exists.

## When to use

- A new animated video needs a voice-over.
- A line changed: voice that line again, then let `scene-sync` re-time.
- The hirer asks to switch engine or voice: a new voice means every line again, never a mix of two voices in one video.

## Inputs

- Approved copy or key messages, the audience, the target length.
- The engine settings from the hirer (below). No engine, voice or model is chosen by this skill.
- Tools: Python 3, ffmpeg and ffprobe (the hirer installs them). For Kokoro only: the hirer's Python environment with `kokoro` and `soundfile` installed (Python 3.10 to 3.12 for the current release).

## Engines, in this order

The script `scripts/tts.py` takes the first engine that is fully set up, or the one named with `--backend`. All settings come from the environment, or from a `KEY=VALUE` file the hirer keeps outside the project (`--env-file`).

1. **ElevenLabs** (primary, the hirer's account): `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`, `ELEVENLABS_MODEL_ID`; optional `ELEVENLABS_BASE_URL` (default `https://api.elevenlabs.io`, for regional servers) and `ELEVENLABS_OUTPUT_FORMAT` (default `wav_24000`). The hirer picks a voice from their account or the Voice Library (https://elevenlabs.io/app/voice-library) and a model from the publisher's list (https://elevenlabs.io/docs/models).
2. **The hirer's speech server** (alternative): any server with an OpenAI-compatible `POST /v1/audio/speech`, self-hosted or hosted: `TTS_BASE_URL` (usually ending in `/v1`), `TTS_MODEL`, `TTS_VOICE`, optional `TTS_API_KEY`. Voices and models are listed in that server's own documentation.

Keys through harnsy: when the hirer keeps a key in harnsy (Settings > Keys), set `ELEVENLABS_KEY_NAME` or `TTS_KEY_NAME` to the key's name there (for example `elevenlabs`, `tts-endpoint`) and leave `ELEVENLABS_API_KEY` / `TTS_API_KEY` unset. `tts.py` then sends the request through harnsy's key proxy on this machine (its address in `HARNSY_AGENT_ADDR`, the seat token in `HARNSY_PROXY_TOKEN`, both set by harnsy) to the same path on the real host, and harnsy adds the key: you never see it. The hirer allows the key's host for that key in harnsy. The proxy calls only public https hosts: a speech server on this machine or the hirer's network (an address without https, `localhost`, a private address) cannot go through it, and `tts.py` refuses that combination with a clear message; for such a server leave `TTS_KEY_NAME` unset and put its key, if it has one, in `TTS_API_KEY`.
3. **Kokoro-82M on the CPU** (no-key fallback): `KOKORO_VOICE`, optional `KOKORO_LANG`. Voices are listed by the publisher in `VOICES.md` of the model repository (https://huggingface.co/hexgrad/Kokoro-82M; American and British English among them; no Russian).

When a setting is missing, `tts.py` names the missing setting (never its value) and moves to the next engine; with `--backend` it stops and says which fallback to try. A failed request stops the run; it never switches engine halfway.

**Network.** The only request the scripts make is the speech request to the engine the hirer configured. Text sent to ElevenLabs, or to a `TTS_BASE_URL` outside the hirer's machine or private network, leaves the hirer's network: `tts.py` refuses to send it without `--cloud-ok`, which you pass only after telling the hirer where the text goes and getting a yes. When the engine is ElevenLabs, also say: ElevenLabs' Terms give it a licence to the script text and the audio to improve its services unless the account holder has opted out in the account's Data use settings; a confidential or unreleased script should not be sent unless the hirer decides so; the Terms that apply differ for accounts in the EEA, Switzerland or the UK. A key goes only over https, or to a server on this machine or network: `tts.py` refuses to send a key over plain HTTP to any other host and does not follow redirects on a keyed request.

**First use downloads (Kokoro).** Ask before running it the first time, and list: the `kokoro` package with its dependencies, PyTorch included (pip, from the Python package index; a CPU-only PyTorch build keeps it smaller), the model weights and one voice file (about 315 MB, from the Hugging Face hub) and a small English language model for the spaCy library (fetched by pip on first use). Its English phoneme fallback is espeak-ng (GPL-3.0), which arrives inside the `espeakng-loader` package; nothing of it is bundled here. If you ship an image or package that contains these libraries, the GPL-3.0 duties (licence text, source) are yours.

## Steps

1. **Script.** Write plain spoken lines: short sentences, active voice, everyday words, one idea a line, no jargon a listener cannot see spelled. Numbers as they are said («about two minutes», «three out of four»). Budget the length: about 150 words a minute, never above 180. Leave room for what the picture must say, or say it in the line.
2. **Claims.** Every factual claim comes from approved copy. A new or changed claim goes back to the copywriter or product marketing manager before voicing.
3. **Script file.** Write `script.json`: scenes in order, each with its lines (`id`, `text`); a scene without voice has `seconds` instead.
4. **Engine check.** `python3 scripts/tts.py script.json --out audio --dry-run` shows which engine would be used and what is missing, without sending anything. If it is a cloud engine, tell the hirer how many lines go where, and wait for a yes.
5. **Test line.** Voice one line first (`--only <id>`), check it is audio and not an error, measure it (step 7), and ask the hirer to listen to it.
6. **All lines.** `python3 scripts/tts.py script.json --out audio [--cloud-ok]`: one WAV per line, its length and words a minute, and `audio/tts-log.json` (engine, host, voice setting, no keys). A line above 180 words a minute is rewritten, not sped up.
7. **Measure.** `python3 scripts/loudness.py measure audio/*.wav`: integrated loudness, true peak, range, sample peak, clipped samples and long silences per file. Lines under 3 s give shaky integrated values; the joined track is what counts.
8. **Join** after `scene-sync` has written `timing.json`: `python3 scripts/mix.py timing.json --audio audio --out narration-raw.wav` places every line at its start time and makes the track exactly as long as the video. A music bed only with a licence on record (`--music`, lowered with `--music-db`).
9. **Normalise.** `python3 scripts/loudness.py normalize narration-raw.wav narration.wav` (two passes; default -16 LUFS integrated, -1 dBTP; `--target -23` for broadcast or the hirer's own figure). Then ask the hirer to listen to the whole narration.

## Voices and consent

- Never a voice that imitates a real, named person; never a «sounds like» request.
- A cloned voice only from a recording of a speaker who agreed in writing, and only through ElevenLabs under its rules or Chatterbox (MIT; its output carries an inaudible watermark, by the publisher's statement). Keep the consent on record with the licence list; never remove or hide a watermark.
- The hirer selects the model on the speech server and holds its licence: ask which model runs and where its licence is, and record it. For example, Qwen3-TTS weights are published under Apache-2.0, while Orpheus weights are tagged Apache-2.0 but built on Llama 3.2, whose community licence and use policy may apply. Such questions go to the contract reviewer or the hirer's lawyer.
- English is the supported language. Another language is best effort: the hirer's ElevenLabs or speech server engine if it lists that language, one test line for the hirer to judge, no claim about quality. Kokoro has no Russian.
- A shared Voice Library voice is the hirer's choice from the hirer's account: record its id and notice period. Its owner can withdraw it (see the notice period); the voice-over WAV files you keep stay usable, so keep every line file; the no-imitation rule covers library voices too.
- On the free plan ElevenLabs may be used only for non-commercial purposes (Terms, read 16 October 2026) and Voice Library voices are not available through the API; a video for a business needs a paid plan, which the hirer holds.
- Never use ElevenLabs audio as a reference clip, training data or input for another voice engine or model: its Prohibited Use Policy forbids it.
- Never remove, alter or hide a watermark or provenance mark of any engine.
- Stop and call a person when the video is for a government body or for political campaigning (ElevenLabs needs written approval for such use); never the voice of a deceased person without the consent of the heirs or estate.

## Checks before hand-over

- Every line has a WAV; none above 180 words a minute; no clipped samples; no unplanned silence of 2 s or more.
- The narration track is within 1 LU of the target and at or below the true-peak ceiling, as printed by `loudness.py`.
- `tts-log.json` names the engine; no key appears in any file (search the output folder for the key's first characters if unsure).
- The hirer has listened to the test line and to the final narration.

## Artefacts

- `script.json` and a readable copy of the script.
- `audio/<line id>.wav`, `audio/tts-log.json`, `narration.wav`, the loudness printout.
- A licence row: engine, voice id or name, the terms it runs under (the hirer's ElevenLabs plan, the speech model's licence, or for Kokoro: Kokoro weights Apache-2.0; espeak-ng GPL-3.0), consent record if cloned.

## Hand-over

- **To the owner:** the narration to listen to, its numbers, and a note that the voice is generated and which engine made it.
- **To the copywriter or product marketing manager:** every changed line, before it is voiced.
- **To `scene-sync`:** the line WAVs and `script.json`.

## Sources

- Section508.gov, U.S. General Services Administration (US government work): speaking pace and caption-friendly narration. Adapted.
- 18F Content Guide, 18F, U.S. General Services Administration (CC0 1.0): plain language, concise lines, active voice, numbers. Adapted for speech.
- Facts only, read 16 October 2026: OpenAI API specification (MIT) and vLLM-Omni docs (Apache-2.0) for the speech request; ElevenLabs API reference, Terms of Service, Prohibited Use Policy and Voice Library Addendum; Kokoro-82M model card (Apache-2.0); Chatterbox README (MIT); FFmpeg loudnorm documentation; EBU R 128 and Apple Podcasts audio requirements for the loudness targets.
- Independent tool; not affiliated with or endorsed by Remotion, ElevenLabs or the model publishers.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Scripts in scripts/ are under the MIT licence (see LICENSE). The names «harnsy» and «hr.harnsy.dev» are not covered by these licences.
