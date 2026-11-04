#!/usr/bin/env python3
# Copyright (c) 2026 Pavel Buchnev (harnsy)
# SPDX-License-Identifier: MIT
"""Fit existing caption files (WebVTT) to a new take. Cue text is never changed.

usage:
  retime.py check <marks> FILE.vtt... [--tol 0.15] [--copy-to DIR]
      Check that cue i runs from shot mark i to shot mark i+1 (one cue per shot, back to back).
      <marks> is a take dir with marks.txt (from assemble.py) or "b0,b1,...,bN" in seconds.
      --copy-to copies the files byte for byte, only if every file passes.
      Exit 1 on any mismatch: retake, or ask the caption owner for new times.

  retime.py retime <marks> FILE.vtt... --out DIR
      Keep each cue's id and text; give cue i the times mark i .. mark i+1.
      Use it only when the caption owner agrees that the shot order and count are unchanged;
      the cue count must equal the shot count.
"""
import os
import re
import shutil
import sys

TIME = r'(?:(\d+):)?(\d{2}):(\d{2})[.,](\d{3})'
ARROW = re.compile(TIME + r'\s+-->\s+' + TIME + r'(.*)')


def secs(h, m, s, ms):
    return int(h or 0) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def ts(t):
    h, r = divmod(round(max(0.0, t) * 1000), 3600_000)
    m, r = divmod(r, 60_000)
    s, ms = divmod(r, 1000)
    return f'{h:02d}:{m:02d}:{s:02d}.{ms:03d}'


def blocks(text):
    return re.split(r'\n\s*\n', text.replace('\r\n', '\n').replace('\r', '\n').strip())


def cues(text):
    out = []
    for b in blocks(text):
        m = ARROW.search(b)
        if m:
            g = m.groups()
            out.append((secs(*g[0:4]), secs(*g[4:8]), b))
    return out


def marks_of(arg):
    if os.path.isdir(arg):
        arg = open(os.path.join(arg, 'marks.txt')).read().strip()
    return [float(x) for x in arg.split(',')]


def opt(args, name, default=None):
    if name in args:
        i = args.index(name); v = args[i + 1]; del args[i:i + 2]; return v
    return default


def usage(code=1):
    print(__doc__.strip()); sys.exit(code)


def cmd_check(args):
    tol, copy_to = float(opt(args, '--tol', '0.15')), opt(args, '--copy-to')
    if len(args) < 2:
        usage()
    marks, files, bad = marks_of(args[0]), args[1:], 0
    for fp in files:
        cs = cues(open(fp, encoding='utf-8').read())
        errs = []
        if len(cs) != len(marks) - 1:
            errs.append(f'  {len(cs)} cues, the take has {len(marks) - 1} shots')
        for i, (a, b, _) in enumerate(cs[:len(marks) - 1]):
            for label, got, mk in (('start', a, marks[i]), ('end', b, marks[i + 1])):
                if abs(got - mk) > tol:
                    errs.append(f'  cue {i + 1} {label} {got:.3f} s, shot mark {mk:.3f} s')
        print(f'{fp}: ' + ('ok' if not errs else f'{len(errs)} mismatch(es)'))
        for e in errs:
            print(e)
        bad += bool(errs)
    if bad:
        print('MISMATCH: retake so the cuts land on the cue boundaries, or ask the caption owner for new times')
        sys.exit(1)
    if copy_to:
        os.makedirs(copy_to, exist_ok=True)
        for fp in files:
            shutil.copyfile(fp, os.path.join(copy_to, os.path.basename(fp)))
        print(f'copied {len(files)} file(s) unchanged to {copy_to}')


def cmd_retime(args):
    out = opt(args, '--out')
    if len(args) < 2 or not out:
        usage()
    marks = marks_of(args[0])
    os.makedirs(out, exist_ok=True)
    for fp in args[1:]:
        text = open(fp, encoding='utf-8').read()
        parts, k = [], 0
        for b in blocks(text):
            m = ARROW.search(b)
            if m and k < len(marks) - 1:
                b = b[:m.start()] + f'{ts(marks[k])} --> {ts(marks[k + 1])}{m.group(9)}' + b[m.end():]
            k += bool(m)
            parts.append(b)
        if k != len(marks) - 1:
            sys.exit(f'{fp}: {k} cues but {len(marks) - 1} shots; nothing written')
        p = os.path.join(out, os.path.basename(fp))
        with open(p, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(parts) + '\n')
        print(f'{fp}: re-timed -> {p}')


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or '-h' in a or '--help' in a:
        usage(0 if a else 1)
    {'check': cmd_check, 'retime': cmd_retime}.get(a[0], lambda _: usage())(a[1:])
