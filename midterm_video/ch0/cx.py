"""
cx.py - small visual vocabulary shared by every chapter of the crypto midterm review.

Color meanings (kept fixed across all videos):
    MSG  teal    plaintext messages m
    KEY  gold    secret keys k / secret factors p, q
    CT   purple  ciphertexts c
    ADV  red     the adversary (Eve, A)
    HON  blue    honest parties (Alice, Bob) and reductions (B)
"""
from explainer import *

MSG = TEAL_C
KEY = GOLD_C
CT = PURPLE_B
ADV = RED_C
HON = BLUE_C
DIM = GREY_C
PANEL = "#15151b"


def tx(s, fs=34, color=WHITE, **kw):
    """Tex line (text with $math$)."""
    return T(s, font_size=fs, color=color, **kw)


def rows(*items, fs=34, buff=0.28, aligned=LEFT):
    """Left-aligned stack of lines. Strings become Tex; mobjects are used as-is."""
    g = VGroup(*[tx(i, fs) if isinstance(i, str) else i for i in items])
    g.arrange(DOWN, buff=buff, aligned_edge=aligned)
    return g


def boxed(m, color=HL, buff=0.15):
    return SurroundingRectangle(m, color=color, buff=buff, corner_radius=0.06)


def panel(m, color=GREY_B, buff=0.25):
    """Dark rounded panel behind a group."""
    r = SurroundingRectangle(m, color=color, buff=buff, corner_radius=0.12, stroke_width=2)
    r.set_fill(PANEL, 1)
    return r


def algo(title, lines, fs=30, title_color=HL, frame_color=GREY_B, indent=0.5):
    """Pseudocode box. Lines are Tex strings; leading '>' characters indent a line one level each.
    Returns VGroup(frame, title, body) - body[i] is line i (handy for Indicate / highlighting)."""
    ttl = tx(title, fs + 2, title_color)
    parsed = []
    for ln in lines:
        lvl = len(ln) - len(ln.lstrip(">"))
        parsed.append((lvl, tx(ln.lstrip(">").strip() or r"\phantom{x}", fs)))
    body = VGroup(*[t for _, t in parsed]).arrange(DOWN, buff=0.17, aligned_edge=LEFT)
    for lvl, t in parsed:
        t.shift(RIGHT * indent * lvl)
    grp = VGroup(ttl, body).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
    frame = panel(grp, frame_color)
    return VGroup(frame, ttl, body)


def party(name, color, r=0.42, fs=28):
    """A labelled circle for Alice / Bob / Eve / an algorithm."""
    c = Circle(radius=r, color=color, fill_opacity=0.18, stroke_width=3)
    ini = tx(name[0], fs + 8, color).move_to(c)
    lab = tx(name, fs, color).next_to(c, DOWN, buff=0.12)
    return VGroup(c, ini, lab)


def bitrow(s, color=WHITE, size=0.46, fs=30, opacity=0.12):
    """Row of square cells holding the characters of s (bits or letters)."""
    cells = VGroup()
    for ch in s:
        sq = Square(size, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=opacity)
        sym = tx(r"\texttt{" + ch + "}" if ch != " " else r"\phantom{0}", fs, color).move_to(sq)
        cells.add(VGroup(sq, sym))
    cells.arrange(RIGHT, buff=0.05)
    return cells


def chip(text, color, fs=28):
    """Small rounded label (roadmap cards, tags)."""
    t = tx(text, fs, color)
    r = SurroundingRectangle(t, color=color, buff=0.18, corner_radius=0.12, stroke_width=2)
    r.set_fill(PANEL, 1)
    return VGroup(r, t)


def roadmap(items, cols=3, color_cycle=None, fs=26, w=4.0, h=1.0):
    """Grid of cards. items = list of (title, subtitle)."""
    color_cycle = color_cycle or PALETTE
    cards = VGroup()
    for i, (a, b) in enumerate(items):
        col = color_cycle[i % len(color_cycle)]
        r = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=col, stroke_width=2.5)
        r.set_fill(PANEL, 1)
        t1 = tx(a, fs + 2, col)
        t2 = tx(b, fs - 4, GREY_B)
        txt = VGroup(t1, t2).arrange(DOWN, buff=0.08)
        if txt.width > w - 0.3:
            txt.scale_to_fit_width(w - 0.3)
        txt.move_to(r)
        cards.add(VGroup(r, txt))
    cards.arrange_in_grid(cols=cols, buff=0.3)
    return cards


def recap_list(items, fs=32):
    """Numbered recap lines, left aligned."""
    g = VGroup()
    for i, s in enumerate(items, 1):
        num = tx(f"{i}.", fs, HL)
        line = tx(s, fs)
        g.add(VGroup(num, line).arrange(RIGHT, buff=0.2, aligned_edge=UP))
    g.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    return g


def fit(m, width=12.8, height=6.6):
    """Shrink m to fit inside the safe area if needed."""
    if m.width > width:
        m.scale_to_fit_width(width)
    if m.height > height:
        m.scale_to_fit_height(height)
    return m


def exam_tag():
    return chip(r"\textbf{exam-style}", HL, fs=24)
