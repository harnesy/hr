#!/usr/bin/env python3
"""Timing and captions from measured narration.

  sync.py timing script.json --audio DIR [--fps 30] [--lead-in 0.3] [--gap 0.25] [--tail 0.6] --out timing.json
  sync.py vtt timing.json --out captions.vtt [--transcript transcript.txt] [--max-chars 42]
  sync.py lint captions.vtt [--video FILE] [--max-chars 42] [--max-wpm 180]

script.json: {"scenes": [{"id": "s1", "lines": [{"id": "s1-1", "text": "..."}]},
                         {"id": "end", "seconds": 2.0, "lines": []}]}
Each line's audio is DIR/<line id>.wav. Lengths come from ffprobe; nothing is typed by hand.
Python 3 standard library only; needs ffprobe on PATH. No network access.
"""
import argparse, json, math, os, re, subprocess, sys, textwrap


def probe_seconds(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True)
    if out.returncode != 0 or not out.stdout.strip():
        sys.exit(f"error: ffprobe could not read {path}: {out.stderr.strip()[:200]}")
    return float(out.stdout.strip())


def cmd_timing(a):
    script = json.load(open(a.script, encoding="utf-8"))
    fps = a.fps
    if fps <= 0 or fps != int(fps):
        sys.exit("error: --fps must be a whole number above 0")
    frame = 0
    scenes = []
    for sc in script["scenes"]:
        lines, t = [], a.lead_in
        start_s = frame / fps
        for i, ln in enumerate(sc.get("lines", [])):
            f = os.path.join(a.audio, ln["id"] + ".wav")
            if not os.path.exists(f):
                sys.exit(f"error: no audio for line {ln['id']} ({f}); voice it first")
            d = probe_seconds(f)
            if i:
                t += a.gap
            lines.append({"id": ln["id"], "text": ln["text"], "file": os.path.basename(f),
                          "start_s": round(start_s + t, 3), "duration_s": round(d, 3)})
            t += d
        if lines:
            seconds = t + a.tail
        else:
            seconds = float(sc.get("seconds", 0))
            if seconds <= 0:
                sys.exit(f"error: scene {sc['id']} has no lines and no \"seconds\"")
        seconds = max(seconds, float(sc.get("min_seconds", 0)))
        frames = math.ceil(round(seconds * fps, 6))
        scenes.append({"id": sc["id"], "start_frame": frame, "frames": frames, "seconds": round(frames / fps, 3), "lines": lines})
        frame += frames
    out = {"fps": int(fps), "total_frames": frame, "duration_s": round(frame / fps, 3),
           "lead_in_s": a.lead_in, "gap_s": a.gap, "tail_s": a.tail, "scenes": scenes}
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    for s in scenes:
        print(f"{s['id']}: frames {s['start_frame']}-{s['start_frame'] + s['frames'] - 1} ({s['frames']} = {s['seconds']} s), lines {len(s['lines'])}")
    print(f"total {frame} frames at {int(fps)} fps = {out['duration_s']} s -> {a.out}")


def ts(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def cues_for(line, max_chars):
    """Split one spoken line into cues of at most two rows; time shared by character count."""
    rows = textwrap.wrap(line["text"], max_chars)
    chunks = [rows[i:i + 2] for i in range(0, len(rows), 2)]
    total = sum(len(" ".join(c)) for c in chunks) or 1
    t = line["start_s"]
    out = []
    for c in chunks:
        d = line["duration_s"] * len(" ".join(c)) / total
        out.append((t, t + d, "\n".join(c)))
        t += d
    return out


def cmd_vtt(a):
    tm = json.load(open(a.timing, encoding="utf-8"))
    parts, n, words = ["WEBVTT", ""], 0, []
    for sc in tm["scenes"]:
        for ln in sc["lines"]:
            words.append(ln["text"])
            for s, e, txt in cues_for(ln, a.max_chars):
                n += 1
                parts += [f"{ln['id']}-{n}", f"{ts(s)} --> {ts(e)}", txt, ""]
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(parts))
    print(f"{n} cues -> {a.out}")
    if a.transcript:
        with open(a.transcript, "w", encoding="utf-8") as fh:
            fh.write("\n\n".join(words) + "\n")
        print(f"transcript -> {a.transcript}")


TIME = re.compile(r"^(\d{2}):(\d{2}):(\d{2})\.(\d{3}) --> (\d{2}):(\d{2}):(\d{2})\.(\d{3})(\s.*)?$")


def secs(g):
    return int(g[0]) * 3600 + int(g[1]) * 60 + int(g[2]) + int(g[3]) / 1000


def cmd_lint(a):
    text = open(a.vtt, encoding="utf-8").read()
    problems = []
    if not text.startswith("WEBVTT"):
        problems.append("file does not start with WEBVTT")
    blocks = [b for b in re.split(r"\n\s*\n", text.strip()) if b.strip()][1:]
    last_end, last_cue = 0.0, 0.0
    for b in blocks:
        rows = b.splitlines()
        k = next((i for i, r in enumerate(rows) if "-->" in r), None)
        if k is None:
            continue
        m = TIME.match(rows[k].strip())
        if not m:
            problems.append(f"bad timing line: {rows[k]}")
            continue
        s, e = secs(m.groups()[:4]), secs(m.groups()[4:8])
        body = rows[k + 1:]
        tag = rows[0] if k else rows[k]
        if e <= s:
            problems.append(f"{tag}: ends before it starts")
        if s < last_end - 0.0005:
            problems.append(f"{tag}: overlaps the cue before")
        if len(body) > 2:
            problems.append(f"{tag}: {len(body)} rows (2 at most)")
        for r in body:
            if len(r) > a.max_chars:
                problems.append(f"{tag}: row of {len(r)} characters ({a.max_chars} at most)")
        wpm = len(" ".join(body).split()) / max(e - s, 0.001) * 60
        if wpm > a.max_wpm:
            problems.append(f"{tag}: {wpm:.0f} words a minute ({a.max_wpm} at most)")
        last_end, last_cue = e, max(last_cue, e)
    if a.video:
        d = probe_seconds(a.video)
        if last_cue > d + 0.001:
            problems.append(f"last cue ends at {last_cue:.3f} s, after the video ({d:.3f} s)")
        print(f"video {d:.3f} s, last cue ends {last_cue:.3f} s")
    print(f"{len(blocks)} cues checked")
    for p in problems:
        print("problem:", p)
    print("ok" if not problems else f"{len(problems)} problem(s)")
    sys.exit(1 if problems else 0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    t = sp.add_parser("timing")
    t.add_argument("script"); t.add_argument("--audio", required=True); t.add_argument("--out", required=True)
    t.add_argument("--fps", type=float, default=30); t.add_argument("--lead-in", type=float, default=0.3)
    t.add_argument("--gap", type=float, default=0.25); t.add_argument("--tail", type=float, default=0.6)
    v = sp.add_parser("vtt")
    v.add_argument("timing"); v.add_argument("--out", required=True); v.add_argument("--transcript")
    v.add_argument("--max-chars", type=int, default=42)
    li = sp.add_parser("lint")
    li.add_argument("vtt"); li.add_argument("--video"); li.add_argument("--max-chars", type=int, default=42)
    li.add_argument("--max-wpm", type=int, default=180)
    a = ap.parse_args()
    {"timing": cmd_timing, "vtt": cmd_vtt, "lint": cmd_lint}[a.cmd](a)


if __name__ == "__main__":
    main()
