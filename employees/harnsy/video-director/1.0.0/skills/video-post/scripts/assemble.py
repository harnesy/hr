#!/usr/bin/env python3
# Copyright (c) 2026 Pavel Buchnev (harnsy)
# SPDX-License-Identifier: MIT
"""Assemble a take (take.mjs output) into a constant-frame-rate, near-lossless master video,
plus a contact sheet to check every shot by eye, the shot marks and a chapters file.

usage: python3 assemble.py <take-dir> [options]

  reads  <take-dir>/frames/*.jpg and <take-dir>/frames.json
  writes <take-dir>/master.mp4    H.264, constant frame rate, near-lossless (the source for encode.sh)
         <take-dir>/contact.png   the middle frame of every shot, then the poster frame (last tile)
         <take-dir>/marks.txt     shot boundaries in seconds, comma-separated (for retime.py and captions)
         <take-dir>/chapters.json [{"id", "title", "start", "end"}] for the page's chapter list

The master starts on the first shot mark (0.0) and ends on the "stop" mark, so the marks are
the video's own times. A mark more than --tol seconds from the shot file prints OFF: retake.

options:
  --fps N         master frame rate (default 30)
  --crf N         master quality, lower = better (default 12)
  --poster-at S   time of the poster tile on the contact sheet (default: middle of the first shot)
  --tol S         allowed distance between a mark and its planned boundary (default 0.15)
  --cols N        contact sheet columns (default 3)
  --tile-width N  contact sheet tile width in px (default 480)
  -h, --help      this text

Exit code: 0 ok, 1 usage or tool error, 3 the take has OFF marks or warnings.
"""
import argparse
import bisect
import json
import os
import shutil
import subprocess
import sys


def ff(*a):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *a], check=True)


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument('take')
    ap.add_argument('--fps', type=float, default=30)
    ap.add_argument('--crf', type=int, default=12)
    ap.add_argument('--poster-at', type=float)
    ap.add_argument('--tol', type=float, default=0.15)
    ap.add_argument('--cols', type=int, default=3)
    ap.add_argument('--tile-width', type=int, default=480)
    ap.add_argument('-h', '--help', action='store_true')
    if any(x in ('-h', '--help') for x in sys.argv[1:]):
        print(__doc__.strip()); return 0
    if len(sys.argv) < 2:
        print(__doc__.strip()); return 1
    o = ap.parse_args()
    if not shutil.which('ffmpeg'):
        print('ffmpeg not found on PATH'); return 1

    out = o.take
    data = json.load(open(os.path.join(out, 'frames.json')))
    f, marks = data['frames'], data['marks']
    if len(marks) < 2 or not f:
        print('the take has no frames or no shots'); return 1
    t0, t1 = marks[0][1], marks[-1][1]

    # The screencast sends a frame only when the picture changes: the frame on screen at t0
    # is the last one sent before it. Each frame lasts until the next one (concat demuxer).
    k = max(0, bisect.bisect_right(f, t0) - 1)
    e = max(k, bisect.bisect_left(f, t1) - 1)
    lst = os.path.join(out, 'list.txt')
    with open(lst, 'w') as w:
        for i in range(k, e + 1):
            start = max(f[i], t0)
            end = f[i + 1] if i < e else t1
            w.write(f"file 'frames/{i:05d}.jpg'\nduration {max(end - start, 0.001):.4f}\n")
        w.write(f"file 'frames/{e:05d}.jpg'\n")
    master = os.path.join(out, 'master.mp4')
    # Even sizes for yuv420p; scale only if the viewport was odd.
    ff('-f', 'concat', '-safe', '0', '-i', lst,
       '-vf', f'fps={o.fps:g},scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p',
       '-c:v', 'libx264', '-crf', str(o.crf), '-preset', 'slow', '-t', f'{t1 - t0:.3f}', '-an', master)

    targets = data.get('targets') or []
    rel = [(n, t - t0) for n, t in marks]
    bad = 0
    print('shot marks (s):', ', '.join(f'{n} @{t:.2f}' for n, t in rel))
    for i, (n, t) in enumerate(rel):
        if i < len(targets) and abs(t - targets[i]) > o.tol:
            print(f'  OFF: {n} at {t:.2f} s, the shot file says {targets[i]:.2f} s'); bad += 1
    with open(os.path.join(out, 'marks.txt'), 'w') as w:
        w.write(','.join(f'{t:.3f}' for _, t in rel) + '\n')
    titles = {s['id']: s.get('title', '') for s in data.get('shots', [])}
    chapters = [{'id': n, 'title': titles.get(n, ''), 'start': round(a, 3), 'end': round(b, 3)}
                for (n, a), (_, b) in zip(rel, rel[1:])]
    with open(os.path.join(out, 'chapters.json'), 'w') as w:
        json.dump(chapters, w, ensure_ascii=False, indent=1)
    for msg in data.get('warnings', []):
        print('  take warning:', msg); bad += 1

    # Contact sheet with ffmpeg only: one tile per shot middle, plus the poster frame.
    poster = o.poster_at if o.poster_at is not None else chapters[0]['start'] + (chapters[0]['end'] - chapters[0]['start']) / 2
    ts = [(c['start'] + c['end']) / 2 for c in chapters] + [poster]
    tiles = os.path.join(out, 'contact')
    os.makedirs(tiles, exist_ok=True)
    for old in os.listdir(tiles):
        os.remove(os.path.join(tiles, old))
    for j, t in enumerate(ts):
        ff('-ss', f'{t:.3f}', '-i', master, '-frames:v', '1', '-vf', f'scale={o.tile_width}:-2',
           os.path.join(tiles, f'{j:03d}.png'))
    rows = (len(ts) + o.cols - 1) // o.cols
    ff('-framerate', '1', '-i', os.path.join(tiles, '%03d.png'),
       '-vf', f'tile={o.cols}x{rows}:padding=4:color=gray', '-frames:v', '1', os.path.join(out, 'contact.png'))
    print('master:', master, f'({rel[-1][1]:.2f} s)')
    print('contact sheet:', os.path.join(out, 'contact.png'), f'(shot middles; last tile = poster at {poster:.2f} s)')
    print('marks:', os.path.join(out, 'marks.txt'), '· chapters:', os.path.join(out, 'chapters.json'))
    return 3 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
