"""
explainer.py — helper library for narrated, 3Blue1Brown-style Manim explainer videos.

Copy this file into your project folder and start every scene file with:

    from explainer import *

Core idea: narration drives timing.

    class MyScene(VScene):
        def construct(self):
            self.header("Problem 1", "(a) rank")
            with self.vo("Here's our matrix. Part a asks for its rank."):
                self.play(Create(m))          # animations play *while* this line is spoken
            # the block waits until the audio clip has finished (+ a short gap)

Linear maps: linear_map(A, tracker) for the quick classic picture, or Warp for more control:

    w = Warp(A, origin=[-3, -2.6, 0], unit=0.6)      # place/scale the plane so targets fit
    self.add(w.ghost, w.grid)                         # add before header/cards so they draw on top
    ia = w.arrow((1, 0), GREEN)                       # rides along with the grid
    self.play(w.s.animate.set_value(1))               # identity -> A
    w.commit(B); self.play(w.s.animate.set_value(1))  # then apply B on top (composition B A)

Environment variables (all optional):
    EXPLAINER_WORK    scratch dir for media/, audio/, audio_el/    (default /tmp/explainer)
    EXPLAINER_TTS     kokoro | eleven | silent                     (default kokoro)
    EXPLAINER_VOICE   Kokoro voice id                              (default af_heart)
    EXPLAINER_SPEED   Kokoro speaking speed                        (default 1.0)
    KOKORO_DIR        folder with kokoro-q8.onnx + voices.npz      (default ~/.cache/explainer-tts)
"""
from contextlib import contextmanager
import hashlib
import os

import numpy as np
import soundfile as sf
from manim import *

WORK = os.environ.get("EXPLAINER_WORK", "/tmp/explainer")
AUDIO_DIR = os.path.join(WORK, "audio")
EL_DIR = os.path.join(WORK, "audio_el")
BACKEND = os.environ.get("EXPLAINER_TTS", "kokoro")
VOICE = os.environ.get("EXPLAINER_VOICE", "af_heart")
SPEED = float(os.environ.get("EXPLAINER_SPEED", "1.0"))
KOKORO_DIR = os.path.expanduser(os.environ.get("KOKORO_DIR", "~/.cache/explainer-tts"))
GAP = 0.35  # silence after each narration beat (seconds)
os.makedirs(AUDIO_DIR, exist_ok=True)

_kokoro = None


def kokoro():
    global _kokoro
    if _kokoro is None:
        from kokoro_onnx import Kokoro
        _kokoro = Kokoro(os.path.join(KOKORO_DIR, "kokoro-q8.onnx"), os.path.join(KOKORO_DIR, "voices.npz"))
    return _kokoro


def line_id(text):
    """Stable id for a narration line (used for ElevenLabs clip filenames)."""
    return hashlib.md5(text.encode()).hexdigest()[:16]


# Kokoro mispronounces some math words. These respellings change only the text sent to Kokoro;
# on-screen text and ElevenLabs input keep the normal spelling. Check any domain word with
#   python3 pronounce.py "Hessian" "Lagrangian"
# and add (regex, replacement) pairs here (or RESPELL.append(...) at the top of a scene file).
RESPELL = [
    (r"\b([Ee])igen", lambda m: m.group(1) + "yegun"),     # eigen- said "EYE-jen" otherwise
    (r"\bA\b", "Eigh"),                                   # capital A = algorithm/letter/event; Kokoro says "uh" otherwise
    (r"\bBlum\b", "Bloom"),
    (r"\bVigenere\b", "Veezhenair"),
    (r"\b[Nn]um[Pp]y\b", "num pie"),
    (r"\bi\.i\.d\.", "I I D"),
]


def spoken(text):
    import re
    for pat, rep in RESPELL:
        text = re.sub(pat, rep, text)
    return text


def tts(text):
    """Return (wav_path, duration_seconds) for a narration line. Cached, so re-renders are free."""
    if BACKEND == "eleven":
        path = os.path.join(EL_DIR, line_id(text) + ".wav")
        if not os.path.exists(path):
            raise FileNotFoundError(f"missing ElevenLabs clip {line_id(text)} for: {text[:70]!r}")
        return path, sf.info(path).duration
    if BACKEND == "silent":  # placeholder timing (~15 chars/s) when no TTS is available
        path = os.path.join(AUDIO_DIR, "silent_" + line_id(text) + ".wav")
        if not os.path.exists(path):
            sf.write(path, np.zeros(int(24000 * max(1.0, len(text) / 15))), 24000)
        return path, sf.info(path).duration
    say = spoken(text)
    h = hashlib.md5(f"{VOICE}|{SPEED}|{say}".encode()).hexdigest()[:14]
    path = os.path.join(AUDIO_DIR, f"{h}.wav")
    if not os.path.exists(path):
        samples, sr = kokoro().create(say, voice=VOICE, speed=SPEED, lang="en-us")
        sf.write(path, samples, sr)
        with open(os.path.join(AUDIO_DIR, "index.tsv"), "a") as f:
            f.write(f"{h}\t{text}\n")
    return path, sf.info(path).duration


# ---------------- 3b1b-ish look ----------------
C1, C2, C3, C4, C5 = BLUE_C, TEAL_C, YELLOW_C, GOLD_C, MAROON_B
PALETTE = [C1, C2, C3, C4, C5]          # cycle these for "object i" (columns, vectors, terms...)
HL = YELLOW                              # highlight / final answers
GOOD = GREEN_C
BAD = RED_C
config.background_color = "#0b0b0e"

TEX = TexTemplate()
TEX.add_to_preamble(r"\usepackage{amsmath,amssymb,bm}")


def T(*s, **kw):
    """Text typeset by LaTeX (Computer Modern, the classic 3b1b look). Use $...$ for inline math."""
    kw.setdefault("tex_template", TEX)
    return Tex(*s, **kw)


def M(*s, **kw):
    """Math. Pass several strings to get separately colorable/animatable parts: M("a", "=", "b")."""
    kw.setdefault("tex_template", TEX)
    return MathTex(*s, **kw)


def mat(rows, **kw):
    """Matrix with LaTeX entries. mat([[1, 0], [0, 1]]); entries may be strings like r"\\vdots"."""
    kw.setdefault("h_buff", 1.0)
    kw.setdefault("v_buff", 0.7)
    kw.setdefault("element_to_mobject", lambda s: M(str(s)))
    return Matrix(rows, **kw)


_MONO = [None]


def mono_font():
    """First installed monospace font: DejaVu Sans Mono (Linux), Menlo (macOS), then other fallbacks.
    Pango silently substitutes a proportional font (and prints a huge warning) if the name isn't installed."""
    if _MONO[0] is None:
        try:
            import manimpango
            have = set(manimpango.list_fonts())
        except Exception:
            have = set()
        _MONO[0] = next((f for f in ("DejaVu Sans Mono", "Menlo", "Monaco", "Consolas", "Courier New")
                         if f in have), "Monospace")
    return _MONO[0]


def code(s, fs=22, language="python"):
    """Syntax-highlighted code block. Scale with .scale_to_fit_width(...) if it is too wide."""
    return Code(code_string=s, language=language, formatter_style="monokai", add_line_numbers=False,
                background="rectangle",
                paragraph_config={"font": mono_font(), "font_size": fs},
                background_config={"fill_color": "#16161c", "fill_opacity": 1, "stroke_color": GREY_D,
                                   "stroke_width": 1.5, "corner_radius": 0.12, "buff": 0.25})


def fmt(x):
    """Number for LaTeX: 3.0 -> '3', -0.5 -> '-0.5'."""
    x = float(x)
    return str(int(round(x))) if abs(x - round(x)) < 1e-9 else f"{x:g}"


def bm(A):
    """numpy array (numbers or strings) -> LaTeX bmatrix string, e.g. M(r"X = " + bm(X))."""
    cell = lambda v: str(v) if isinstance(v, str) else fmt(v)
    return r"\begin{bmatrix}" + r"\\".join("&".join(cell(v) for v in row) for row in np.atleast_2d(A)) + r"\end{bmatrix}"


# ---- spoken numbers: build narration from computed values so audio can't disagree with the data ----
_ONES = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen "
         "sixteen seventeen eighteen nineteen").split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def words(n):
    """128 -> 'one hundred twenty eight'. Use .capitalize() at the start of a sentence."""
    n = int(n)
    if n < 0:
        return "minus " + words(-n)
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else " " + _ONES[n % 10])
    if n < 1000:
        return _ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + words(n % 100))
    return words(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + words(n % 1000))


def dec_words(x, digits=2):
    """0.944 -> 'zero point nine four'; -0.392 -> 'minus zero point three nine' (rounded to `digits`)."""
    s = f"{abs(x):.{digits}f}".rstrip("0").rstrip(".")
    whole, _, frac = s.partition(".")
    out = ("minus " if x < 0 and float(s) != 0 else "") + words(int(whole))
    return out + ((" point " + " ".join(_ONES[int(c)] for c in frac)) if frac else "")


def pct(k, n, digits=1):
    """On-screen percentage string. Use the SAME digits as pct_words, or screen and voice disagree."""
    return f"{100 * k / n:.{digits}f}"


def pct_words(k, n, digits=1):
    """6, 128 -> 'four point seven percent'."""
    return dec_words(100 * k / n, digits) + " percent"


def card(mob, buff=0.15, opacity=0.85):
    """Dark backing card for text placed over a busy background (grids, plots). Add it *before* the text:
    self.add(card(eq)); self.play(Write(eq)).  (Unlike add_background_rectangle it doesn't change
    eq's submobject indices.)"""
    return BackgroundRectangle(mob, color=config.background_color, fill_opacity=opacity, buff=buff)


def lerp_matrix(A, s):
    """(1 - s) I + s A, embedded in 3x3: the standard way to animate a linear map continuously."""
    A = np.array(A, dtype=float)
    M3 = np.identity(3)
    M3[:A.shape[0], :A.shape[1]] = (1 - s) * np.identity(A.shape[0]) + s * A
    return M3


def linear_map(A, s, vectors=(), x_range=(-8, 8), y_range=(-5, 5), ghost=True):
    """The classic 3b1b linear-transformation picture. `s` is a ValueTracker (0 = identity, 1 = A).
    vectors: [((x, y), color), ...] drawn as arrows that ride along with the grid.
    Returns VGroup(ghost_grid, moving_grid, *arrows). Animate with self.play(s.animate.set_value(1), run_time=3).
    Arrows are rebuilt every frame (ApplyMatrix on an Arrow would shear its tip)."""
    base = NumberPlane(x_range=[*x_range, 1], y_range=[*y_range, 1],
                       background_line_style={"stroke_color": BLUE_D, "stroke_width": 2, "stroke_opacity": 0.8},
                       faded_line_ratio=1)
    parts = []
    if ghost:
        parts.append(NumberPlane(x_range=[*x_range, 1], y_range=[*y_range, 1], axis_config={"stroke_opacity": 0.25},
                                 background_line_style={"stroke_color": GREY_D, "stroke_opacity": 0.35},
                                 faded_line_ratio=0))
    parts.append(always_redraw(lambda: base.copy().apply_matrix(lerp_matrix(A, s.get_value()))))
    for v, col in vectors:
        vv = np.array([*v, 0][:3], dtype=float)
        parts.append(always_redraw(lambda vv=vv, col=col: Arrow(
            ORIGIN, lerp_matrix(A, s.get_value()) @ vv, buff=0, color=col, stroke_width=6,
            max_tip_length_to_length_ratio=0.2)))
    return VGroup(*parts)


def arr(a, b, color=WHITE, sw=5, tip=0.22):
    """Arrow from a to b with consistent tip/stroke at any length; zero length doesn't crash."""
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    if np.linalg.norm(b - a) < 1e-3:
        b = a + 1e-3 * RIGHT
    return Arrow(a, b, buff=0, color=color, stroke_width=sw, tip_length=tip,
                 max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=40)


class Coords:
    """Math coordinates -> screen points for a plane with its origin at `origin` and `unit` screen units per 1."""

    def __init__(self, origin=ORIGIN, unit=1.0):
        self.o = np.array(origin, dtype=float)
        self.u = unit

    def __call__(self, x, y=None):
        if y is None:
            x, y = x
        return self.o + self.u * np.array([x, y, 0.0])


def grid_plane(origin=ORIGIN, unit=1.0, xr=(-7, 7), yr=(-4, 4), opacity=0.75, sw=1.5, ghost=False):
    """NumberPlane whose (0, 0) sits at `origin`, matching Coords(origin, unit). ghost=True: faint grey version."""
    line = ({"stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.45} if ghost else
            {"stroke_color": BLUE_D, "stroke_width": sw, "stroke_opacity": opacity})
    axis = ({"stroke_color": GREY_D, "stroke_width": 1.5, "stroke_opacity": 0.6} if ghost else
            {"stroke_color": GREY_B, "stroke_width": 2})
    p = NumberPlane(x_range=[xr[0], xr[1], 1], y_range=[yr[0], yr[1], 1],
                    x_length=unit * (xr[1] - xr[0]), y_length=unit * (yr[1] - yr[0]),
                    background_line_style=line, axis_config=axis, faded_line_ratio=0)
    p.shift(np.array(origin, dtype=float) - p.c2p(0, 0))
    return p


def rot(theta):
    return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])


def rot_path(theta):
    """Warp path that truly rotates (straight-line interpolation would shrink vectors mid-turn)."""
    return lambda s: rot(theta * s)


def between(A0, A1):
    """Warp path that morphs straight from matrix A0 to matrix A1 (e.g. an invertible map into a squish)."""
    A0, A1 = np.array(A0, dtype=float), np.array(A1, dtype=float)
    return lambda s: (1 - s) * A0 + s * A1


class Warp:
    """A linear map of the plane driven by the ValueTracker `w.s`.

    Current matrix = path(s) @ pre, where path(s) = (1 - s) I + s A, or fn(s) if given.
      w.grid / w.ghost   moving grid / faint static reference grid (add both, before text cards)
      w.p(v)             screen point of math vector v under the current map (use it in always_redraw)
      w.arrow(v, color)  arrow from the origin to w.p(v), rebuilt every frame
      w.dot(v, color)    dot riding at w.p(v)
      w.commit(B, fn=)   bake the current map into `pre`; the next animation applies B (or fn) on top
      w.reset(A, fn=)    back to identity-based path; call only when the grid currently shows `pre`
    `extent` = half-width of the moving grid in math units; raise it (~30) for maps that squash toward singular.
    """

    def __init__(self, A, origin=ORIGIN, unit=1.0, extent=14, ghost=True, opacity=0.8, fn=None):
        self.A = np.array(A, dtype=float)
        self.fn = fn
        self.pre = np.identity(2)
        self.s = ValueTracker(0)
        self.c = Coords(origin, unit)
        ext = (-extent, extent)
        self.base = grid_plane(origin, unit, ext, ext, opacity=opacity, sw=2)
        self.ghost = grid_plane(origin, unit, ext, ext, ghost=True) if ghost else VGroup()
        self.grid = always_redraw(lambda: self.base.copy().apply_matrix(self.M3(), about_point=self.c.o))

    def M(self):
        s = self.s.get_value()
        step = self.fn(s) if self.fn is not None else (1 - s) * np.identity(2) + s * self.A
        return step @ self.pre

    def M3(self):
        m = np.identity(3)
        m[:2, :2] = self.M()
        return m

    def p(self, v):
        return self.c(self.M() @ np.array(v, dtype=float))

    def arrow(self, v, color=WHITE, sw=6):
        return always_redraw(lambda: arr(self.c.o, self.p(v), color, sw=sw))

    def dot(self, v, color=WHITE, r=0.08):
        return always_redraw(lambda: Dot(self.p(v), radius=r, color=color))

    def commit(self, new_A=None, fn=None):
        self.pre = self.M()
        self.s.set_value(0)
        self.fn = fn
        if new_A is not None:
            self.A = np.array(new_A, dtype=float)

    def reset(self, A, fn=None):
        self.pre = np.identity(2)
        self.s.set_value(0)
        self.fn = fn
        self.A = np.array(A, dtype=float)


def follow(label, point_fn, offset=UR * 0.3):
    """Keep `label` beside a moving point: follow(label, lambda: w.p((1, 0)), DOWN * 0.35)."""
    label.add_updater(lambda m: m.move_to(point_fn() + offset))
    return label


def qframe(text, font_size=38, color=YELLOW):
    """Question frame: a question on a dark card. Show it, then self.wait(2.5) after the narration line."""
    q = T(text, font_size=font_size, color=color)
    return VGroup(card(q, buff=0.2), q)


class VoiceMixin:
    _header = None

    @contextmanager
    def vo(self, text, gap=GAP):
        """Speak `text`; animations inside the block play during the speech.
        Yields the clip duration so you can size run_times: `with self.vo(t) as d: ...`"""
        path, dur = tts(text)
        self.add_sound(path)
        t0 = self.renderer.time
        yield dur
        elapsed = self.renderer.time - t0
        if elapsed < dur + gap:
            self.wait(dur + gap - elapsed)

    def header(self, label, sub=None):
        """Small top-left section label, e.g. header("Problem 2", "(c) independence"). Animates changes."""
        new = VGroup(T(label, font_size=34, color=GREY_A))
        if sub:
            new.add(T(sub, font_size=28, color=GREY_B))
            new.arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        new.to_corner(UL, buff=0.4)
        line = Line(LEFT, RIGHT, stroke_width=1.5, color=GREY_D).set_width(new.width + 0.2)
        line.next_to(new, DOWN, buff=0.12, aligned_edge=LEFT)
        grp = VGroup(card(VGroup(new, line), buff=0.12), new, line).set_z_index(10)  # card keeps it legible over grids
        self._fix(grp)
        if self._header is None:
            self.play(FadeIn(grp, shift=0.2 * RIGHT), run_time=0.6)
        else:
            self.play(ReplacementTransform(self._header, grp), run_time=0.6)
        self._header = grp
        return grp

    def _fix(self, mob):
        if isinstance(self, ThreeDScene):
            self.add_fixed_in_frame_mobjects(mob)
            self.remove(mob)

    def clear_all(self, keep_header=True, run_time=0.6):
        """Fade out everything (optionally keeping the header)."""
        mobs = [m for m in self.mobjects if not (keep_header and m is self._header)]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)


class VScene(VoiceMixin, Scene):
    """2-D narrated scene."""


_CAM = [None]


class BArrow(VGroup):
    """Fast 3-D arrow: a stroked line plus a flat tip that always faces the camera.
    Use instead of Arrow3D, which renders ~50x slower with the Cairo renderer."""

    def __init__(self, scene, start, end, color=WHITE, stroke_width=5, tip_len=0.26, tip_w=0.11, **kw):
        super().__init__(**kw)
        _CAM[0] = scene.camera
        self.s = np.array(start, dtype=float)
        self.e = np.array(end, dtype=float)
        self.alpha = 1.0
        self.tip_len, self.tip_w = tip_len, tip_w
        self.line = Line(self.s, self.e, color=color, stroke_width=stroke_width)
        self.tip = Polygon(self.e, self.e + RIGHT * 0.01, self.e + UP * 0.01, color=color,
                           fill_color=color, fill_opacity=1, stroke_width=0)
        self.add(self.line, self.tip)
        self.rebuild()
        self.add_updater(lambda m: m.rebuild())

    def rebuild(self):
        cam = _CAM[0]
        phi, theta = cam.get_phi(), cam.get_theta()
        view = np.array([np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi)])
        e = self.s + self.alpha * (self.e - self.s)
        v = e - self.s
        L = np.linalg.norm(v)
        if L < 1e-6:
            self.line.set_points_as_corners([self.s, self.s + 1e-4 * RIGHT])
            self.tip.set_points_as_corners([self.s, self.s, self.s, self.s])
            return self
        d = v / L
        tl = min(self.tip_len, 0.45 * L)
        perp = np.cross(d, view)
        if np.linalg.norm(perp) < 1e-6:
            perp = np.cross(d, OUT if abs(d[2]) < 0.9 else RIGHT)
        perp = perp / np.linalg.norm(perp)
        base = e - tl * d
        self.line.set_points_as_corners([self.s, base + 0.02 * d])
        self.tip.set_points_as_corners([e, base + self.tip_w * perp, base - self.tip_w * perp, e])
        return self

    def set_end(self, end):
        self.e = np.array(end, dtype=float)
        return self.rebuild()


def grow(arrow, **kw):
    """Animation that grows a BArrow from its start point: self.play(grow(a), run_time=1)."""
    def f(m, a):
        m.alpha = a
        m.rebuild()
    arrow.alpha = 0
    arrow.rebuild()
    return UpdateFromAlphaFunc(arrow, f, **kw)


class VThreeD(VoiceMixin, ThreeDScene):
    """3-D narrated scene. Put text/equations on screen with self.fixed(mob) so they don't rotate."""

    def arrow(self, start, end, color=WHITE, **kw):
        return BArrow(self, start, end, color=color, **kw)

    def fixed(self, *mobs):
        self.add_fixed_in_frame_mobjects(*mobs)
        for m in mobs:
            self.remove(m)
        return mobs
