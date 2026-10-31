#!/usr/bin/env python3
# Copyright (c) 2026 Pavel Buchnev (harnsy)
# SPDX-License-Identifier: MIT
"""Privacy check of a take before it leaves the recording machine.

usage: python3 check-frames.py <take-dir> [--every 1.0] [--deny names.txt] [--allow PATTERN]...

1. Text scan: reads <take-dir>/texts.json (the page's visible text and URL at each shot start and
   end, written by take.mjs) and flags what looks like a secret or personal data: e-mail addresses,
   key and token shapes (long hex or base64 strings, JWTs, common key prefixes, "Bearer ..."),
   phone numbers, card-like numbers, and every name from --deny (one per line, case-insensitive,
   e.g. real customer or staff names that must not appear).
   --allow REGEX skips a finding that matches (e.g. the stand's made-up domain). Repeatable.
2. Frames for review: copies one frame every --every seconds (and the first frame of each shot)
   into <take-dir>/review/ named by time, so a person or a vision model can look at every second.
   The text scan cannot see text inside images, canvas or video; the review frames are for that.

Exit 0 when the text scan finds nothing, 3 when it finds something. The frame review is still
required either way.
"""
import argparse
import bisect
import json
import os
import re
import shutil
import sys

PATTERNS = [
    ('e-mail', r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'),
    ('JWT', r'\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}'),
    ('key prefix', r'\b(?:sk|pk|rk)[-_](?:live|test|proj|ant)?[-_]?[A-Za-z0-9]{16,}|\bgh[pousr]_[A-Za-z0-9]{20,}|\bxox[abprs]-[A-Za-z0-9-]{10,}|\bAKIA[0-9A-Z]{16}\b|\bAIza[0-9A-Za-z_-]{30,}'),
    ('bearer', r'\bBearer\s+[A-Za-z0-9._~+/-]{12,}'),
    ('long hex', r'\b[0-9a-fA-F]{32,}\b'),
    ('long token', r'\b(?=[A-Za-z0-9_-]*\d)(?=[A-Za-z0-9_-]*[A-Z])(?=[A-Za-z0-9_-]*[a-z])[A-Za-z0-9_-]{32,}\b'),
    ('card-like number', r'\b(?:\d[ -]?){13,19}\b'),
    ('phone', r'(?<!\w)\+\d[\d ()-]{8,}\d'),
    ('private key', r'-----BEGIN [A-Z ]*PRIVATE KEY-----'),
]


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print(__doc__.strip()); return 0 if len(sys.argv) > 1 else 1
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument('take')
    ap.add_argument('--every', type=float, default=1.0)
    ap.add_argument('--deny')
    ap.add_argument('--allow', action='append', default=[])
    o = ap.parse_args()

    pats = [(n, re.compile(p)) for n, p in PATTERNS]
    if o.deny:
        for name in open(o.deny, encoding='utf-8').read().splitlines():
            if name.strip() and not name.startswith('#'):
                pats.append(('denied name', re.compile(re.escape(name.strip()), re.I)))
    allow = [re.compile(a) for a in o.allow]

    found = set()
    tpath = os.path.join(o.take, 'texts.json')
    if os.path.exists(tpath):
        for snap in json.load(open(tpath, encoding='utf-8')):
            hay = f"{snap.get('url', '')}\n{snap.get('text', '')}"
            for name, rx in pats:
                for m in rx.finditer(hay):
                    s = m.group(0)
                    if not any(a.search(s) for a in allow):
                        found.add((snap['shot'], snap['when'], name, s[:80]))
    else:
        print(f'no {tpath}: text scan skipped (frames only)')
    for shot, when, name, s in sorted(found):
        print(f'  FOUND shot {shot} ({when}): {name}: {s}')

    data = json.load(open(os.path.join(o.take, 'frames.json')))
    f, marks = data['frames'], data['marks']
    t0, t1 = marks[0][1], marks[-1][1]
    rev = os.path.join(o.take, 'review')
    shutil.rmtree(rev, ignore_errors=True)
    os.makedirs(rev)
    times = set()
    t = 0.0
    while t0 + t <= t1:
        times.add(round(t, 3)); t += o.every
    times |= {round(m[1] - t0 + 0.05, 3) for m in marks[:-1]}
    for t in sorted(times):
        i = max(0, bisect.bisect_right(f, t0 + t) - 1)
        shutil.copyfile(os.path.join(o.take, 'frames', f'{i:05d}.jpg'), os.path.join(rev, f't{t:08.3f}.jpg'))
    print(f'{len(times)} frames for review in {rev}: look at each for keys, tokens, personal data, real customer names')
    print('text scan: ' + ('nothing found' if not found else f'{len(found)} finding(s)'))
    return 3 if found else 0


if __name__ == '__main__':
    sys.exit(main())
