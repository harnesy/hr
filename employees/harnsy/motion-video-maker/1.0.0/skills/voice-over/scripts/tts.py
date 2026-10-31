#!/usr/bin/env python3
"""Voice every line of a narration script into its own WAV file.

  tts.py script.json --out audio/ [--backend auto|elevenlabs|endpoint|kokoro] [--only LINE_ID]
                     [--env-file FILE] [--cloud-ok] [--dry-run]

Engines, tried in this order when --backend is auto (the first one fully configured is used):
  1. elevenlabs  ElevenLabs API with the hirer's key.
                 ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID, ELEVENLABS_MODEL_ID (all required);
                 ELEVENLABS_BASE_URL (default https://api.elevenlabs.io), ELEVENLABS_OUTPUT_FORMAT (default wav_24000).
  2. endpoint    The hirer's OpenAI-compatible speech server: POST {TTS_BASE_URL}/audio/speech.
                 TTS_BASE_URL (usually ends in /v1), TTS_MODEL, TTS_VOICE (required); TTS_API_KEY (optional).
  3. kokoro      Kokoro-82M on this machine's CPU, through the `kokoro` Python package the hirer installed.
                 KOKORO_VOICE (required); KOKORO_LANG (optional, defaults to the first letter of the voice id).
No engine, voice or model name is built into this script: every one comes from the hirer's settings.

Keys kept in harnsy (Settings > Keys): set ELEVENLABS_KEY_NAME or TTS_KEY_NAME to the key's name there and leave
ELEVENLABS_API_KEY / TTS_API_KEY unset. The request then goes through harnsy's key proxy on this machine (address from
HARNSY_AGENT_ADDR, seat token from HARNSY_PROXY_TOKEN, both set by harnsy for a seated agent) to the same path on the
real host (ELEVENLABS_BASE_URL or TTS_BASE_URL); harnsy adds the key, so the agent never sees it.

Settings come from the environment; --env-file reads KEY=VALUE lines from a file the hirer keeps outside the
project (values already in the environment win). Keys are never printed, logged or written to a file.

Network: the only request this script makes is the speech request to the engine the hirer configured
(ElevenLabs or TTS_BASE_URL). The kokoro engine itself may download its model weights on first use.
Text sent to ElevenLabs, or to a TTS_BASE_URL that is not on this machine or a private network, leaves
the hirer's network: the script refuses to send it without --cloud-ok, which the agent passes only
after the hirer said yes.

A failed request stops the run; it never switches engine in the middle of a script (one voice per video).
Python 3 standard library only, except the kokoro engine (needs `kokoro`, `numpy`) and ffmpeg for
converting a non-WAV reply.
"""
import argparse, ipaddress, json, os, shutil, socket, struct, subprocess, sys, tempfile, urllib.error, urllib.parse, urllib.request, wave

SECRET_VARS = ("ELEVENLABS_API_KEY", "TTS_API_KEY", "HARNSY_PROXY_TOKEN")
KEY_NAME = {"elevenlabs": "ELEVENLABS_KEY_NAME", "endpoint": "TTS_KEY_NAME"}


def redact(msg):
    for k in SECRET_VARS:
        v = os.environ.get(k)
        if v:
            msg = msg.replace(v, "<redacted>")
    return msg


def die(msg, code=2):
    print("error: " + redact(msg), file=sys.stderr)
    sys.exit(code)


def load_env_file(path):
    for raw in open(path, encoding="utf-8"):
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip().removeprefix("export ").strip(), v.strip().strip('"').strip("'")
        os.environ.setdefault(k, v)


def missing(names):
    if os.environ.get("ELEVENLABS_KEY_NAME"):
        names = [n for n in names if n != "ELEVENLABS_API_KEY"]
    return [n for n in names if not os.environ.get(n)]


def route(engine, url):
    """Return (url to call, auth headers): direct with the key from the environment, or through harnsy's key proxy."""
    key_name = os.environ.get(KEY_NAME[engine])
    if not key_name:
        keyed = engine == "elevenlabs" or bool(os.environ.get("TTS_API_KEY"))
        if keyed and urllib.parse.urlsplit(url).scheme != "https" and not is_local(url):
            die(f"refuses to send a key over http to a non-local host ({urllib.parse.urlsplit(url).netloc or url}): "
                "use the https address of the service, or a server on this machine or your network")
        if engine == "elevenlabs":
            return url, {"xi-api-key": os.environ["ELEVENLABS_API_KEY"]}
        return url, ({"Authorization": "Bearer " + os.environ["TTS_API_KEY"]} if os.environ.get("TTS_API_KEY") else {})
    if urllib.parse.urlsplit(url).scheme != "https" or is_local(url):
        die(f"{KEY_NAME[engine]} is set, but {urllib.parse.urlsplit(url).netloc or url} is not a public https host: harnsy's key "
            "proxy calls only public https hosts. For a speech server on this machine or your network, unset "
            f"{KEY_NAME[engine]} and put its key in {'ELEVENLABS_API_KEY' if engine == 'elevenlabs' else 'TTS_API_KEY'} (or none)")
    miss = missing(["HARNSY_AGENT_ADDR", "HARNSY_PROXY_TOKEN"])
    if miss:
        die(f"{KEY_NAME[engine]} is set, but {', '.join(miss)} is not: run inside a harnsy seat, or use a key in the environment")
    u = urllib.parse.urlsplit(url)
    proxied = urllib.parse.urlunsplit(("http", os.environ["HARNSY_AGENT_ADDR"],
                                       "/proxy/" + urllib.parse.quote(key_name, safe="") + u.path, u.query, ""))
    return proxied, {"X-Harnsy-Seat": os.environ["HARNSY_PROXY_TOKEN"], "X-Harnsy-Host": u.hostname or ""}


def is_local(url):
    host = urllib.parse.urlparse(url).hostname or ""
    if host in ("localhost",) or host.endswith(".local"):
        return True
    try:
        addrs = {ai[4][0] for ai in socket.getaddrinfo(host, None)}
    except OSError:
        return False
    return all(ipaddress.ip_address(a.split("%")[0]).is_private or ipaddress.ip_address(a.split("%")[0]).is_loopback for a in addrs)


def kokoro_available():
    try:
        import importlib.util
        return importlib.util.find_spec("kokoro") is not None
    except Exception:
        return False


REQ = {"elevenlabs": ["ELEVENLABS_API_KEY", "ELEVENLABS_VOICE_ID", "ELEVENLABS_MODEL_ID"],
       "endpoint": ["TTS_BASE_URL", "TTS_MODEL", "TTS_VOICE"],
       "kokoro": ["KOKORO_VOICE"]}


def choose(backend):
    order = ["elevenlabs", "endpoint", "kokoro"] if backend == "auto" else [backend]
    for name in order:
        miss = missing(REQ[name])
        if name == "kokoro" and not miss and not kokoro_available():
            miss = ["the kokoro Python package (pip install kokoro soundfile, in the hirer's environment)"]
        if not miss:
            return name
        why = f"{name}: not configured, missing {', '.join(miss)}"
        if backend != "auto":
            nxt = {"elevenlabs": "endpoint or kokoro", "endpoint": "kokoro", "kokoro": "none left"}[name]
            die(f"{why}. Ask the hirer for these settings, or fall back with --backend {nxt}" if nxt != "none left"
                else f"{why}. No engine is left: ask the hirer to configure one of elevenlabs, endpoint or kokoro.")
        print(f"skip {why}; trying the next engine")
    die("no engine is configured. Primary: ELEVENLABS_API_KEY + ELEVENLABS_VOICE_ID + ELEVENLABS_MODEL_ID. "
        "Alternative: TTS_BASE_URL + TTS_MODEL + TTS_VOICE. No-key fallback: KOKORO_VOICE with the kokoro package installed.")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # a keyed request never follows a redirect: the key would travel to another address


OPENER = urllib.request.build_opener(_NoRedirect)


def post(url, body, headers):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", **headers})
    try:
        with OPENER.open(req, timeout=120) as r:
            return r.read(), r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        detail = e.read()[:300].decode("utf-8", "replace")
        die(f"{urllib.parse.urlparse(url).netloc} answered HTTP {e.code}: {detail}", 4)
    except urllib.error.URLError as e:
        die(f"cannot reach {urllib.parse.urlparse(url).netloc}: {e.reason}", 4)


def to_wav(data, ctype, dest, pcm_rate=None):
    if data[:4] == b"RIFF" and data[8:12] == b"WAVE":
        open(dest, "wb").write(data)
    elif pcm_rate:
        with wave.open(dest, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(pcm_rate); w.writeframes(data)
    elif data[:1] in (b"{", b"<"):
        die(f"the server replied with text, not audio ({ctype}): {data[:200].decode('utf-8', 'replace')}", 4)
    else:
        if not shutil.which("ffmpeg"):
            die(f"the reply is {ctype or 'not WAV'}; install ffmpeg to convert it, or ask the server for WAV", 4)
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(data)
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp.name, dest], capture_output=True, text=True)
        os.unlink(tmp.name)
        if r.returncode:
            die(f"ffmpeg could not convert the reply ({ctype}): {r.stderr[:200]}", 4)


def speak_elevenlabs(text, dest, dry):
    base = os.environ.get("ELEVENLABS_BASE_URL", "https://api.elevenlabs.io").rstrip("/")
    fmt = os.environ.get("ELEVENLABS_OUTPUT_FORMAT", "wav_24000")
    voice = urllib.parse.quote(os.environ["ELEVENLABS_VOICE_ID"], safe="")
    url = f"{base}/v1/text-to-speech/{voice}?output_format={urllib.parse.quote(fmt)}"
    body = {"text": text, "model_id": os.environ["ELEVENLABS_MODEL_ID"]}
    if dry:
        print(f"  would POST {url.split('?')[0]} (output_format={fmt}, model from ELEVENLABS_MODEL_ID, key {'added by harnsy key proxy' if os.environ.get('ELEVENLABS_KEY_NAME') else 'in xi-api-key header'})")
        return
    call, auth = route("elevenlabs", url)
    data, ctype = post(call, body, {**auth, "Accept": "audio/*"})
    rate = int(fmt.split("_")[1]) if fmt.startswith("pcm_") else None
    to_wav(data, ctype, dest, rate)


def speak_endpoint(text, dest, dry):
    url = os.environ["TTS_BASE_URL"].rstrip("/") + "/audio/speech"
    body = {"model": os.environ["TTS_MODEL"], "input": text, "voice": os.environ["TTS_VOICE"], "response_format": "wav"}
    proxied = bool(os.environ.get("TTS_KEY_NAME"))
    if dry:
        print(f"  would POST {url} (model from TTS_MODEL, voice from TTS_VOICE, response_format=wav, "
              f"key {'added by harnsy key proxy' if proxied else 'in Authorization header' if os.environ.get('TTS_API_KEY') else 'not set'})")
        return
    call, headers = route("endpoint", url)
    data, ctype = post(call, body, headers)
    to_wav(data, ctype, dest)


_PIPE = {}


def speak_kokoro(text, dest, dry):
    voice = os.environ["KOKORO_VOICE"]
    lang = os.environ.get("KOKORO_LANG") or voice[0]
    if dry:
        print(f"  would run Kokoro on CPU (voice from KOKORO_VOICE, language code {lang!r}); weights download on first use")
        return
    import numpy as np
    from kokoro import KPipeline
    if lang not in _PIPE:
        _PIPE[lang] = KPipeline(lang_code=lang, device="cpu")
    chunks = [np.asarray(audio, dtype=np.float32) for _, _, audio in _PIPE[lang](text, voice=voice) if audio is not None]
    if not chunks:
        die(f"Kokoro produced no audio for: {text[:60]}", 4)
    pcm = (np.clip(np.concatenate(chunks), -1, 1) * 32767).astype("<i2").tobytes()
    with wave.open(dest, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)


def wav_seconds(path):
    with wave.open(path) as w:
        return w.getnframes() / w.getframerate()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script"); ap.add_argument("--out", required=True)
    ap.add_argument("--backend", default="auto", choices=["auto", "elevenlabs", "endpoint", "kokoro"])
    ap.add_argument("--only"); ap.add_argument("--env-file"); ap.add_argument("--cloud-ok", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)
    if a.env_file:
        load_env_file(a.env_file)
    lines = [ln for sc in json.load(open(a.script, encoding="utf-8"))["scenes"] for ln in sc.get("lines", [])]
    if a.only:
        lines = [ln for ln in lines if ln["id"] == a.only] or die(f"no line with id {a.only}")
    name = choose(a.backend)
    where = {"elevenlabs": os.environ.get("ELEVENLABS_BASE_URL", "https://api.elevenlabs.io"),
             "endpoint": os.environ.get("TTS_BASE_URL", ""), "kokoro": "this machine (CPU)"}[name]
    remote = name == "elevenlabs" or (name == "endpoint" and not is_local(where))
    print(f"engine: {name}; audio made at: {urllib.parse.urlparse(where).netloc or where}; lines: {len(lines)}")
    if remote:
        print(f"note: the script text of {len(lines)} line(s) will be sent to {urllib.parse.urlparse(where).netloc}")
        if not a.cloud_ok and not a.dry_run:
            die("not sent: ask the hirer first (the script would go to this service), then rerun with --cloud-ok after a yes", 3)
    os.makedirs(a.out, exist_ok=True)
    speak = {"elevenlabs": speak_elevenlabs, "endpoint": speak_endpoint, "kokoro": speak_kokoro}[name]
    log = []
    for ln in lines:
        dest = os.path.join(a.out, ln["id"] + ".wav")
        speak(ln["text"], dest, a.dry_run)
        if a.dry_run:
            continue
        sec = wav_seconds(dest)
        wpm = len(ln["text"].split()) / max(sec, 0.01) * 60
        print(f"{ln['id']}: {sec:.2f} s, {wpm:.0f} words a minute -> {dest}")
        log.append({"id": ln["id"], "file": os.path.basename(dest), "seconds": round(sec, 3), "wpm": round(wpm)})
    if not a.dry_run:
        meta = {"engine": name, "host": urllib.parse.urlparse(where).netloc or where,
                "voice_setting": {"elevenlabs": "ELEVENLABS_VOICE_ID", "endpoint": "TTS_VOICE", "kokoro": "KOKORO_VOICE"}[name],
                "voice": os.environ.get({"elevenlabs": "ELEVENLABS_VOICE_ID", "endpoint": "TTS_VOICE", "kokoro": "KOKORO_VOICE"}[name]),
                "model": os.environ.get({"elevenlabs": "ELEVENLABS_MODEL_ID", "endpoint": "TTS_MODEL"}.get(name, "-")),
                "synthetic_voice": True, "lines": log}
        with open(os.path.join(a.out, "tts-log.json"), "w", encoding="utf-8") as fh:
            json.dump(meta, fh, indent=2); fh.write("\n")
        print(f"log -> {os.path.join(a.out, 'tts-log.json')} (no keys in it)")


if __name__ == "__main__":
    main()
