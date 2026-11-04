#!/usr/bin/env python3
"""Join the voiced lines into one narration track, each line at its start time from timing.json.

  mix.py timing.json --audio DIR --out narration.wav [--music bed.wav --music-db -22] [--rate 48000]

Each line DIR/<line id>.wav is placed at its "start_s"; the track is exactly as long as the video
("duration_s"), so picture and sound stay in step. An optional music bed (only with a licence on record)
is lowered by --music-db and cut to the same length. Normalise the result afterwards with
loudness.py normalize. Python 3 standard library; needs ffmpeg. No network access.
"""
import argparse, json, os, subprocess, sys


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("timing"); ap.add_argument("--audio", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--music"); ap.add_argument("--music-db", type=float, default=-22.0)
    ap.add_argument("--rate", type=int, default=48000)
    a = ap.parse_args()
    t = json.load(open(a.timing, encoding="utf-8"))
    lines = [ln for sc in t["scenes"] for ln in sc["lines"]]
    if not lines:
        sys.exit("error: timing.json has no voiced lines")
    args, parts = ["ffmpeg", "-v", "error", "-y"], []
    for i, ln in enumerate(lines):
        f = os.path.join(a.audio, ln["file"])
        if not os.path.exists(f):
            sys.exit(f"error: missing {f}")
        args += ["-i", f]
        ms = int(round(ln["start_s"] * 1000))
        parts.append(f"[{i}:a]aresample={a.rate},aformat=channel_layouts=mono,adelay={ms}:all=1[l{i}]")
    n = len(lines)
    labels = "".join(f"[l{i}]" for i in range(n))
    if a.music:
        args += ["-i", a.music]
        parts.append(f"[{n}:a]aresample={a.rate},aformat=channel_layouts=mono,volume={a.music_db}dB[m]")
        labels += "[m]"; n += 1
    parts.append(f"{labels}amix=inputs={n}:normalize=0:duration=longest,apad,atrim=0:{t['duration_s']}[out]")
    args += ["-filter_complex", ";".join(parts), "-map", "[out]", "-ar", str(a.rate), "-ac", "1", a.out]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"error: ffmpeg failed: {r.stderr[-400:]}")
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.out],
                       capture_output=True, text=True).stdout.strip()
    print(f"{len(lines)} lines{' + music bed' if a.music else ''} -> {a.out}: {float(d):.3f} s (video {t['duration_s']} s)")


if __name__ == "__main__":
    main()
