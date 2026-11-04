#!/usr/bin/env python3
"""Check a timing file before rendering, and print the still and render commands for it.

  plan.py timing.json --entry src/index.ts --comp Explainer [--size 1920x1080] [--out out] [--audio public/narration.wav]

Checks: whole-number fps, every scene a whole number of frames above 0, scenes back to back from frame 0,
the total equal to the sum, every voiced line inside its scene, an even frame size, and (with --audio)
that the narration is not longer than the video. Then prints one `npx remotion still` command per scene
(a frame in the middle of the scene) and the two `npx remotion render` commands (H.264 MP4, VP9 WebM).
It runs nothing itself. Python 3 standard library only; ffprobe only for --audio. No network access.
"""
import argparse, json, subprocess, sys


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("timing"); ap.add_argument("--entry", required=True); ap.add_argument("--comp", required=True)
    ap.add_argument("--size"); ap.add_argument("--out", default="out"); ap.add_argument("--audio")
    a = ap.parse_args()
    t = json.load(open(a.timing, encoding="utf-8"))
    fps, problems, expect = t.get("fps"), [], 0
    if not isinstance(fps, int) or not 1 <= fps <= 120:
        problems.append(f"fps {fps!r} is not a whole number from 1 to 120")
        fps = 30
    for s in t["scenes"]:
        if not isinstance(s["frames"], int) or s["frames"] <= 0:
            problems.append(f"scene {s['id']}: frames {s['frames']!r}")
        if s["start_frame"] != expect:
            problems.append(f"scene {s['id']}: starts at frame {s['start_frame']}, expected {expect}")
        end_s = (s["start_frame"] + s["frames"]) / fps
        for ln in s.get("lines", []):
            if ln["start_s"] + ln["duration_s"] > end_s + 1e-6:
                problems.append(f"line {ln['id']} ends at {ln['start_s'] + ln['duration_s']:.3f} s, after scene {s['id']} ({end_s:.3f} s)")
        expect = s["start_frame"] + s["frames"]
    if t["total_frames"] != expect:
        problems.append(f"total_frames {t['total_frames']} but scenes add up to {expect}")
    if a.size:
        w, _, h = a.size.partition("x")
        if not (w.isdigit() and h.isdigit()) or int(w) % 2 or int(h) % 2:
            problems.append(f"size {a.size}: width and height must be even numbers (H.264 and VP9 need it)")
    if a.audio:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.audio],
                             capture_output=True, text=True)
        d = float(out.stdout.strip() or 0)
        print(f"narration {d:.3f} s, video {t['total_frames'] / fps:.3f} s")
        if d > t["total_frames"] / fps + 1 / fps:
            problems.append("the narration is longer than the video")
    print(f"{len(t['scenes'])} scenes, {t['total_frames']} frames at {fps} fps = {t['total_frames'] / fps:.3f} s")
    for p in problems:
        print("problem:", p)
    if problems:
        sys.exit(1)
    print("\n# one still per scene: look at each image before the full render")
    for s in t["scenes"]:
        f = s["start_frame"] + s["frames"] // 2
        print(f"npx remotion still {a.entry} {a.comp} {a.out}/still-{s['id']}.png --frame={f}")
    print("\n# full render, after the stills are approved")
    print(f"npx remotion render {a.entry} {a.comp} {a.out}/{a.comp}.mp4 --codec=h264")
    print(f"npx remotion render {a.entry} {a.comp} {a.out}/{a.comp}.webm --codec=vp9")
    print("ok")


if __name__ == "__main__":
    main()
