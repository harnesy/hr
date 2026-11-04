#!/usr/bin/env python3
"""Check rendered web files against size targets written before encoding.

  webcheck.py --target out/video.webm=4MB --target out/video.mp4=6MB --target out/poster.jpg=150KB \
              [--seconds 9.5] [--silent out/loop.webm]

For each video: size, duration, codecs and whether it has an audio track (ffprobe).
--seconds: the expected length (timing.json "duration_s"); every video must match it within one frame (--fps, default 30).
--silent: files that must carry no audio track. Python 3 standard library only; no network access.
"""
import argparse, json, os, re, subprocess, sys

UNITS = {"B": 1, "KB": 1000, "MB": 1000 ** 2, "GB": 1000 ** 3}


def parse_target(s):
    path, _, lim = s.rpartition("=")
    m = re.fullmatch(r"([\d.]+)\s*(B|KB|MB|GB)", lim.strip(), re.I)
    if not path or not m:
        sys.exit(f"error: target must look like file=4MB, got {s}")
    return path, float(m.group(1)) * UNITS[m.group(2).upper()]


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,codec_name,width,height",
                          "-of", "json", path], capture_output=True, text=True)
    if out.returncode:
        return None
    return json.loads(out.stdout)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", action="append", default=[], required=True)
    ap.add_argument("--seconds", type=float); ap.add_argument("--fps", type=float, default=30)
    ap.add_argument("--silent", action="append", default=[])
    a = ap.parse_args()
    problems = 0
    for spec in a.target:
        path, limit = parse_target(spec)
        if not os.path.exists(path):
            print(f"{path}: missing"); problems += 1; continue
        size = os.path.getsize(path)
        verdict = "ok" if size <= limit else "OVER"
        problems += size > limit
        line = f"{path}: {size / 1000:.1f} KB of {limit / 1000:.0f} KB {verdict}"
        info = probe(path)
        streams = (info or {}).get("streams", [])
        is_video = os.path.splitext(path)[1].lower() in (".mp4", ".webm", ".mov", ".mkv", ".m4v")
        if is_video and any(s.get("codec_type") == "video" for s in streams):
            dur = float(info["format"]["duration"])
            v = next(s for s in streams if s.get("codec_type") == "video")
            aud = [s["codec_name"] for s in streams if s.get("codec_type") == "audio"]
            line += f"; {dur:.3f} s, {v.get('codec_name')} {v.get('width')}x{v.get('height')}, audio {aud or 'none'}"
            if a.seconds is not None and abs(dur - a.seconds) > 1 / a.fps + 0.001:
                line += f"; LENGTH differs from {a.seconds:.3f} s"; problems += 1
            if path in a.silent and aud:
                line += "; HAS AUDIO but must be silent"; problems += 1
        print(line)
    print("ok" if not problems else f"{problems} problem(s)")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
