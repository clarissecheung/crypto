"""
tts_pass.py — synthesize every narration line WITHOUT rendering video, and write narration.json.

Run from the project folder (the one containing scenes.txt and explainer.py):

    timeout 170 python3 tts_pass.py            # all scenes in scenes.txt
    timeout 170 python3 tts_pass.py Q1 Q2      # only these scenes

Audio is cached by text, so if the call times out just run it again; it resumes where it stopped.
Prints "DONE" once every scene was processed, plus a per-line speaking-rate check: Kokoro normally
speaks 10-20 characters/second, so lines flagged outside 8-22 c/s are worth a look (truncated or
garbled audio, or a line full of single letters). Also compiles all LaTeX into the shared Tex
cache, which speeds up the renders and surfaces LaTeX errors early.
"""
import importlib
import json
import logging
import os
import sys
from contextlib import contextmanager

sys.path.insert(0, os.getcwd())
import explainer  # noqa: E402
from manim import Scene, ThreeDScene, config  # noqa: E402

config.media_dir = os.path.join(explainer.WORK, "media")
config.verbosity = "WARNING"
logging.getLogger("manim").setLevel(logging.WARNING)
lines, seen, total = [], set(), [0.0]


@contextmanager
def fake_vo(self, text, gap=explainer.GAP):
    _, d = explainer.tts(text)
    total[0] += d + gap
    i = explainer.line_id(text)
    if i not in seen:
        seen.add(i)
        cps = len(text) / max(d, 1e-6)
        lines.append({"id": i, "scene": type(self).__name__, "text": text, "seconds": round(d, 2),
                      "chars_per_sec": round(cps, 1)})
        if not 8 <= cps <= 22:
            print(f"  CHECK {cps:4.1f} c/s ({d:.1f}s): {text[:70]}", flush=True)
    yield d


def noop(self, *a, **k):
    return None


explainer.VoiceMixin.vo = fake_vo
explainer.VoiceMixin._fix = noop
explainer.VThreeD.fixed = lambda self, *m: m
for cls in (Scene, ThreeDScene):
    for name in ("play", "wait", "add_sound", "move_camera", "set_camera_orientation",
                 "begin_ambient_camera_rotation", "stop_ambient_camera_rotation"):
        setattr(cls, name, noop)


def scene_list():
    out = []
    for raw in open("scenes.txt"):
        raw = raw.split("#")[0].strip()
        if raw:
            f, s = raw.split()
            out.append((f, s))
    return out


only = set(sys.argv[1:])
for f, s in scene_list():
    if only and s not in only:
        continue
    total[0] = 0
    mod = importlib.import_module(os.path.splitext(f)[0])
    getattr(mod, s)().construct()
    print(f"{s}: narration ~{total[0]:.1f}s", flush=True)

if not only:
    json.dump(lines, open("narration.json", "w"), indent=1)
    secs = sum(l["seconds"] for l in lines)
    print(f"narration.json: {len(lines)} lines, {sum(len(l['text']) for l in lines)} characters, "
          f"{secs / 60:.1f} min of speech (video will run ~15% longer)")
print("DONE")
