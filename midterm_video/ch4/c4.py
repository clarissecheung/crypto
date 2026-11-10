from cx import *

QR77 = {r * r % 77 for r in range(1, 77) if r % 7 and r % 11}


class Intro4(VScene):
    def construct(self):
        title = tx(r"\textbf{Part 4: Hiding One Bit}", 52, HL).move_to(UP * 0.4)
        sub = tx(r"Week 4 \quad (notes chapter 4)", 30, GREY_A).next_to(title, DOWN)
        with self.vo("Part four: hiding one bit."):
            self.play(Write(title), FadeIn(sub))
        self.play(FadeOut(title), FadeOut(sub))
        self.header("Part 4", "can squaring encrypt?")
        idea = M(r"\mathrm{Enc}(m) = [\,m^2 \bmod N\,] \ ?", font_size=48, color=CT).to_edge(UP, buff=1.2)
        with self.vo("Part three showed squaring mod N is hard to undo without the factors. So why not encrypt a message "
                     "m by squaring it?"):
            self.play(Write(idea))
        probs = VGroup(tx(r"\textbf{Correctness:} \ the decryptor finds \emph{four} roots. \ Which one was $m$?", 32),
                       tx(r"\textbf{Security:} \ Theorem 3.3 only says Eve can't recover \emph{all} of a \emph{random} $m$.", 32),
                       tx(r"\qquad It allows learning \emph{part} of $m$, or all of a non-random $m$ (``yes''/``no'').", 30, GREY_A)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        probs.next_to(idea, DOWN, buff=0.6)
        fit(probs, 12.9)
        with self.vo("Two problems. Correctness: even with the factors, Bob finds four square roots and can't tell which "
                     "was m. Security: theorem three point three only says Eve can't recover the whole message when it's "
                     "uniformly random. She might still learn part of it, and real messages aren't random. If Alice only "
                     "ever sends yes or no, Eve just squares both and compares.") as d:
            for x in probs:
                self.play(FadeIn(x, shift=0.2 * RIGHT))
                self.wait(d / 6)
        q = qframe(r"If $x \mapsto x^2 \bmod N$ is hard to invert, \emph{what} exactly does $x^2$ hide about $x$?", 34).to_edge(DOWN, buff=0.6)
        with self.vo("So the real question is: if squaring is hard to undo, what specific information about x does x "
                     "squared hide? The answer: its last bit."):
            self.play(FadeIn(q))
        self.clear_all()


class LSB4(VScene):
    def construct(self):
        self.header("Least significant bit", r"Def.\ 4.1")
        d = VGroup(M(r"\mathrm{LSB}(x) = \begin{cases} 0 & [x \bmod N] \text{ even} \\ 1 & [x \bmod N] \text{ odd} \end{cases}", font_size=40),
                   tx(r"(use the representative in $\{0,\dots,N-1\}$: mod 5, $2 \equiv 7$ but we read $2$, so LSB $= 0$)", 28, GREY_A)).arrange(DOWN, buff=0.3)
        d.to_edge(UP, buff=1.15)
        with self.vo("The least significant bit of x is just its parity: zero if even, one if odd, read off the standard "
                     "representative between zero and N minus one."):
            self.play(Write(d[0]))
            self.play(FadeIn(d[1]))
        a1 = VGroup(tx(r"\textbf{Attempt 1:} \ ``$\Pr[A \text{ guesses } \mathrm{LSB}(x)]$ is negligible'' \ --- \ \textbf{impossible}", 32, BAD),
                    tx(r"a coin flip is right half the time. \ Fix: require $\Pr < \tfrac12 + \mathrm{negl}(n)$.", 30)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        a1.next_to(d, DOWN, buff=0.5)
        with self.vo("How should we say squaring hides the LSB? First attempt: no efficient algorithm guesses the LSB "
                     "except with negligible probability. Impossible: flipping a coin is right half the time. So instead "
                     "we require success at most one half plus negligible."):
            self.play(FadeIn(a1))
        self.clear_all()
        a2 = tx(r"\textbf{Attempt 2:} \ $x \xleftarrow{\$} \mathbb Z_N^*$, \ $y = x^2$. \ Guessing LSB$(x)$ from $y$ is \emph{trivially} $\tfrac12$. \ Why?", 32, HL)
        a2.to_edge(UP, buff=1.15)
        fit(a2, 12.9)
        with self.vo("Second attempt: pick x from all of Z N star, square it, and ask for the LSB of x. Now the statement "
                     "is true, but trivially. Here's why, with N equals seventy seven and y equals twenty three."):
            self.play(FadeIn(a2))
        roots = [10, 32, 45, 67]
        cells = VGroup()
        for r in roots:
            col = GOOD if r % 2 == 0 else BAD
            c = VGroup(M(str(r), font_size=44), tx(f"LSB $= {r % 2}$", 28, col)).arrange(DOWN, buff=0.15)
            cells.add(c)
        cells.arrange(RIGHT, buff=1.3).move_to(UP * 0.2)
        arcs = VGroup(CurvedArrow(cells[0].get_bottom() + DOWN * 0.1, cells[3].get_bottom() + DOWN * 0.1, angle=PI / 3, color=GREY_B),
                      CurvedArrow(cells[1].get_bottom() + DOWN * 0.1, cells[2].get_bottom() + DOWN * 0.1, angle=PI / 3, color=GREY_B))
        with self.vo("Twenty three has four square roots: ten, thirty two, forty five, sixty seven. Two are even and two "
                     "are odd. That's no accident. Roots come in pairs, x and N minus x, and since N is odd, those two "
                     "always have opposite parity. Ten pairs with sixty seven, thirty two with forty five.") as dd:
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.2))
            self.play(Create(arcs))
        cl = tx(r"Claim 4.1: exactly half the roots of any $y$ have LSB $0$. \ ``The'' root of $y$ isn't defined, so $y$ says nothing.", 30, BAD)
        cl.to_edge(DOWN, buff=0.6)
        fit(cl, 12.9)
        with self.vo("So given y, the root x is equally likely to be even or odd. The LSB of the square root of y isn't "
                     "even well defined, so of course nobody can predict it. We need to pick out one special root."):
            self.play(FadeIn(cl))
        self.clear_all()


class Principal4(VScene):
    def construct(self):
        self.header("The principal root", "Lemma 4.1")
        lm = VGroup(tx(r"\textbf{Lemma 4.1} (= Ex.\ 3.8(c)): \ $N$ Blum, $y \in QR_N$ $\Rightarrow$ exactly \textbf{one} root of $y$ is in $QR_N$.", 32, HL),
                    tx(r"Call it the \textbf{principal root}. \ (Like $\sqrt{4} = 2$, not $-2$.)", 32)).arrange(DOWN, buff=0.25)
        lm.to_edge(UP, buff=1.15)
        fit(lm, 12.9)
        with self.vo("Here's the special root, from exercise three point eight. For a Blum integer, exactly one of the four "
                     "roots is itself a quadratic residue. We call it the principal root, the way the square root of four "
                     "means two, not minus two."):
            self.play(FadeIn(lm[0]))
            self.play(FadeIn(lm[1]))
        roots = [10, 32, 45, 67]
        cells = VGroup()
        for r in roots:
            isq = r in QR77
            c = VGroup(M(str(r), font_size=44, color=HL if isq else WHITE),
                       tx(r"$\in QR_{77}$" if isq else r"$\notin QR_{77}$", 28, GOOD if isq else GREY_B)).arrange(DOWN, buff=0.15)
            cells.add(c)
        cells.arrange(RIGHT, buff=1.3).move_to(UP * 0.0)
        with self.vo("For twenty three mod seventy seven, that's sixty seven, as we found in part three."):
            self.play(FadeIn(cells))
            self.play(Create(boxed(cells[3])))
        th = VGroup(tx(r"\textbf{Theorem 4.3.} If Factoring, then for every PPT $A$:", 32),
                    M(r"\Pr\big[A(N, y) = \mathrm{LSB}(x)\big] < \tfrac12 + \mathrm{negl}(n)", font_size=40, color=HL),
                    tx(r"where $N \leftarrow \mathrm{Blum}(1^n)$, \ $x \xleftarrow{\$} QR_N$ (so $x$ \emph{is} the principal root), \ $y = x^2$", 30)).arrange(DOWN, buff=0.25)
        th.to_edge(DOWN, buff=0.5)
        fit(th, 12.9)
        with self.vo("Now the real theorem. Sample x from the quadratic residues, so x is the principal root of y. If "
                     "factoring is hard, no efficient algorithm given N and y guesses the LSB of x with probability "
                     "noticeably better than one half. Squaring hides the last bit of the principal root."):
            self.play(FadeIn(th[0]))
            self.play(Write(th[1]))
            self.play(FadeIn(th[2]))
        self.clear_all()


class Lemma42(VScene):
    def construct(self):
        self.header("Lemma 4.2", r"perfect LSB $\Rightarrow$ square roots")
        st = VGroup(tx(r"Full proof of Thm 4.3: beyond the course. \ We prove the key step:", 32),
                    tx(r"If $A$ \emph{always} outputs LSB of the principal root (and $2 \in QR_N$), we can find the root itself.", 32, HL)).arrange(DOWN, buff=0.25)
        st.to_edge(UP, buff=1.15)
        fit(st, 12.9)
        with self.vo("The full proof is beyond the course, but lemma four point two shows the main idea. Suppose A always "
                     "returns the LSB of the principal root, and two happens to be a residue mod N. Then we can compute "
                     "the whole principal root, which breaks theorem three point three."):
            self.play(FadeIn(st))
        idea = VGroup(tx(r"\textbf{Idea:} \ read the binary digits of $x/N = 0.b_1 b_2 b_3\dots$ \ one at a time.", 32),
                      M(r"2^i x = N \cdot \Big\lfloor \tfrac{2^i x}{N} \Big\rfloor + [\,2^i x \bmod N\,]", font_size=40),
                      tx(r"left side even, $N$ odd $\Rightarrow$ \ $b_i = $ parity of $\lfloor 2^i x / N\rfloor$ $= \mathrm{LSB}([2^i x \bmod N])$", 30),
                      tx(r"and $2^i x$ is the principal root of $4^i y$ (both $2, x \in QR_N$), so \ $b_i = A(N, [4^i y \bmod N])$", 30, GOOD)).arrange(DOWN, buff=0.3)
        idea.next_to(st, DOWN, buff=0.45)
        fit(idea, 12.9)
        with self.vo("The idea: learn the binary expansion of x over N, one digit at a time. Multiplying by two to the i "
                     "shifts the digits, and the i th digit is the parity of the whole part of two to the i x over N.") as d:
            self.play(FadeIn(idea[0]))
            self.play(Write(idea[1]))
        with self.vo("Here's the trick. Two to the i x equals N times that whole part, plus the remainder. The left side is "
                     "even and N is odd, so the whole part and the remainder have the same parity. So the i th digit is "
                     "the LSB of two to the i x mod N. And two to the i x is the principal root of four to the i y, because "
                     "two and x are both residues. So A, run on four to the i y, hands us digit i."):
            self.play(FadeIn(idea[2]))
            self.play(FadeIn(idea[3]))
        self.clear_all()
        ex = tx(r"\textbf{Example:} \ $N = 161 = 7\cdot 23$ (2 is a QR), \ secret $x = 100$, \ $B$ sees only $y = 18$", 32, HL).to_edge(UP, buff=1.15)
        with self.vo("Let's watch it work. N is one sixty one, the secret principal root is one hundred, and B only sees "
                     "y equals eighteen."):
            self.play(FadeIn(ex))
        vals = [39, 78, 156, 151, 141, 121, 81, 1, 2]
        hdr = VGroup(tx("$i$", 28, GREY_A), tx(r"$[2^i x \bmod N]$", 28, GREY_A), tx(r"$b_i$ = LSB", 28, HL))
        cols = [hdr]
        for i, v in enumerate(vals, 1):
            cols.append(VGroup(M(str(i), font_size=30), M(str(v), font_size=30), M(str(v % 2), font_size=32, color=HL)))
        tbl = VGroup(*cols)
        for c in tbl:
            c.arrange(DOWN, buff=0.3)
        tbl.arrange(RIGHT, buff=0.42).next_to(ex, DOWN, buff=0.5)
        fit(tbl, 12.9)
        with self.vo("B asks A about four y, sixteen y, and so on. A answers with the parities of two x, four x, eight x "
                     "mod N: one, zero, zero, one, one, one, one, one, zero. B never sees the middle row; it's only "
                     "there so we can check A's answers.") as d:
            self.play(FadeIn(tbl[0]))
            for c in tbl[1:]:
                self.play(FadeIn(c), run_time=d / 14)
        res = VGroup(M(r"\hat x = N \cdot 0.100111110_2 = 161 \cdot \tfrac{318}{512} \approx 99.996", font_size=36),
                     M(r"\mathrm{Round}(\hat x) = 100 = x \;\checkmark", font_size=40, color=GOOD),
                     tx(r"$k = \lceil \log_2 N\rceil + 1$ digits make the error $< N 2^{-k} < \tfrac12$, so rounding is exact.", 28, GREY_A)).arrange(DOWN, buff=0.3)
        res.next_to(tbl, DOWN, buff=0.5)
        fit(res, 12.9)
        with self.vo("Put those digits after a binary point and multiply by N: about ninety nine point nine nine six. "
                     "Round it: one hundred, the secret root. Using about log N digits makes the error less than one "
                     "half, so rounding is always exact."):
            self.play(Write(res[0]))
            self.play(Write(res[1]))
            self.play(FadeIn(res[2]))
        self.clear_all()


class Ex41(VScene):
    def construct(self):
        self.header("Exam-style", r"Ex.\ 4.1 (= Quiz 5 Q1)")
        q = VGroup(tx(r"Show these are equivalent (predictors $A$ output a bit):", 32),
                   M(r"\text{(1)}\ \ \mathrm{Adv}_A < \tfrac12 + \mathrm{negl}(n) \qquad\quad \text{(2)}\ \ \big|\mathrm{Adv}_A - \tfrac12\big| \text{ is negligible}", font_size=36)).arrange(DOWN, buff=0.3)
        q.to_edge(UP, buff=1.15)
        with self.vo("Exercise four point one, quiz five question one. Show that saying every predictor's success is below "
                     "one half plus negligible is the same as saying it's within negligible of one half, on both sides."):
            self.play(FadeIn(q))
        e = VGroup(tx(r"(2) $\Rightarrow$ (1): \ $\mathrm{Adv} - \tfrac12 \le |\mathrm{Adv} - \tfrac12| = $ negligible. \ Done.", 30),
                   tx(r"(1) $\Rightarrow$ (2): \ the danger is $\mathrm{Adv}_A$ far \emph{below} $\tfrac12$. \ Use the \textbf{flipped predictor}:", 30),
                   algo(r"$\bar A(z)$", [r"return $1 - A(z)$"], fs=30, title_color=HON),
                   M(r"\mathrm{Adv}_{\bar A} = 1 - \mathrm{Adv}_A \overset{(1)}{<} \tfrac12 + \mathrm{negl}' \;\Rightarrow\; \mathrm{Adv}_A > \tfrac12 - \mathrm{negl}'", font_size=36),
                   tx(r"So $\tfrac12 - \mathrm{negl}' < \mathrm{Adv}_A < \tfrac12 + \mathrm{negl}$, \ i.e.\ $|\mathrm{Adv}_A - \tfrac12| < \mathrm{negl} + \mathrm{negl}'$: negligible. $\blacksquare$", 30, GOOD)).arrange(DOWN, buff=0.28)
        e.next_to(q, DOWN, buff=0.4)
        fit(e, 12.9)
        with self.vo("One direction is free: a quantity is at most its absolute value. For the other, the worry is a "
                     "predictor that's right far less than half the time. But such a predictor is secretly great: flip its "
                     "answers. The flipped predictor A bar is also efficient, and it's right exactly when A is wrong.") as d:
            self.play(FadeIn(e[0]))
            self.play(FadeIn(e[1]))
            self.play(FadeIn(e[2]))
        with self.vo("Apply statement one to A bar: one minus A's advantage is below one half plus negligible. Rearranged, "
                     "A's advantage is above one half minus negligible. Together with statement one for A itself, A is "
                     "within a negligible distance of one half. That flip is the predictor the grader was looking for."):
            self.play(Write(e[3]))
            self.play(FadeIn(e[4]))
        self.clear_all()


class Ex42(VScene):
    def construct(self):
        self.header("Exam-style", r"Ex.\ 4.2: sampling domains")
        a = VGroup(tx(r"\textbf{(a)} \ $\Pr_{x \leftarrow \mathbb Z_N^*}[\pi(x)]$ negl $\Rightarrow$ $\Pr_{x \leftarrow QR_N}[\pi(x)]$ negl", 32, HL),
                   M(r"\Pr_{QR_N}[\pi] = \frac{|\{x \in QR_N : \pi(x)\}|}{|QR_N|} \le \frac{|\{x \in \mathbb Z_N^* : \pi(x)\}|}{|\mathbb Z_N^*|/4} = 4\Pr_{\mathbb Z_N^*}[\pi]", font_size=34),
                   tx(r"$4 \times$ negligible is negligible. \ ($QR_N$ is a quarter of $\mathbb Z_N^*$.)", 30, GOOD)).arrange(DOWN, buff=0.25)
        a.to_edge(UP, buff=1.15)
        fit(a, 12.9)
        with self.vo("Exercise four point two. Part a: if a property is rare among all units, it's rare among the residues. "
                     "The residues are a quarter of the units, so restricting to them can boost a probability by at most "
                     "a factor of four. Four times negligible is negligible."):
            self.play(FadeIn(a[0]))
            self.play(Write(a[1]), run_time=2)
            self.play(FadeIn(a[2]))
        b = VGroup(tx(r"\textbf{(b)} \ Thm 3.3 with $x \xleftarrow{\$} QR_N$ instead of $\mathbb Z_N^*$: \ \emph{same theorem!}", 32, HL),
                   tx(r"$A$ only sees $y = x^2$. \ Both ways, $y$ is \textbf{uniform on $QR_N$}: same input distribution, same success.", 30)).arrange(DOWN, buff=0.2)
        b.next_to(a, DOWN, buff=0.45)
        fit(b, 12.9)
        with self.vo("Part b: theorem three point three, but with x sampled from the residues. No new reduction needed. The "
                     "algorithm only sees y, and y is a uniform residue either way. Same input distribution, same success "
                     "probability, so it's negligible by theorem three point three."):
            self.play(FadeIn(b))
        c = VGroup(tx(r"\textbf{(c)} \ Reduction $B'$ samples $x \xleftarrow{\$} QR_N$. \ What breaks?", 32, HL),
                   tx(r"``$x$ is uniform among the 4 roots, so $\Pr[\hat x \equiv \pm x] = \tfrac12$'' is now \textbf{false}:", 30),
                   tx(r"$x$ is always the principal root. \ An $A$ that returns the principal root makes $B'$ \emph{always} abort.", 30, BAD)).arrange(DOWN, buff=0.2)
        c.next_to(b, DOWN, buff=0.45)
        fit(c, 12.9)
        with self.vo("Part c: what if the reduction itself sampled x from the residues? Then the sentence x is uniform among "
                     "the four roots is false: x is always the principal root. An A that always returns the principal root "
                     "returns x every time, and B prime always gives up. Where the reduction samples matters."):
            self.play(FadeIn(c))
        self.clear_all()


class Ex43(VScene):
    def construct(self):
        self.header("Exam-style", r"Ex.\ 4.3 (= Quiz 5 Q2)")
        q = VGroup(tx(r"$A$ finds the principal root of a \textbf{uniformly random} $y \in QR_N$ w.p.\ $\varepsilon(n)$.", 32),
                   tx(r"Build $B$ that finds the principal root of one \textbf{fixed, special} $y^*$ w.p.\ $\varepsilon(n)$.", 32, HL)).arrange(DOWN, buff=0.2)
        q.to_edge(UP, buff=1.15)
        fit(q, 12.9)
        with self.vo("Exercise four point three, quiz five question two. A finds principal roots of random residues. But we "
                     "need the root of one particular, fixed residue, y star. A might fail on that one every time. How do "
                     "we use A anyway?"):
            self.play(FadeIn(q))
        idea = tx(r"\textbf{Idea: re-randomize.} Disguise $y^*$ as a random residue, ask $A$, then undo the disguise.", 32, GOOD).next_to(q, DOWN, buff=0.4)
        with self.vo("The idea is called re randomizing. Disguise y star as a uniformly random residue, ask A, then remove "
                     "the disguise."):
            self.play(FadeIn(idea))
        alg = algo(r"$B(N, y^*)$", [r"$r \xleftarrow{\$} \mathbb Z_N^*$; \ $a := [r^2 \bmod N]$ \qquad // random $a \in QR_N$",
                                    r"$y' := [\,y^* \cdot a^2 \bmod N\,]$ \qquad // uniform in $QR_N$",
                                    r"$x' \leftarrow A(N, y')$",
                                    r"return $\hat x := [\,x' \cdot a^{-1} \bmod N\,]$"], fs=30).next_to(idea, DOWN, buff=0.35)
        with self.vo("Here's B. Pick a random residue a, by squaring a random unit. Multiply y star by a squared. Ask A for "
                     "the principal root of that, and divide the answer by a.") as d:
            self.play(FadeIn(alg[0]), FadeIn(alg[1]))
            for ln in alg[2]:
                self.play(FadeIn(ln, shift=0.15 * RIGHT))
                self.wait(d / 10)
        self.clear_all()
        why = VGroup(tx(r"\textbf{Why it works}", 34, HL),
                     tx(r"\textbf{Distribution:} for Blum $N$, $a \mapsto a^2$ is a bijection on $QR_N$, and $\times y^*$ is too.", 30),
                     tx(r"\qquad So $y'$ is \emph{exactly} uniform on $QR_N$: $A$ succeeds w.p.\ $\varepsilon(n)$, as promised.", 30),
                     tx(r"\textbf{Root:} \ $\hat x^2 = x'^2 a^{-2} \equiv y^* a^2 a^{-2} = y^*$ \checkmark", 30),
                     tx(r"\textbf{Principal:} \ $x' \in QR_N$ and $a^{-1} \in QR_N$ $\Rightarrow$ $\hat x \in QR_N$ \checkmark", 30),
                     tx(r"Note: with $a$ merely in $\mathbb Z_N^*$, $x' a^{-1}$ is \emph{a} root, but principal only $\tfrac14$ of the time.", 28, GREY_A)).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        fit(why, 12.9)
        with self.vo("Why it works. First, the disguise is perfect. For a Blum integer, squaring is a one to one map on the "
                     "residues, and so is multiplying by y star. So y prime is exactly a uniform residue, and A succeeds "
                     "with probability epsilon.") as d:
            self.play(FadeIn(why[0]), FadeIn(why[1]), FadeIn(why[2]))
        with self.vo("Second, x hat squared is x prime squared over a squared, which is y star. Third, x prime and a inverse "
                     "are both residues, so x hat is a residue: the principal root. One caution: if a were just any unit, "
                     "x prime over a would be a square root, but only the principal one a quarter of the time. That's why "
                     "we choose a as a square."):
            self.play(FadeIn(why[3]))
            self.play(FadeIn(why[4]))
            self.play(FadeIn(why[5]))
        self.clear_all()


class Outro4(VScene):
    def construct(self):
        self.header("Part 4", "we can encrypt one bit")
        enc = algo(r"$\mathrm{Enc}_N(m)$ \ for $m \in \{0, 1\}$",
                   [r"$x \xleftarrow{\$} QR_N$", r"$y := [x^2 \bmod N]$", r"return $c := (\mathrm{LSB}(x) \oplus m,\ y)$"], fs=32)
        enc.move_to(LEFT * 3.3 + UP * 0.6)
        with self.vo("Here's the payoff. To encrypt one bit m, pick a random residue x, square it, and send y, together "
                     "with m XOR the LSB of x."):
            self.play(FadeIn(enc))
        pts = VGroup(tx(r"\textbf{Correct:} with $p, q$, Bob finds the \emph{unique} principal root $x$, then LSB$(x) \oplus z = m$.", 30),
                     tx(r"\textbf{Secure:} LSB$(x)$ looks like a fair coin to Eve, so it acts as a one-time pad on $m$.", 30)).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        pts.next_to(enc, RIGHT, buff=0.5)
        fit(pts, 6.2)
        with self.vo("It fixes both problems. Correctness: Bob, knowing p and q, finds the unique principal root, so he "
                     "knows the LSB and can XOR it off. Security: to Eve, that LSB is as good as a fair coin, so it's a one "
                     "time pad on the bit m. Part five makes this precise."):
            self.play(FadeIn(pts[0]))
            self.play(FadeIn(pts[1]))
        self.clear_all()
        r = recap_list([r"LSB of ``the'' root is meaningless: $x$ and $N - x$ have opposite parity.",
                        r"Principal root = the unique root in $QR_N$ (Blum $N$).",
                        r"Thm 4.3: LSB of the principal root can't be guessed better than $\tfrac12 + $ negl.",
                        r"Lemma 4.2: perfect LSB oracle $\Rightarrow$ read $x/N$ digit by digit $\Rightarrow$ root.",
                        r"Flip a predictor to turn ``far below $\tfrac12$'' into ``far above''.",
                        r"Re-randomize: $y^* a^2$ is uniform; divide the answer by $a$."], fs=30)
        fit(r, 12.8).move_to(DOWN * 0.1)
        with self.vo("Recap. The LSB of the square root is meaningless until we pick the principal root, the one that's a "
                     "residue. Theorem four point three says its LSB is hidden. Lemma four point two shows a perfect LSB "
                     "oracle reveals the whole root, digit by digit. Bad predictors can be flipped. And re randomizing "
                     "turns a fixed instance into a random one.") as d:
            for line in r:
                self.play(FadeIn(line, shift=0.2 * RIGHT), run_time=0.6)
                self.wait(d / 9)
        nxt = tx(r"Next: Part 5 --- public-key encryption, IND security, and Rabin's scheme", 30, HL).to_edge(DOWN, buff=0.4)
        with self.vo("Next, part five: public key encryption and its security definition."):
            self.play(FadeIn(nxt))
        self.wait(1)
