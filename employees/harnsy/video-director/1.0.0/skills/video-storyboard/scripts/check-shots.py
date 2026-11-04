#!/usr/bin/env python3
# Copyright (c) 2026 Pavel Buchnev (harnsy)
# SPDX-License-Identifier: MIT
"""Check a shot file (JSON) before anyone records from it.

usage: python3 check-shots.py <shots.json> [--max-wpm 180] [--min-shot 1.5] [--langs en,es]

Checks: required fields; shot ids unique; boundaries strictly increasing; every action has a
known "do" and a target where it needs one; action "at" times fall inside their shot; captions
present for every listed language and readable in the shot's time (words per minute); the poster
time falls inside the video. Prints the shot table with start, end and length, then problems.
Exit 1 if there is any problem.
"""
import argparse
import json
import sys

ACTIONS = {'goto', 'point', 'hover', 'click', 'type', 'press', 'wait', 'waitText', 'hold', 'scroll',
           'zoom', 'unzoom', 'label', 'blur', 'cursor', 'exec'}
NEEDS_TARGET = {'point', 'hover', 'click', 'type', 'zoom', 'blur'}
TARGET_KEYS = {'role', 'label', 'placeholder', 'testId', 'text', 'selector'}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print(__doc__.strip()); return 0 if len(sys.argv) > 1 else 1
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument('file')
    ap.add_argument('--max-wpm', type=float, default=180)
    ap.add_argument('--min-shot', type=float, default=1.5)
    ap.add_argument('--langs')
    o = ap.parse_args()
    cfg = json.load(open(o.file, encoding='utf-8'))
    errs = []
    if not cfg.get('baseUrl'):
        errs.append('no "baseUrl" (it can also come from --base-url at take time)')
    shots = cfg.get('shots') or []
    if not shots:
        errs.append('no "shots"')
    langs = o.langs.split(',') if o.langs else sorted({k for s in shots if isinstance(s.get('caption'), dict) for k in s['caption']})
    seen, t = set(), 0.0
    print(f"{'id':>6}  {'start':>7}  {'end':>7}  {'len':>5}  title")
    for s in shots:
        sid = str(s.get('id', '?'))
        if sid in seen:
            errs.append(f'shot {sid}: duplicate id')
        seen.add(sid)
        end = s.get('end', t + s['duration'] if 'duration' in s else None)
        if end is None:
            errs.append(f'shot {sid}: needs "end" or "duration"'); continue
        length = end - t
        print(f'{sid:>6}  {t:7.2f}  {end:7.2f}  {length:5.2f}  {s.get("title", "")}')
        if length <= 0:
            errs.append(f'shot {sid}: ends at {end} s, not after {t} s')
        elif length < o.min_shot:
            errs.append(f'shot {sid}: {length:.2f} s is shorter than {o.min_shot} s')
        for a in s.get('actions', []):
            d = a.get('do')
            if d not in ACTIONS:
                errs.append(f'shot {sid}: unknown action {d!r}')
            tgt = a.get('target', a)
            if d in NEEDS_TARGET and not (TARGET_KEYS & set(tgt)):
                errs.append(f'shot {sid}: {d} has no target (role, label, placeholder, testId, text or selector)')
            if 'at' in a and not 0 <= a['at'] < length:
                errs.append(f'shot {sid}: {d} at {a["at"]} s is outside the shot (0..{length:.2f})')
            if d == 'type' and 'text' not in a:
                errs.append(f'shot {sid}: type has no "text"')
        cap = s.get('caption')
        for lang in langs or ([] if cap is None else ['-']):
            text = cap.get(lang) if isinstance(cap, dict) else cap
            if not text:
                errs.append(f'shot {sid}: no caption for {lang}'); continue
            if ' ' in text and length > 0:
                wpm = len(text.split()) / length * 60
                if wpm > o.max_wpm:
                    errs.append(f'shot {sid} [{lang}]: {wpm:.0f} words per minute (max {o.max_wpm:.0f})')
        t = end
    poster = cfg.get('poster')
    if poster is not None and not 0 <= poster < t:
        errs.append(f'poster at {poster} s is outside the video (0..{t:.2f})')
    print(f'total {t:.2f} s, {len(shots)} shots, languages: {",".join(langs) or "none"}')
    for e in errs:
        print('  ' + e)
    print('ok' if not errs else f'{len(errs)} problem(s)')
    return 1 if errs else 0


if __name__ == '__main__':
    sys.exit(main())
