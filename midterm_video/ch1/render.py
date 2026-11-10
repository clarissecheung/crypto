"""
render.py — render the scenes listed in scenes.txt, resumably, within a wall-clock budget.

Run from the project folder:

    python3 render.py --quality low            # quick 480p15 preview of everything
    python3 render.py --quality high           # final 1080p30
    python3 render.py --quality high Q2b Q5ef  # just these scenes
    python3 render.py --quality high --force Q3   # re-render even if up to date
    python3 render.py --quality high --budget 0   # no time limit (normal machines)

Designed for sandboxes where one shell call is capped at ~3 minutes and background processes die
when the call ends: it stops starting new work when the budget runs out, and Manim's per-animation
cache means a scene that was cut off resumes where it stopped. Run the same command again until
it prints ALL DONE.

Parallel safety: Manim writes a temporary "<hash>_.svg" next to every cached LaTeX svg each time
it loads one, so two processes sharing a Tex folder can delete each other's temp files. Each scene
therefore gets its own Tex folder (seeded from the shared cache, merged back afterwards), and
launches are staggered. A scene that still fails is retried once on its own.

A scene counts as up to date when its mp4 is newer than every .py file in the project folder.
Uses EXPLAINER_TTS / EXPLAINER_WORK like explainer.py; non-Kokoro voices render into their own
media folder (media_eleven, media_silent) so the Kokoro version is never overwritten.
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys
import time

WORK = os.environ.get("EXPLAINER_WORK", "/tmp/explainer")
TTS = os.environ.get("EXPLAINER_TTS", "kokoro")
MEDIA = os.path.join(WORK, "media" if TTS == "kokoro" else f"media_{TTS}")
QUAL = {"low": (["-ql"], "480p15"), "mid": (["-r", "1280,720", "--fps", "30"], "720p30"), "high": (["-r", "1920,1080", "--fps", "30"], "1080p30")}
SHARED_TEX = os.path.join(MEDIA, "Tex")


def scene_list():
    out = []
    for raw in open("scenes.txt"):
        raw = raw.split("#")[0].strip()
        if raw:
            f, s = raw.split()
            out.append((f, s))
    return out


def stem(f):
    return os.path.splitext(os.path.basename(f))[0]


def target(f, s, qdir):
    return os.path.join(MEDIA, "videos", stem(f), qdir, s + ".mp4")


def sync(src, dst):
    """Copy files present in src but missing in dst (hard links when possible)."""
    if not os.path.isdir(src):
        return
    os.makedirs(dst, exist_ok=True)
    have = set(os.listdir(dst))
    for n in os.listdir(src):
        if n in have or n.endswith("_.svg"):
            continue
        a, b = os.path.join(src, n), os.path.join(dst, n)
        try:
            os.link(a, b)
        except OSError:
            shutil.copy2(a, b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scenes", nargs="*")
    ap.add_argument("--quality", choices=QUAL, default="low")
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--budget", type=float, default=float(os.environ.get("RENDER_BUDGET", 160)),
                    help="seconds of wall clock to use (default 160 for 3-minute tool calls; 0 = unlimited)")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    flags, qdir = QUAL[a.quality]
    t_start = time.time()
    deadline = t_start + (a.budget if a.budget > 0 else 10 ** 9)
    logs = os.path.join(WORK, "logs")
    os.makedirs(logs, exist_ok=True)
    src_mtime = max(os.path.getmtime(p) for p in glob.glob("*.py"))

    todo = []
    for f, s in scene_list():
        if a.scenes and s not in a.scenes:
            continue
        out = target(f, s, qdir)
        if os.path.exists(out) and os.path.getmtime(out) > src_mtime and not a.force:
            print(f"{s}: up to date")
        else:
            todo.append((f, s))
            # pre-create folders Manim would otherwise race to mkdir
            for d in (os.path.join(MEDIA, "images", stem(f)),
                      os.path.join(MEDIA, "videos", stem(f), qdir, "partial_movie_files", s)):
                os.makedirs(d, exist_ok=True)

    # tts_pass.py compiles LaTeX into media/Tex; seed other voices' media folders from it
    sync(os.path.join(WORK, "media", "Tex"), SHARED_TEX)
    env = dict(os.environ, PATH=os.path.expanduser("~/.local/bin") + ":" + os.environ.get("PATH", ""))
    status = {}

    def launch(f, s):
        tex = os.path.join(MEDIA, "Tex_scenes", s)
        sync(SHARED_TEX, tex)
        os.makedirs(tex, exist_ok=True)       # SHARED_TEX may not exist yet (e.g. first silent/eleven render)
        cfg = os.path.join(MEDIA, "Tex_scenes", s + ".cfg")
        with open(cfg, "w") as fh:
            fh.write(f"[CLI]\ntex_dir = {tex}\n")
        log = open(os.path.join(logs, f"{s}.log"), "w")
        cmd = [sys.executable, "-m", "manim", *flags, "-v", "WARNING", "--media_dir", MEDIA,
               "--config_file", cfg, f, s]
        return subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, env=env), time.time()

    def run_batch(items, jobs):
        queue, running, failed, last_launch = list(items), {}, [], 0.0
        while queue or running:
            while (queue and len(running) < jobs and deadline - time.time() > 20
                   and time.time() - last_launch > 3):  # stagger starts
                f, s = queue.pop(0)
                running[s] = (f, *launch(f, s))
                last_launch = time.time()
            if not running:
                if queue and deadline - time.time() > 20:
                    time.sleep(0.5)
                    continue
                break
            time.sleep(0.5)
            for s, (f, p, t0) in list(running.items()):
                if p.poll() is None:
                    if time.time() > deadline:
                        p.terminate()
                        p.wait()
                        del running[s]
                        status[s] = "cut off by time budget (progress cached) - rerun to resume"
                    continue
                del running[s]
                sync(os.path.join(MEDIA, "Tex_scenes", s), SHARED_TEX)  # share newly compiled LaTeX
                if p.returncode == 0 and os.path.exists(target(f, s, qdir)):
                    status[s] = f"done ({time.time() - t0:.0f}s)"
                else:
                    failed.append((f, s))
                    status[s] = "FAILED"
        for f, s in queue:
            status[s] = "not started (budget) - rerun"
        return failed

    failed = run_batch(todo, a.jobs)
    if failed and deadline - time.time() > 30:
        print("retrying failures one at a time:", ", ".join(s for _, s in failed))
        failed = run_batch(failed, 1)
    for _, s in todo:
        print(f"{s}: {status.get(s, '?')}")
    for f, s in failed:
        log = os.path.join(logs, f"{s}.log")
        tail = [l.rstrip() for l in open(log, errors="replace") if "Error" in l or "error:" in l][-4:]
        print(f"--- {s} log ({log}):\n   " + "\n   ".join(tail))
    pending = [s for _, s in todo if not status.get(s, "").startswith("done")]
    print("ALL DONE" if not pending else f"PENDING: {' '.join(pending)}  (run the same command again)")
    print(f"videos in {os.path.join(MEDIA, 'videos')}/<file>/{qdir}/   ({time.time() - t_start:.0f}s)")


if __name__ == "__main__":
    main()
