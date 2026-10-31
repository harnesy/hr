#!/usr/bin/env python3
"""Measure and normalise loudness with ffmpeg, and print the numbers against a target.

  loudness.py measure FILE... [--target -16] [--tp -1]
  loudness.py normalize IN OUT [--target -16] [--tp -1] [--lra 11]

measure: integrated loudness (LUFS), true peak (dBTP), loudness range (LU), sample peak, clipped samples
and silences of 2 s or more, for each file. Verdict: integrated within 1 LU of the target and true peak
at or below the ceiling. Below 3 s of audio the integrated value is shaky: it is marked, and the joined
narration track is what counts.
normalize: two passes of ffmpeg's loudnorm (measure, then apply the measured values in linear mode),
keeping the input's sample rate; then measures the result.
Defaults: -16 LUFS and -1 dBTP for web (the hirer may choose; -23 LUFS for broadcast).
These are numbers only: a person still has to listen. Python 3 standard library; needs ffmpeg, ffprobe.
No network access.
"""
import argparse, json, re, subprocess, sys


def ffprobe(path, entry):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", entry, "-of", "csv=p=0", path], capture_output=True, text=True)
    return r.stdout.strip().split("\n")[0].split(",")[0]


def analyse(path, target, tp, lra):
    # astats and silencedetect first: they must see the input, not loudnorm's output
    f = (f"astats=metadata=0:measure_overall=Peak_level:measure_perchannel=none,silencedetect=noise=-50dB:d=2,"
         f"loudnorm=I={target}:TP={tp}:LRA={lra}:print_format=json")
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", f, "-f", "null", "-"], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"error: ffmpeg failed on {path}: {r.stderr[-300:]}")
    err = r.stderr
    j = json.loads(err[err.rindex("{"):err.rindex("}") + 1])
    peak = re.findall(r"Peak level dB:\s*(-?[\d.]+|-inf)", err)
    silences = re.findall(r"silence_duration:\s*([\d.]+)", err)
    clipped = clip_count(path)
    pk = peak[-1] if peak else "?"
    return j, (f"{float(pk):.1f}" if pk not in ("?", "-inf") else pk), silences, clipped


def clip_count(path):
    """Samples at or within 0.01 dB of full scale, counted on 16-bit signed PCM decoded by ffmpeg."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-"], capture_output=True)
    data = memoryview(r.stdout).cast("h") if len(r.stdout) % 2 == 0 else memoryview(r.stdout[:-1]).cast("h")
    return sum(1 for v in data if v >= 32766 or v <= -32767)


def report(path, target, tp, lra):
    j, peak, silences, clipped = analyse(path, target, tp, lra)
    dur = float(ffprobe(path, "format=duration") or 0)
    i, t = float(j["input_i"]), float(j["input_tp"])
    ok_i, ok_tp = abs(i - target) <= 1.0, t <= tp
    shaky = " (under 3 s: integrated value shaky)" if dur < 3 else ""
    print(f"{path}: {dur:.2f} s | integrated {i:.1f} LUFS (target {target}) {'ok' if ok_i else 'OFF'}{shaky} | "
          f"true peak {t:.1f} dBTP (ceiling {tp}) {'ok' if ok_tp else 'OVER'} | range {float(j['input_lra']):.1f} LU | "
          f"sample peak {peak} dB | clipped samples {clipped} | silences >=2 s: {len(silences)}")
    return j, ok_i and ok_tp and clipped == 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    for n in ("measure", "normalize"):
        p = sp.add_parser(n)
        p.add_argument("files", nargs="+")
        p.add_argument("--target", type=float, default=-16.0); p.add_argument("--tp", type=float, default=-1.0)
        p.add_argument("--lra", type=float, default=11.0)
    a = ap.parse_args()
    if a.cmd == "measure":
        bad = sum(not report(f, a.target, a.tp, a.lra)[1] for f in a.files)
        print("ok" if not bad else f"{bad} file(s) off target")
        sys.exit(1 if bad else 0)
    if len(a.files) != 2:
        sys.exit("error: normalize takes IN OUT")
    src, dst = a.files
    j, _ = report(src, a.target, a.tp, a.lra)
    rate = ffprobe(src, "stream=sample_rate") or "48000"
    f = (f"loudnorm=I={a.target}:TP={a.tp}:LRA={a.lra}:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
         f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", f, "-ar", rate, dst], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"error: ffmpeg failed: {r.stderr[-300:]}")
    print(f"normalised -> {dst} ({rate} Hz)")
    ok = report(dst, a.target, a.tp, a.lra)[1]
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
