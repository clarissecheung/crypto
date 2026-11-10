"""
elevenlabs.py — optional premium voice via ElevenLabs on OpenRouter, for when the sandbox itself
can't reach openrouter.ai. The user runs a generated script on their own machine; you ingest the zip.

Step 1 (you): write the user-runnable script from narration.json (made by tts_pass.py):
    python3 elevenlabs.py make "Linear algebra HW2" /path/to/outputs/make_elevenlabs_audio.py

Step 2 (user): `export OPENROUTER_API_KEY=...; python3 make_elevenlabs_audio.py [--voice george]`
    -> produces <name>_elevenlabs_audio.zip, which they upload back.

Step 3 (you): convert the clips and prepare a separate media folder:
    python3 elevenlabs.py ingest /path/to/uploaded.zip

Step 4 (you): EXPLAINER_TTS=eleven python3 render.py --quality high   (repeat until ALL DONE)
              EXPLAINER_TTS=eleven python3 assemble.py --quality high /path/to/outputs/video_elevenlabs.mp4
Every animation re-times itself to the new clip lengths, so sync stays exact.

If the machine CAN reach openrouter.ai (e.g. the user's own computer), run the generated script yourself
instead of step 2, from the project folder so clips persist there: --env-file reads the key from a .env.
Re-running skips clips that already exist, so after narration edits only changed lines are synthesized.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.environ.get("EXPLAINER_WORK", "/tmp/explainer")


def make(title, out_path, narration="narration.json"):
    lines = json.load(open(narration))
    payload = json.dumps([{"id": l["id"], "text": l["text"]} for l in lines], indent=0, ensure_ascii=False)
    assert '"""' not in payload
    slug = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")[:40] or "explainer"
    tpl = open(os.path.join(HERE, "elevenlabs_template.py")).read()
    src = tpl.replace("__PAYLOAD__", payload).replace("__TITLE__", title).replace("__OUTNAME__", slug + "_elevenlabs_audio")
    with open(out_path, "w") as f:
        f.write(src)
    print(f"wrote {out_path}: {len(lines)} lines, {sum(len(l['text']) for l in lines)} characters")


def ingest(zip_path, narration="narration.json"):
    raw = os.path.join(WORK, "el_raw")      # untrusted upload: unpack into its own folder
    out = os.path.join(WORK, "audio_el")
    shutil.rmtree(raw, ignore_errors=True)
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(raw)
    os.makedirs(out)
    with zipfile.ZipFile(zip_path) as z:
        for n in z.namelist():
            if re.fullmatch(r"[0-9a-f]{16}\.mp3|meta\.json", n):
                z.extract(n, raw)
    lines = json.load(open(narration))
    missing = []
    for l in lines:
        src = os.path.join(raw, l["id"] + ".mp3")
        if not os.path.exists(src):
            missing.append(l["id"])
            continue
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-ac", "1", "-ar", "44100",
                        os.path.join(out, l["id"] + ".wav")], check=True)
    # reuse the compiled LaTeX cache so the new render doesn't recompile everything
    tex_src, tex_dst = os.path.join(WORK, "media", "Tex"), os.path.join(WORK, "media_eleven", "Tex")
    if os.path.isdir(tex_src):
        shutil.copytree(tex_src, tex_dst, dirs_exist_ok=True)
    meta = os.path.join(raw, "meta.json")
    print(open(meta).read() if os.path.exists(meta) else "")
    print(f"{len(lines) - len(missing)}/{len(lines)} clips converted into {out}" +
          (f"; MISSING (narration changed since the script was made?): {missing}" if missing else ""))


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "make":
        make(sys.argv[2], sys.argv[3])
    elif len(sys.argv) >= 3 and sys.argv[1] == "ingest":
        ingest(sys.argv[2])
    else:
        print(__doc__)
