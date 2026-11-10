"""
assemble.py — stitch the rendered scenes (in scenes.txt order) into one mp4 with a clean audio track.

    python3 assemble.py --quality high /path/to/outputs/my_explainer.mp4

Why not just concat the mp4s? Each scene's audio track ends when its last voice line ends, so naive
concatenation slowly drifts the narration out of sync. Instead this pads every scene's audio to the
exact length of its video, joins those, and muxes the result over the concatenated video (video is
stream-copied, so this takes well under a minute). Loudness is normalized to -16 LUFS.
"""
import argparse
import os
import subprocess
import tempfile

import numpy as np
import soundfile as sf

WORK = os.environ.get("EXPLAINER_WORK", "/tmp/explainer")
TTS = os.environ.get("EXPLAINER_TTS", "kokoro")
MEDIA = os.path.join(WORK, "media" if TTS == "kokoro" else f"media_{TTS}")
QDIR = {"low": "480p15", "mid": "720p30", "high": "1080p30"}
SR = 48000


def scene_list():
    out = []
    for raw in open("scenes.txt"):
        raw = raw.split("#")[0].strip()
        if raw:
            f, s = raw.split()
            out.append((f, s))
    return out


def vdur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                          "stream=duration", "-of", "csv=p=0", path]).decode())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--quality", choices=QDIR, default="high")
    a = ap.parse_args()
    tmp = tempfile.mkdtemp(prefix="assemble_")
    vids, chunks, total = [], [], 0.0
    for f, s in scene_list():
        mp4 = os.path.join(MEDIA, "videos", os.path.splitext(os.path.basename(f))[0], QDIR[a.quality], s + ".mp4")
        if not os.path.exists(mp4):
            raise SystemExit(f"missing render for {s}: {mp4}  (run render.py --quality {a.quality})")
        d = vdur(mp4)
        n = int(round(d * SR))
        wav = mp4[:-4] + ".wav"
        if os.path.exists(wav):
            w48 = os.path.join(tmp, s + ".wav")
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-ac", "1", "-ar", str(SR), w48], check=True)
            x, _ = sf.read(w48, dtype="float32")
        else:
            x = np.zeros(0, dtype=np.float32)  # silent scene
        x = x[:n] if len(x) >= n else np.concatenate([x, np.zeros(n - len(x), dtype=np.float32)])
        chunks.append(x)
        vids.append(mp4)
        total += d
        print(f"{s:>14}: {d:7.2f}s")
    audio = os.path.join(tmp, "full.wav")
    sf.write(audio, np.concatenate(chunks), SR)
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as fh:
        fh.writelines(f"file '{v}'\n" for v in vids)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", audio,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "-movflags", "+faststart", a.out],
                   check=True)
    v = vdur(a.out)
    adur = float(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
                                          "stream=duration", "-of", "csv=p=0", a.out]).decode())
    print(f"wrote {a.out}: video {v:.2f}s, audio {adur:.2f}s (expected {total:.2f}s), "
          f"{os.path.getsize(a.out) / 1e6:.1f} MB  ->  {'OK' if abs(v - adur) < 0.2 else 'CHECK SYNC'}")


if __name__ == "__main__":
    main()
