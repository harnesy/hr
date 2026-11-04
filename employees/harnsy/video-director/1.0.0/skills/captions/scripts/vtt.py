#!/usr/bin/env python3
# Copyright (c) 2026 Pavel Buchnev (harnsy)
# SPDX-License-Identifier: MIT
"""Caption files (WebVTT) for a recorded video: write them from the shot file, then lint them.
Text comes from the shot file as written; this tool only breaks it into lines, it never rewords it.

usage:
  vtt.py write <marks> --shots shots.json --out DIR [--name video] [--lang en,es] [--line 32]
      Write <DIR>/<name>.<lang>.vtt: one cue per shot, timed on the take's marks, text from each
      shot's "caption" (a string, or {"en": "...", "es": "..."}). Cue ids are the shot ids.
      Text is broken into balanced lines of at most --line characters, at word boundaries.
      A shot without a caption gets no cue. Default languages: all found in the shot file.
      <marks> is a take dir with marks.txt (from assemble.py) or "b0,b1,...,bN" in seconds.

  vtt.py lint FILE.vtt... [--max-lines 2] [--line 32] [--max-wpm 180] [--min-dur 1.0]
      Readability: lines per cue, characters per line, reading speed in words per minute,
      shortest time on screen, overlapping cues. Prints every problem; exit 1 if any.
      Text without spaces (Chinese, Japanese, Korean) is not wrapped or checked by words.

Defaults follow common subtitle practice: 2 lines, about 32 characters per line,
160-180 words per minute at most. Change them if the page's style guide says otherwise.
"""
import json
import os
import re
import sys

TIME = r'(?:(\d+):)?(\d{2}):(\d{2})[.,](\d{3})'
ARROW = re.compile(TIME + r'\s+-->\s+' + TIME + r'(.*)')
CJK = re.compile(r'[぀-ヿ㐀-鿿가-힯]')


def secs(h, m, s, ms):
    return int(h or 0) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def ts(t):
    h, r = divmod(round(max(0.0, t) * 1000), 3600_000)
    m, r = divmod(r, 60_000)
    s, ms = divmod(r, 1000)
    return f'{h:02d}:{m:02d}:{s:02d}.{ms:03d}'


def parse(text):
    cues = []
    for b in re.split(r'\n\s*\n', text.replace('\r\n', '\n').replace('\r', '\n').strip()):
        lines = b.split('\n')
        i = next((j for j, ln in enumerate(lines) if '-->' in ln), None)
        m = ARROW.search(lines[i]) if i is not None else None
        if not m:
            continue  # header, NOTE, STYLE, REGION
        g = m.groups()
        cues.append({'id': '\n'.join(lines[:i]).strip(), 'start': secs(*g[0:4]), 'end': secs(*g[4:8]),
                     'text': '\n'.join(lines[i + 1:]).strip()})
    return cues


def wrap(text, width):
    """Fewest lines of <= width characters, balanced so the lines are about equal."""
    if '\n' in text or len(text) <= width or CJK.search(text):
        return text
    words = text.split()
    for n in range(2, len(words) + 1):
        target = len(text) / n
        lines, cur = [], ''
        for w in words:
            cand = f'{cur} {w}'.strip()
            if cur and (len(cand) > width or (len(cur) >= target and len(lines) < n - 1)):
                lines.append(cur)
                cur = w
            else:
                cur = cand
        lines.append(cur)
        if all(len(x) <= width for x in lines):
            return '\n'.join(lines)
    return '\n'.join(words)


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


def cmd_write(args):
    shots_path, out, name = opt(args, '--shots'), opt(args, '--out'), opt(args, '--name', 'video')
    langs, width = opt(args, '--lang'), int(opt(args, '--line', '32'))
    if len(args) != 1 or not shots_path or not out:
        usage()
    marks = marks_of(args[0])
    shots = json.load(open(shots_path, encoding='utf-8'))['shots'][:len(marks) - 1]
    found = set()
    for s in shots:
        if isinstance(s.get('caption'), dict):
            found |= set(s['caption'])
    langs = langs.split(',') if langs else sorted(found) or ['en']
    os.makedirs(out, exist_ok=True)
    for lang in langs:
        body, n = ['WEBVTT', ''], 0
        for i, s in enumerate(shots):
            c = s.get('caption')
            text = c.get(lang) if isinstance(c, dict) else c
            if not text:
                continue
            body += [str(s['id']), f'{ts(marks[i])} --> {ts(marks[i + 1])}', wrap(text.strip(), width), '']
            n += 1
        p = os.path.join(out, f'{name}.{lang}.vtt')
        with open(p, 'w', encoding='utf-8') as f:
            f.write('\n'.join(body))
        print(f'{lang}: {n} cues -> {p}')


def cmd_lint(args):
    mlines = int(opt(args, '--max-lines', '2'))
    width = int(opt(args, '--line', '32'))
    wpm = float(opt(args, '--max-wpm', '180'))
    mind = float(opt(args, '--min-dur', '1.0'))
    if not args:
        usage()
    bad = 0
    for fp in args:
        cs = parse(open(fp, encoding='utf-8').read())
        errs = []
        for i, c in enumerate(cs):
            name = c['id'] or str(i + 1)
            plain = re.sub(r'<[^>]+>', '', c['text'])
            dur = c['end'] - c['start']
            lines = plain.split('\n')
            if dur < mind:
                errs.append(f'  cue {name}: {dur:.2f} s on screen, under {mind} s')
            if len(lines) > mlines:
                errs.append(f'  cue {name}: {len(lines)} lines (max {mlines}); split the shot or shorten the text')
            for ln in lines:
                if len(ln) > width:
                    errs.append(f'  cue {name}: a line of {len(ln)} characters (max {width})')
            if not CJK.search(plain) and dur > 0:
                rate = len(plain.split()) / dur * 60
                if rate > wpm:
                    errs.append(f'  cue {name}: {rate:.0f} words per minute (max {wpm:.0f}); more time or fewer words')
            if i and c['start'] < cs[i - 1]['end'] - 0.001:
                errs.append(f'  cue {name}: starts before the previous cue ends')
        print(f'{fp}: ' + ('ok' if not errs else f'{len(errs)} problem(s)'))
        for e in errs:
            print(e)
        bad += bool(errs)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or '-h' in a or '--help' in a:
        usage(0 if a else 1)
    {'write': cmd_write, 'lint': cmd_lint}.get(a[0], lambda _: usage())(a[1:])
