from cx import *


class Intro0(VScene):
    def construct(self):
        title = tx(r"\textbf{Cryptography Midterm Review}", 54, HL)
        sub = tx(r"Part 0: the toolkit (weeks 1--5 rely on it)", 34, GREY_A)
        VGroup(title, sub).arrange(DOWN, buff=0.35).move_to(UP * 0.6)
        with self.vo("Welcome to the midterm review. Before we touch any cryptography, we need a small toolkit. "
                     "Every proof later in the course is built out of these pieces."):
            self.play(Write(title), run_time=1.5)
            self.play(FadeIn(sub, shift=0.2 * UP))
        self.play(FadeOut(title), FadeOut(sub))
        self.header("Part 0", "prerequisites")
        cards = roadmap([("Counting", "bit strings"), ("Probability", "uniform strings"),
                         ("Conditioning", "total prob., Bayes"), ("XOR", r"$\oplus$"),
                         ("Remainders", r"$[a \bmod m]$"), ("Logic and time", r"negation, loops")],
                        cols=3, w=3.9, h=1.25).move_to(DOWN * 0.2)
        with self.vo("Here is the plan. Six short topics, and each one matches an exercise from the "
                     "prerequisite notes. I'll solve every exercise step by step and assume nothing."):
            self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in cards], lag_ratio=0.15), run_time=2.5)
        with self.vo("Along the way I'll point out the exact mistakes that cost points on quiz one, "
                     "so they don't happen again on the midterm."):
            self.play(Indicate(cards[1], color=HL), Indicate(cards[5], color=HL), run_time=1.5)
        self.clear_all()

        n1 = rows(r"$x \xleftarrow{\$} S$ \quad : \quad pick $x$ uniformly at random from the set $S$",
                  r"$y \leftarrow A(x)$ \quad : \quad run the randomized algorithm $A$ on $x$",
                  r"$x := 5$ \quad : \quad ordinary assignment, no randomness", fs=34, buff=0.5)
        n1.move_to(UP * 0.3)
        with self.vo("Three pieces of notation first. An arrow with a dollar sign means pick uniformly at "
                     "random from a set. And a plain left arrow means run a randomized algorithm and store "
                     "its output. And colon equals is ordinary assignment.") as d:
            for line in n1:
                self.play(FadeIn(line, shift=0.2 * RIGHT))
                self.wait(d / 5)
        self.clear_all()


class Counting0(VScene):
    def construct(self):
        self.header("Counting", "Exercise 1")
        setdef = tx(r"$\{0,1\}^n$ = all bit strings of length exactly $n$", 38).to_edge(UP, buff=1.2)
        with self.vo("The set zero one to the n is every string of exactly n bits."):
            self.play(Write(setdef))
        strs = ["000", "001", "010", "011", "100", "101", "110", "111"]
        grid = VGroup(*[bitrow(s, MSG, size=0.42, fs=26) for s in strs]).arrange_in_grid(rows=2, buff=(0.5, 0.35))
        grid.move_to(UP * 0.2)
        with self.vo("For n equals three, here they all are. Count them: eight strings."):
            self.play(LaggedStart(*[FadeIn(g, shift=0.1 * DOWN) for g in grid], lag_ratio=0.12), run_time=2)
        why = M(r"2", r"\times", r"2", r"\times", r"2", r"=", r"8", font_size=48).next_to(grid, DOWN, buff=0.6)
        gen = M(r"|\{0,1\}^n| = 2^n", font_size=48, color=HL).next_to(why, DOWN, buff=0.35)
        with self.vo("Why eight? Each of the three positions has two choices, zero or one, and independent "
                     "choices multiply: two times two times two. The same argument with n positions gives "
                     "two to the n. That is part a.") as d:
            self.play(Write(why), run_time=1.5)
            self.wait(0.35 * d)
            self.play(Write(gen))
            self.play(Create(boxed(gen)))
        self.clear_all()

        qb = tx(r"(b) \ $|\{0,1\}^n \cup \{0,1\}^{10}|$ \quad for $n \ge 11$", 38).to_edge(UP, buff=1.2)
        A = Ellipse(width=4.2, height=2.6, color=C1, fill_opacity=0.15).move_to(LEFT * 2.6 + DOWN * 0.3)
        B = Ellipse(width=3.0, height=2.0, color=C2, fill_opacity=0.15).move_to(RIGHT * 2.6 + DOWN * 0.3)
        la = tx(r"$n$-bit strings\\$2^n$ of them", 30, C1).move_to(A)
        lb = tx(r"10-bit strings\\$2^{10}$ of them", 30, C2).move_to(B)
        with self.vo("Part b takes the union of two sets: all n bit strings, and all ten bit strings."):
            self.play(Write(qb))
            self.play(DrawBorderThenFill(A), DrawBorderThenFill(B), FadeIn(la), FadeIn(lb))
        ans = M(r"2^n + 2^{10}", font_size=48, color=HL).to_edge(DOWN, buff=0.7)
        with self.vo("Every string has one length. Since n is at least eleven, no string is in both sets, so they "
                     "don't overlap, and the sizes simply add: two to the n, plus two to the ten.") as d:
            self.wait(0.45 * d)
            self.play(Write(ans), Create(boxed(ans)))
        qc = tx(r"(c) \ $|\{0,1\}^n \cap \{0,1\}^{10}| = 0$", 38, HL).next_to(ans, UP, buff=0.35)
        with self.vo("And part c, the intersection, is the strings in both sets. There are none, so its size is zero. "
                     "Remember: sizes add in a union only when the sets don't overlap."):
            self.play(FadeIn(qc, shift=0.2 * UP))
        self.clear_all()


class Prob0a(VScene):
    def construct(self):
        self.header("Probability", "Exercise 2 (a)--(d)")
        rule = M(r"\Pr[E] = \frac{\#\text{ strings in } E}{\#\text{ all strings}} = \frac{|E|}{2^n}",
                 font_size=46).to_edge(UP, buff=1.2)
        note = tx(r"(only when $x$ is \emph{uniform}: every string equally likely)", 28, GREY_B).next_to(rule, DOWN)
        with self.vo("Exercise two samples x uniformly from all n bit strings. Uniform means every string is "
                     "equally likely, so a probability is just a count: how many strings are in the event, "
                     "divided by two to the n."):
            self.play(Write(rule), run_time=2)
            self.play(FadeIn(note))
        pa = M(r"\text{(a)}\ \Pr[x = 0^n] = \frac{1}{2^n}", font_size=42).next_to(note, DOWN, buff=0.6)
        with self.vo("Part a. The event x equals the all zero string contains exactly one string, so the "
                     "probability is one over two to the n."):
            self.play(Write(pa))
        self.clear_all()

        # palindromes
        s = "01100110"
        row = bitrow(s, MSG, size=0.6, fs=32).move_to(UP * 1.4)
        first = VGroup(*row[:4])
        second = VGroup(*row[4:])
        lab = tx(r"palindrome: reads the same backwards", 32).next_to(row, UP, buff=0.4)
        with self.vo("Event A says x is a palindrome: it reads the same forwards and backwards, like this "
                     "one with eight bits."):
            self.play(FadeIn(row), FadeIn(lab))
        arcs = VGroup(*[CurvedArrow(row[i].get_bottom() + DOWN * 0.05, row[7 - i].get_bottom() + DOWN * 0.05,
                                    angle=PI / 2.2, color=GREY_B, stroke_width=2, tip_length=0.15)
                        for i in range(4)])
        with self.vo("Here's the key observation. The last bit must copy the first, the second to last must "
                     "copy the second, and so on. Once you choose the first half, the second half is forced.") as d:
            self.play(first.animate.set_color(HL), run_time=0.8)
            self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.2), run_time=1.6)
            self.wait(0.2 * d)
            self.play(Indicate(second, color=GREY_B))
        cnt = M(r"\#\text{palindromes} = 2^{n/2}", r"\quad\Rightarrow\quad",
                r"\text{(b)}\ \Pr[A] = \frac{2^{n/2}}{2^n} = 2^{-n/2}", font_size=40).move_to(DOWN * 1.2)
        with self.vo("The first half has n over two free bits, so there are two to the n over two palindromes. "
                     "Divide by two to the n, and the probability is two to the minus n over two."):
            self.play(Write(cnt[0]))
            self.play(Write(cnt[1:]))
            self.play(Create(boxed(cnt[2])))
        chk = tx(r"check $n=4$: \ \texttt{0000, 0110, 1001, 1111} \ $= 4 = 2^{2}$ of 16", 30, GREY_A).to_edge(DOWN, buff=0.5)
        with self.vo("Always sanity check with a tiny case. For n equals four, the palindromes are zero zero "
                     "zero zero, zero one one zero, one zero zero one, and one one one one. Four of sixteen, "
                     "exactly two to the two."):
            self.play(FadeIn(chk, shift=0.2 * UP))
        self.clear_all()

        rowb = bitrow("00" + "?" * 6, MSG, size=0.6, fs=32).move_to(UP * 1.6)
        VGroup(*rowb[:2]).set_color(HL)
        with self.vo("Event B says x starts with zero zero. The first two bits are forced, and the remaining "
                     "n minus two are free."):
            self.play(FadeIn(rowb))
        pc = M(r"\text{(c)}\ \Pr[B] = \frac{2^{n-2}}{2^n} = \frac{1}{4}", font_size=42).move_to(UP * 0.1)
        pd = M(r"\text{(d)}\ \Pr[\overline{B}] = 1 - \Pr[B] = \frac{3}{4}", font_size=42).next_to(pc, DOWN, buff=0.5)
        with self.vo("So the probability of B is two to the n minus two over two to the n, which simplifies "
                     "to one quarter."):
            self.play(Write(pc))
        with self.vo("Part d asks for B bar, the complement: x does not start with zero zero. "
                     "Complements subtract from one, giving three quarters."):
            self.play(Write(pd))
            self.play(Create(boxed(pd)))
        tip = tx(r"Quiz 1 feedback: write the simplified answer $\tfrac34$, not $1 - \tfrac{2^{2n-2}}{2^{2n}}$", 30, BAD)
        tip.to_edge(DOWN, buff=0.6)
        with self.vo("On quiz one this exact answer was left unsimplified, and the grader asked for three "
                     "quarters. Always finish the arithmetic."):
            self.play(FadeIn(tip, shift=0.2 * UP))
        self.clear_all()


class Prob0b(VScene):
    def construct(self):
        self.header("Probability", "Exercise 2 (e), (f) + Quiz 1")
        row = bitrow("00" + "??" + "??" + "00", MSG, size=0.6, fs=32).move_to(UP * 1.7)
        VGroup(*row[:2]).set_color(HL)
        VGroup(*row[6:]).set_color(HL)
        with self.vo("Part e: A and B, a palindrome that starts with zero zero. Here's the trick: because it "
                     "is a palindrome, starting with zero zero forces it to end with zero zero too."):
            self.play(FadeIn(row))
            self.play(Indicate(VGroup(*row[6:]), color=HL))
        pe = M(r"\text{free bits} = \tfrac{n}{2} - 2", r"\quad\Rightarrow\quad",
               r"\text{(e)}\ \Pr[A \wedge B] = \frac{2^{n/2-2}}{2^n} = 2^{-n/2-2}", font_size=38).move_to(UP * 0.2)
        with self.vo("The palindrome is still decided by its first half, but now two of those bits are fixed. "
                     "That leaves n over two minus two free bits. Divide by two to the n."):
            self.play(Write(pe[0]))
            self.play(Write(pe[1:]))
            self.play(Create(boxed(pe[2])))
        chk = tx(r"check $n=4$: only \texttt{0000} \ $\Rightarrow \tfrac{1}{16} = 2^{-4}$ \checkmark", 30, GREY_A)
        chk.next_to(pe, DOWN, buff=0.5)
        with self.vo("Check with n equals four: the only such string is all zeros, one out of sixteen, which "
                     "is two to the minus four. It matches."):
            self.play(FadeIn(chk))
        self.clear_all()

        A = Circle(radius=1.5, color=C1, fill_opacity=0.2).move_to(LEFT * 3.6 + DOWN * 0.1)
        B = Circle(radius=1.5, color=C2, fill_opacity=0.2).move_to(LEFT * 1.9 + DOWN * 0.1)
        la = tx("A", 36, C1).move_to(A.get_center() + LEFT * 0.8)
        lb = tx("B", 36, C2).move_to(B.get_center() + RIGHT * 0.8)
        with self.vo("Part f asks for A or B. In math, or means at least one of them happens, including both."):
            self.play(DrawBorderThenFill(A), DrawBorderThenFill(B), FadeIn(la), FadeIn(lb))
        f1 = M(r"\Pr[A \vee B]", r"=", r"\Pr[A]", r"+", r"\Pr[B]", r"-", r"\Pr[A\wedge B]", font_size=36)
        f1.move_to(RIGHT * 2.9 + UP * 1.4)
        f2 = M(r"= 2^{-n/2} + \tfrac14 - 2^{-n/2-2}", font_size=36).next_to(f1, DOWN, buff=0.35, aligned_edge=LEFT).shift(RIGHT * 1.3)
        f3 = M(r"= \tfrac14 + \tfrac34 \cdot 2^{-n/2}", font_size=40, color=HL).next_to(f2, DOWN, buff=0.35, aligned_edge=LEFT)
        lens = Intersection(A, B, color=HL, fill_opacity=0.6, stroke_width=0)
        with self.vo("Adding the probability of A and the probability of B counts the overlap twice, so we "
                     "subtract it once. That's inclusion exclusion.") as d:
            self.play(Write(f1[:5]))
            self.play(FadeIn(lens))
            self.play(Write(f1[5:]))
        with self.vo("Plug in parts b, c and e. Two to the minus n over two, minus a quarter of it, leaves three "
                     "quarters of it. The answer: one quarter plus three quarters times two to the minus n over two."):
            self.play(Write(f2))
            self.play(Write(f3))
            self.play(Create(boxed(f3)))
        xor = tx(r"``or'' includes both. \ (Exclusive-or is the one that excludes both.)", 30, GREY_A).to_edge(DOWN, buff=0.5)
        with self.vo("Careful, because on quiz one, or got mixed up with exclusive or. Or is true when both sides are true."):
            self.play(FadeIn(xor))
        self.clear_all()

        q = qframe(r"Quiz 1: \ $x \xleftarrow{\$} \{0,1\}^{2n}$. \ What is $\Pr[A \mid B]$?", 38).move_to(UP * 2.0)
        with self.vo("Now the quiz version, which used strings of length two n and asked for the probability of "
                     "A given B. Take a moment to try it.") as d:
            self.play(FadeIn(q))
        self.wait(2.5)
        wrong = tx(r"Tempting: fix the first two \emph{and} last two bits $\Rightarrow \dfrac{2^{2n-4}}{2^{2n}}$", 32, BAD)
        wrong.next_to(q, DOWN, buff=0.5)
        cross = tx(r"counts strings that start and end with \texttt{00} --- most aren't palindromes!", 28, BAD)
        cross.next_to(wrong, DOWN, buff=0.2)
        with self.vo("The tempting answer, which is what was written on the quiz, fixes four bits and counts two "
                     "to the two n minus four strings. But that counts strings that start and end with zero zero, "
                     "and most of those are not palindromes. It also never divided by the probability of B."):
            self.play(FadeIn(wrong))
            self.play(FadeIn(cross))
        self.play(FadeOut(wrong), FadeOut(cross))
        steps = VGroup(
            M(r"\Pr[A \mid B] = \frac{\Pr[A \wedge B]}{\Pr[B]}", font_size=38),
            M(r"\Pr[A\wedge B] = \frac{2^{n-2}}{2^{2n}} \quad(\text{first half: } n \text{ bits, 2 fixed})", font_size=34),
            M(r"\Pr[A \mid B] = \frac{2^{n-2}/2^{2n}}{1/4} = \frac{2^{n}}{2^{2n}} = 2^{-n}", font_size=38),
        ).arrange(DOWN, buff=0.35).next_to(q, DOWN, buff=0.45)
        with self.vo("Do it right. Conditional probability is the probability of both, divided by the probability "
                     "of the condition.") as d:
            self.play(Write(steps[0]))
        with self.vo("With length two n, the first half has n bits, and two of them are fixed, so two to the n "
                     "minus two palindromes start with zero zero."):
            self.play(Write(steps[1]))
        with self.vo("Divide by one quarter, which multiplies by four, and we get two to the minus n."):
            self.play(Write(steps[2]))
            self.play(Create(boxed(steps[2])))
        punch = tx(r"$= \Pr[A]$: \ A and B are \textbf{independent}", 34, GOOD).to_edge(DOWN, buff=0.45)
        with self.vo("And here's a nice surprise: two to the minus n is exactly the probability of A by itself. "
                     "Knowing B happened tells you nothing about A. They are independent."):
            self.play(FadeIn(punch, shift=0.2 * UP))
        self.clear_all()


class Cond0(VScene):
    def construct(self):
        self.header("Conditioning", "Exercise 3")
        defs = VGroup(
            M(r"\Pr[X = 0] = \tfrac23,\quad \Pr[X=1] = \tfrac13", font_size=36),
            M(r"Y = \begin{cases} X & \text{prob. } 3/4 \\ 1 & \text{prob. } 1/4 \end{cases}", font_size=36),
        ).arrange(DOWN, buff=0.3).move_to(RIGHT * 2.6 + UP * 2.0)
        with self.vo("Exercise three. X is zero with probability two thirds and one with probability one third. "
                     "Then Y copies X with probability three quarters, and otherwise Y is just one."):
            self.play(FadeIn(defs, shift=0.2 * LEFT))
        root = Dot(LEFT * 6.3 + DOWN * 0.5)
        x0 = Dot(LEFT * 4.6 + UP * 0.7, color=C1)
        x1 = Dot(LEFT * 4.6 + DOWN * 1.7, color=C2)
        leaves = {
            "00": Dot(LEFT * 2.9 + UP * 1.4), "01": Dot(LEFT * 2.9 + DOWN * 0.0),
            "11a": Dot(LEFT * 2.9 + DOWN * 1.1), "11b": Dot(LEFT * 2.9 + DOWN * 2.5),
        }
        e = [Line(root, x0), Line(root, x1), Line(x0, leaves["00"]), Line(x0, leaves["01"]),
             Line(x1, leaves["11a"]), Line(x1, leaves["11b"])]
        lbl = [M(r"\tfrac23", font_size=28).move_to(e[0].get_center() + UL * 0.3),
               M(r"\tfrac13", font_size=28).move_to(e[1].get_center() + DL * 0.3),
               M(r"\tfrac34", font_size=26).move_to(e[2].get_center() + UP * 0.25),
               M(r"\tfrac14", font_size=26).move_to(e[3].get_center() + DOWN * 0.25),
               M(r"\tfrac34", font_size=26).move_to(e[4].get_center() + UP * 0.25),
               M(r"\tfrac14", font_size=26).move_to(e[5].get_center() + DOWN * 0.25)]
        nodes = [M("X=0", font_size=28, color=C1).next_to(x0, UP, buff=0.12),
                 M("X=1", font_size=28, color=C2).next_to(x1, DOWN, buff=0.12)]
        outs = [M("Y=0", font_size=28).next_to(leaves["00"], RIGHT), M("Y=1", font_size=28, color=HL).next_to(leaves["01"], RIGHT),
                M("Y=1", font_size=28, color=HL).next_to(leaves["11a"], RIGHT), M("Y=1", font_size=28, color=HL).next_to(leaves["11b"], RIGHT)]
        tree = VGroup(root, x0, x1, *leaves.values(), *e, *lbl, *nodes, *outs)
        with self.vo("Draw it as a tree. First X is chosen. Then Y either copies X, or is set to one.") as d:
            self.play(Create(VGroup(e[0], e[1])), FadeIn(VGroup(root, x0, x1, *nodes, lbl[0], lbl[1])))
            self.play(Create(VGroup(*e[2:])), FadeIn(VGroup(*leaves.values(), *lbl[2:], *outs)))
        f = VGroup(
            M(r"\Pr[Y{=}1] = \Pr[X{=}0]\,\Pr[Y{=}1 \mid X{=}0]", font_size=32),
            M(r"\qquad\quad + \Pr[X{=}1]\,\Pr[Y{=}1 \mid X{=}1]", font_size=32),
            M(r"= \tfrac23\cdot\tfrac14 + \tfrac13 \cdot 1 = \tfrac16 + \tfrac13 = \tfrac12", font_size=36),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(RIGHT * 2.6 + DOWN * 0.9)
        with self.vo("Part a wants the probability that Y equals one. The law of total probability says: split "
                     "on the value of X, and add up each branch, weighted by its probability.") as d:
            self.play(Write(f[0]), run_time=1.5)
            self.play(Write(f[1]), run_time=1.2)
        with self.vo("If X is zero, Y is one only through the one quarter branch. If X is one, Y is one no matter "
                     "which branch happens. Two thirds times a quarter, plus one third times one, is one half.") as d:
            self.play(Indicate(outs[1]), run_time=0.8)
            self.play(Indicate(VGroup(outs[2], outs[3])), run_time=0.8)
            self.play(Write(f[2]))
            fb = boxed(f[2])
            self.play(Create(fb))
        self.play(FadeOut(f), FadeOut(fb))
        bay = VGroup(
            M(r"\Pr[X{=}1 \mid Y{=}1] = \frac{\Pr[Y{=}1 \mid X{=}1]\,\Pr[X{=}1]}{\Pr[Y{=}1]}", font_size=32),
            M(r"= \frac{1 \cdot \tfrac13}{\tfrac12} = \tfrac23", font_size=36),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 2.6 + DOWN * 0.9)
        with self.vo("Part b flips the conditioning: given Y is one, how likely is it that X was one? That's "
                     "Bayes' rule: the reverse conditional, times the prior, divided by the probability of what we saw."):
            self.play(Write(bay[0]), run_time=2)
        with self.vo("One times one third, divided by one half, is two thirds. Seeing Y equals one doubled our "
                     "belief that X is one, from one third to two thirds."):
            self.play(Write(bay[1]))
            self.play(Create(boxed(bay[1])))
        self.clear_all()
        ub = VGroup(
            tx(r"\textbf{Union bound} \ (used all over the course)", 34, HL),
            M(r"\Pr[E_1 \vee E_2 \vee \dots \vee E_k] \;\le\; \Pr[E_1] + \Pr[E_2] + \dots + \Pr[E_k]", font_size=38),
            tx(r"equality when the events never overlap", 28, GREY_B),
        ).arrange(DOWN, buff=0.4)
        with self.vo("One more tool you'll see again: the union bound. The chance that at least one of several "
                     "events happens is at most the sum of their chances, because overlaps only make the left "
                     "side smaller."):
            self.play(FadeIn(ub[0]))
            self.play(Write(ub[1]), run_time=2)
            self.play(FadeIn(ub[2]))
        self.clear_all()


class Xor0(VScene):
    def construct(self):
        self.header("XOR", "Exercise 4")
        tt = VGroup(*[M(f"{a} \\oplus {b} = {a ^ b}", font_size=38, color=(HL if a ^ b else WHITE))
                      for a in (0, 1) for b in (0, 1)]).arrange(DOWN, buff=0.22).to_edge(LEFT, buff=1.0).shift(UP * 0.4)
        rule = tx(r"$1$ exactly when the bits \textbf{differ}", 30, HL).next_to(tt, DOWN, buff=0.4).align_to(tt, LEFT)
        with self.vo("XOR, written as a plus in a circle, compares two bits. The result is one exactly when the "
                     "bits differ, and zero when they match."):
            self.play(LaggedStart(*[FadeIn(r) for r in tt], lag_ratio=0.2))
            self.play(FadeIn(rule))
        xs, ys = "1011000", "0110101"
        zs = "".join(str(int(a) ^ int(b)) for a, b in zip(xs, ys))
        rx = bitrow(xs, MSG, size=0.5).move_to(RIGHT * 2.3 + UP * 1.4)
        ry = bitrow(ys, KEY, size=0.5).next_to(rx, DOWN, buff=0.2)
        line = Line(ry.get_left() + DOWN * 0.35, ry.get_right() + DOWN * 0.35, color=GREY_B)
        rz = bitrow(zs, HL, size=0.5).next_to(ry, DOWN, buff=0.5)
        lx = M("x", font_size=36, color=MSG).next_to(rx, LEFT)
        ly = M(r"y", font_size=36, color=KEY).next_to(ry, LEFT)
        lz = M(r"x \oplus y", font_size=34, color=HL).next_to(rz, LEFT)
        with self.vo("For strings, XOR works bit by bit. Here are x and y from the exercise."):
            self.play(FadeIn(rx), FadeIn(ry), FadeIn(lx), FadeIn(ly), Create(line))
        with self.vo("Go column by column: one and zero differ, so one. Zero and one differ, one. One and one "
                     "match, zero. And so on.") as d:
            for i in range(7):
                self.play(FadeIn(rz[i], shift=0.15 * DOWN), run_time=d / 9)
            self.play(FadeIn(lz))
        ans = tx(r"(a) \ $x \oplus y = \texttt{1101101}$", 36, HL).to_edge(DOWN, buff=0.8).shift(RIGHT * 2.3)
        with self.vo("So x XOR y is one one zero one one zero one."):
            self.play(Write(ans), Create(boxed(ans)))
        self.clear_all()

        laws = rows(r"$a \oplus a = 0$ \quad (anything XOR itself vanishes)",
                    r"$a \oplus 0 = a$ \quad (XOR with zero changes nothing)",
                    r"order and grouping don't matter", fs=34, buff=0.3).to_edge(UP, buff=1.2)
        with self.vo("Three rules make XOR algebra easy. Anything XOR itself is zero. XOR with zero changes "
                     "nothing. And, like addition, order and grouping don't matter.") as d:
            for l in laws:
                self.play(FadeIn(l, shift=0.2 * RIGHT))
                self.wait(d / 6)
        e1 = M(r"(x\oplus x)", r"\oplus", r"(y \oplus y)", r"\oplus", r"(x\oplus y)", r"\oplus", r"(y \oplus x)", font_size=40)
        e2 = M(r"0", r"\oplus", r"0", r"\oplus", r"(x\oplus y)", r"\oplus", r"(x \oplus y)", font_size=40)
        e3 = M(r"= 0^7 = \texttt{0000000}", font_size=40, color=HL)
        VGroup(e1, e2, e3).arrange(DOWN, buff=0.35).next_to(laws, DOWN, buff=0.5)
        with self.vo("Part b looks scary but collapses. The first two groups are things XOR themselves, so they "
                     "become zero. The last group, y XOR x, is the same as x XOR y.") as d:
            self.play(Write(e1), run_time=1.5)
            self.play(TransformFromCopy(e1, e2), run_time=1.2)
        with self.vo("Now x XOR y appears twice and cancels itself. The answer is seven zeros, no arithmetic needed."):
            self.play(Write(e3))
            self.play(Create(boxed(e3)))
        self.clear_all()
        pc = M(r"\text{(c)}\ \ z \xleftarrow{\$} \{0,1\}^7:\quad \Pr[z = x \oplus y] = \frac{1}{2^7} = \frac{1}{128}", font_size=40)
        pc.move_to(UP * 1.2)
        with self.vo("Part c. If z is uniform over seven bit strings, the chance it equals one particular string "
                     "is one over two to the seven, one over one hundred twenty eight."):
            self.play(Write(pc))
            self.play(Create(boxed(pc)))
        tease = VGroup(tx(r"Coming up (week 1): XOR \emph{undoes itself}", 34, KEY),
                       M(r"(m \oplus k) \oplus k = m \oplus (k \oplus k) = m \oplus 0 = m", font_size=40)).arrange(DOWN, buff=0.3)
        tease.next_to(pc, DOWN, buff=0.8)
        with self.vo("Keep these rules in mind. XOR with a key, then XOR with the same key again, and you get the "
                     "message back. That is exactly how the one time pad decrypts."):
            self.play(FadeIn(tease[0]))
            self.play(Write(tease[1]))
        self.clear_all()


class Mod0(VScene):
    def construct(self):
        self.header("Remainders", "Exercise 5")
        d = M(r"a = k\cdot m + r, \qquad 0 \le r < m", r"\qquad [a \bmod m] = r", font_size=40).to_edge(UP, buff=1.2)
        with self.vo("Square brackets a mod m means the remainder when a is divided by m: write a as a multiple "
                     "of m plus a leftover r between zero and m minus one."):
            self.play(Write(d[0]))
            self.play(Write(d[1]))
        circ = Circle(radius=1.3, color=GREY_B).move_to(LEFT * 3.8 + DOWN * 0.9)
        pts = [circ.point_at_angle(PI / 2 - i * TAU / 4) for i in range(4)]
        dots = VGroup(*[Dot(p, color=C1) for p in pts])
        nums = VGroup(*[M(str(i), font_size=34).move_to(circ.get_center() + 1.75 * (p - circ.get_center()) / 1.3)
                        for i, p in enumerate(pts)])
        with self.vo("Picture a clock with four positions, zero to three. Counting mod four means walking "
                     "around this clock."):
            self.play(Create(circ), FadeIn(dots), FadeIn(nums))
        pa = M(r"\text{(a)}\ 17 + 20 = 37 = 9\cdot 4 + 1 \;\Rightarrow\; 1", font_size=38).move_to(RIGHT * 2.4 + UP * 0.4)
        with self.vo("Part a. Seventeen plus twenty is thirty seven, which is nine fours plus one. "
                     "So the remainder is one."):
            self.play(Write(pa))
            self.play(Indicate(nums[1], color=HL, scale_factor=1.5))
        pb = VGroup(M(r"\text{(b)}\ 17 \equiv 1,\quad 82 \equiv 2 \pmod 4", font_size=38),
                    M(r"17\cdot 82 \equiv 1 \cdot 2 = 2", font_size=38, color=HL)).arrange(DOWN, buff=0.3)
        pb.next_to(pa, DOWN, buff=0.6)
        with self.vo("Part b is the useful trick: reduce first, then multiply. Seventeen leaves remainder one, "
                     "eighty two leaves remainder two, so the product leaves one times two, which is two."):
            self.play(Write(pb[0]))
            self.play(Write(pb[1]))
            self.play(Create(boxed(pb[1])))
        why = tx(r"Allowed because remainders respect $+$ and $\times$ (Week 3, Prop.\ 3.1)", 28, GREY_B).to_edge(DOWN, buff=0.5)
        with self.vo("You never need to compute the big product. This works because remainders respect addition "
                     "and multiplication, a fact we'll prove in week three."):
            self.play(FadeIn(why))
        self.clear_all()


class Logic0(VScene):
    def construct(self):
        self.header("Logic", "Exercise 6 (= Quiz 1, Q3)")
        claim = VGroup(tx(r"Claim: \ for all positive integers $n$:", 34),
                       tx(r"$n$ is composite \ \textbf{or} \ there exists a positive integer $k$ with $n = 2k+1$", 32))
        claim.arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(UP, buff=1.15)
        with self.vo("Exercise six gives a false claim: for every positive integer n, either n is composite, or "
                     "n equals two k plus one for some positive integer k. In plain words: every number is "
                     "composite, or odd and at least three."):
            self.play(FadeIn(claim, shift=0.2 * DOWN))
        rules = VGroup(
            M(r"\text{not}(\forall x,\ P) \;\equiv\; \exists x,\ \text{not } P", font_size=34),
            M(r"\text{not}(\exists x,\ P) \;\equiv\; \forall x,\ \text{not } P", font_size=34),
            M(r"\text{not}(P \text{ or } Q) \;\equiv\; (\text{not } P) \text{ and } (\text{not } Q)", font_size=34),
            M(r"\text{not}(n = 2k+1) \;\equiv\; n \ne 2k+1", font_size=34),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(claim, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
        with self.vo("To negate it, push the not inside, one layer at a time, using four rules. For all flips to "
                     "there exists. There exists flips to for all. Or flips to and. And equals flips to not "
                     "equals.") as d:
            for r in rules:
                self.play(FadeIn(r, shift=0.2 * RIGHT), run_time=0.7)
                self.wait(d / 8)
        neg = VGroup(tx(r"\textbf{Negation:} there \emph{exists} a positive integer $n$ such that", 32, HL),
                     tx(r"$n$ is \emph{not} composite \ \textbf{and} \ for \emph{all} positive integers $k$, \ $n \ne 2k+1$", 32, HL))
        neg.arrange(DOWN, buff=0.18, aligned_edge=LEFT).to_edge(DOWN, buff=0.6)
        with self.vo("Apply every rule and you get: there exists a positive integer n such that n is not composite, "
                     "and for all positive integers k, n is not two k plus one. On the quiz, the for all and there "
                     "exists flips were missed. Every quantifier must flip."):
            self.play(Write(neg), run_time=3)
            self.play(Create(boxed(neg)))
        self.clear_all()
        q = qframe(r"Disprove: which $n$ makes the negation true?").move_to(UP * 2.0)
        with self.vo("Part b: disprove the claim. That means finding one n that makes the negation true. Try it."):
            self.play(FadeIn(q))
        self.wait(2.5)
        sol = rows(r"$n = 2$: \ 2 is prime, so \emph{not} composite \checkmark",
                   r"$2 = 2k+1 \Rightarrow k = \tfrac12$, \ not an integer, so $2 \ne 2k+1$ for every $k$ \checkmark",
                   r"Both parts of the negation hold $\Rightarrow$ the claim is \textbf{false}.",
                   fs=32, buff=0.3).next_to(q, DOWN, buff=0.6)
        with self.vo("Take n equals two. Two is prime, so it is not composite. And two equals two k plus one would "
                     "need k to be one half, which isn't an integer. Both halves of the negation hold, so the "
                     "claim is false. One also works, because k equals zero is not positive.") as d:
            for s in sol:
                self.play(FadeIn(s, shift=0.2 * RIGHT))
                self.wait(d / 5)
        orx = tx(r"Reminder: ``$P$ or $Q$'' is \textbf{true when both} are true (e.g.\ $n=9$: composite \emph{and} odd).", 28, GREY_A)
        orx.to_edge(DOWN, buff=0.5)
        with self.vo("And remember, or in math is inclusive. Nine is composite and also odd, and the claim's or is "
                     "perfectly happy with that. Nine is not a counterexample."):
            self.play(FadeIn(orx))
        self.clear_all()


class Runtime0(VScene):
    def construct(self):
        self.header("Running time", "Exercise 7")
        algs = VGroup(
            algo(r"(a) $A_1(x)$", [r"for $i = 1,\dots,n$:", r">print $i$"], fs=28),
            algo(r"(b) $A_2(x)$", [r"for $i = 1,\dots,n$:", r">for $j=1,\dots,n$:", r">>print $j$"], fs=28),
            algo(r"(c) $A_3(x)$", [r"while $x \ne 0^n$:", r">$x := x - 1$"], fs=28),
            algo(r"(d) $A_4(x)$", [r"$i := 1$", r"while $i \le n$:", r">$i := 2i$"], fs=28),
        ).arrange_in_grid(rows=1, buff=0.3).to_edge(UP, buff=1.2)
        fit(algs, 13.0)
        with self.vo("Exercise seven: four algorithms on an n bit input x. To find a running time, count how many "
                     "times each loop runs, as a function of n."):
            self.play(LaggedStart(*[FadeIn(a, shift=0.2 * DOWN) for a in algs], lag_ratio=0.2))
        ans = [M(r"\Theta(n)", font_size=40), M(r"\Theta(n^2)", font_size=40), M(r"\Theta(2^n)", font_size=40, color=BAD),
               M(r"\Theta(\log n)", font_size=40)]
        for a, alg in zip(ans, algs):
            a.next_to(alg, DOWN, buff=0.4)
        notes = [r"one pass, $n$ steps", r"$n$ passes of $n$ steps", r"$x$ can be $2^n - 1$!", r"$1,2,4,\dots$ passes $n$ fast"]
        nts = [tx(s, 24, GREY_B).next_to(a, DOWN, buff=0.2) for s, a in zip(notes, ans)]
        with self.vo("The first loop runs n times: order n. The second runs n times inside n times: order n squared."):
            self.play(Write(ans[0]), FadeIn(nts[0]))
            self.play(Write(ans[1]), FadeIn(nts[1]))
        with self.vo("The third is the trap. It counts x down to zero, one at a time. An n bit number can be as "
                     "large as two to the n minus one, so in the worst case the loop runs about two to the n times. "
                     "That's exponential."):
            self.play(Write(ans[2]), FadeIn(nts[2]))
            self.play(Indicate(ans[2], color=BAD))
        with self.vo("The fourth doubles i each time: one, two, four, eight. It passes n after about log n doublings."):
            self.play(Write(ans[3]), FadeIn(nts[3]))
        take = tx(r"Running time is measured in the \textbf{length} of the input ($n$ bits), not its numeric \textbf{value}.", 30, HL)
        take.to_edge(DOWN, buff=0.45)
        with self.vo("Here's the lesson that matters all semester: running time is measured against the length of "
                     "the input, n bits, not the number's value. Looping up to the value of x is exponential in n. "
                     "This idea becomes probabilistic polynomial time in week two."):
            self.play(FadeIn(take, shift=0.2 * UP))
            self.play(Create(boxed(take)))
        self.clear_all()


class Recap0(VScene):
    def construct(self):
        self.header("Part 0", "recap")
        r = recap_list([r"Uniform probability = (count of good strings) / $2^n$. Check tiny cases.",
                        r"Palindromes: first half decides everything $\Rightarrow 2^{n/2}$ of them.",
                        r"Conditional $= \Pr[\text{both}]/\Pr[\text{condition}]$; total probability splits into cases.",
                        r"XOR: $a\oplus a = 0$, $a \oplus 0 = a$, so XOR with $k$ twice undoes itself.",
                        r"Negate by flipping $\forall\leftrightarrow\exists$, or$\leftrightarrow$and, $=\ \leftrightarrow\ \neq$.",
                        r"Time counts in input \emph{length}: a loop to $x$ is $2^n$ for $n$-bit $x$."], fs=30)
        fit(r, 12.8).move_to(DOWN * 0.2)
        with self.vo("Let's recap the toolkit. Uniform probabilities are counts over two to the n, and you should "
                     "always check a tiny case. Palindromes are decided by their first half. Conditional "
                     "probability divides by the condition. XOR undoes itself. Negations flip every quantifier and "
                     "every or. And running time is measured in input length.") as d:
            for line in r:
                self.play(FadeIn(line, shift=0.2 * RIGHT), run_time=0.6)
                self.wait(d / 8)
        nxt = tx(r"Next: Part 1 --- encryption and perfect secrecy", 34, HL).to_edge(DOWN, buff=0.4)
        with self.vo("Next up, part one: encryption, and the first real security definition, perfect secrecy."):
            self.play(FadeIn(nxt))
        self.wait(1)
