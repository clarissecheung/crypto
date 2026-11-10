#!/usr/bin/env python3
"""
Generate ElevenLabs narration for an explainer video via OpenRouter (__TITLE__).

Run on your Mac (no installs needed; uses the built-in curl):

    export OPENROUTER_API_KEY=sk-or-...      # or just run it and paste the key when asked
    python3 make_elevenlabs_audio.py         # optional: --voice george --model elevenlabs/eleven-v4-turbo
    python3 make_elevenlabs_audio.py --env-file ../.env   # or read OPENROUTER_API_KEY / OPENROUTER_KEY from a .env

It writes one mp3 per narration line into ./__OUTNAME__/ and then zips
them into __OUTNAME__.zip. Upload that zip back to Claude.
Re-running resumes: lines that already have an mp3 are skipped.
"""
import argparse, concurrent.futures as cf, getpass, json, os, shutil, subprocess, sys, tempfile, time, urllib.request, zipfile

URL = "https://openrouter.ai/api/v1/audio/speech"
LINES = json.loads(r"""__PAYLOAD__""")


def looks_like_mp3(b):
    return b[:3] == b"ID3" or (len(b) > 1 and b[0] == 0xFF and (b[1] & 0xE0) == 0xE0)


def request_curl(body, hdr_file):
    p = subprocess.run(["curl", "-sS", "-X", "POST", URL, "-H", "@" + hdr_file, "--data-binary", "@-",
                        "-w", "\n%{http_code}", "-o", "-"], input=body, capture_output=True, timeout=180)
    if p.returncode != 0:
        raise RuntimeError("curl failed: " + p.stderr.decode(errors="replace"))
    out = p.stdout
    i = out.rfind(b"\n")
    return int(out[i + 1:].decode().strip() or 0), out[:i]


def request_urllib(body, key):
    req = urllib.request.Request(URL, data=body, method="POST", headers={
        "Authorization": "Bearer " + key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default="george", help="OpenRouter ElevenLabs voice, e.g. george, adam, sarah, roger, will")
    ap.add_argument("--model", default="elevenlabs/eleven-v4-turbo")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", default="__OUTNAME__")
    ap.add_argument("--env-file", help=".env file containing OPENROUTER_API_KEY=... or OPENROUTER_KEY=...")
    a = ap.parse_args()

    key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENROUTER_KEY")
    if not key and a.env_file:
        for raw in open(os.path.expanduser(a.env_file)):
            name, _, val = raw.strip().partition("=")
            if name.strip().removeprefix("export ").strip() in ("OPENROUTER_API_KEY", "OPENROUTER_KEY") and val:
                key = val.strip().strip("'\"")
                break
        if not key:
            raise SystemExit("No OPENROUTER_API_KEY or OPENROUTER_KEY found in " + a.env_file)
    key = key or getpass.getpass("OpenRouter API key: ").strip()
    os.makedirs(a.out, exist_ok=True)
    use_curl = shutil.which("curl") is not None
    hdr = None
    if use_curl:
        fd, hdr = tempfile.mkstemp()
        os.write(fd, ("Authorization: Bearer %s\nContent-Type: application/json\n" % key).encode())
        os.close(fd)
        os.chmod(hdr, 0o600)

    def synth(line):
        path = os.path.join(a.out, line["id"] + ".mp3")
        if os.path.exists(path) and os.path.getsize(path) > 1000:
            return line["id"], "skip"
        body = json.dumps({"model": a.model, "input": line["text"], "voice": a.voice,
                           "response_format": "mp3"}).encode()
        delay = 2
        for attempt in range(6):
            try:
                code, data = request_curl(body, hdr) if use_curl else request_urllib(body, key)
            except Exception as e:
                code, data = -1, str(e).encode()
            if code == 200 and looks_like_mp3(data):
                with open(path, "wb") as f:
                    f.write(data)
                return line["id"], "ok"
            msg = data[:400].decode(errors="replace")
            if code in (400, 401, 402, 403, 404):
                raise SystemExit("\nOpenRouter error %s: %s" % (code, msg))
            time.sleep(delay)
            delay = min(delay * 2, 30)
        raise SystemExit("\nGave up on line %s after retries. Last response (%s): %s" % (line["id"], code, msg))

    total_chars = sum(len(l["text"]) for l in LINES)
    print("%d lines, %d characters -> %s (voice: %s)" % (len(LINES), total_chars, a.model, a.voice))
    try:
        synth(LINES[0])  # fail fast on a bad key / model / voice
        done = 1
        with cf.ThreadPoolExecutor(a.workers) as ex:
            for _id, status in ex.map(synth, LINES[1:]):
                done += 1
                print("\r  %d / %d" % (done, len(LINES)), end="", flush=True)
    finally:
        if hdr:
            os.remove(hdr)
    print()
    zpath = a.out + ".zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for l in LINES:
            z.write(os.path.join(a.out, l["id"] + ".mp3"), l["id"] + ".mp3")
        z.writestr("meta.json", json.dumps({"model": a.model, "voice": a.voice}))
    print("Done! Upload %s back to Claude." % os.path.abspath(zpath))


if __name__ == "__main__":
    main()
