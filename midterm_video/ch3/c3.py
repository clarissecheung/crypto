from cx import *

QR7 = {1, 2, 4}
QR11 = {1, 3, 4, 5, 9}


class Intro3(VScene):
    def construct(self):
        title = tx(r"\textbf{Part 3: Algorithmic Number Theory}", 50, HL).move_to(UP * 0.4)
        sub = tx(r"Weeks 3--4 \quad (notes chapter 3)", 30, GREY_A).next_to(title, DOWN)
        with self.vo("Part three: algorithmic number theory."):
            self.play(Write(title), FadeIn(sub))
        self.play(FadeOut(title), FadeOut(sub))
        self.header("Part 3", "the destination")
        goal = VGroup(tx(r"\textbf{Theorem 3.3:} \ if factoring is hard, then computing", 36),
                      tx(r"square roots modulo $N = pq$ is hard.", 36)).arrange(DOWN, buff=0.15).move_to(UP * 1.7)
        with self.vo("Everything in this part builds to one theorem: if factoring is hard, then taking square roots "
                     "modulo N is hard too. That's the hard problem our encryption will be built on."):
            self.play(FadeIn(goal))
        steps = roadmap([("Mod arithmetic", r"$+, \times$, weirdness"), ("Mod a prime", r"Fermat, inverses"),
                         ("CRT", r"$\mathbb Z_N \leftrightarrow \mathbb Z_p \times \mathbb Z_q$"),
                         ("Squares mod $p$", r"Euler's criterion"), ("Squares mod $N$", r"four roots"),
                         ("Reduction", r"roots $\Rightarrow$ factors")], cols=3, w=3.9, h=1.2).move_to(DOWN * 1.0)
        with self.vo("The route: arithmetic mod m, then mod a prime, the Chinese remainder theorem, squares mod a prime, "
                     "squares mod N, and finally the reduction."):
            self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in steps], lag_ratio=0.15), run_time=2.5)
        self.clear_all()


class Mod3(VScene):
    def construct(self):
        self.header("Modular arithmetic", r"$\mathbb Z_m = \{0, 1, \dots, m-1\}$")
        d = VGroup(M(r"a \equiv b \pmod m \iff m \mid (a - b) \iff [a \bmod m] = [b \bmod m]", font_size=38),
                   tx(r"\textbf{Prop.\ 3.1:} \ if $a \equiv c$ and $b \equiv d$, then $a + b \equiv c + d$ and $ab \equiv cd$", 32, HL)).arrange(DOWN, buff=0.4)
        d.to_edge(UP, buff=1.2)
        with self.vo("a is congruent to b mod m when m divides their difference, or equivalently, they leave the same "
                     "remainder. Proposition three point one says you can replace numbers by congruent ones inside sums "
                     "and products. That's what lets us reduce as we go."):
            self.play(Write(d[0]), run_time=2)
            self.play(FadeIn(d[1]))
        pf = VGroup(tx(r"\textbf{Ex.\ 3.1 proof (product):} \ write $a = c + ms$, \ $b = d + mt$. Then", 30),
                    M(r"ab = cd + m(ct + sd + mst) \;\Rightarrow\; m \mid (ab - cd) \;\Rightarrow\; ab \equiv cd", font_size=36)).arrange(DOWN, buff=0.25)
        pf.next_to(d, DOWN, buff=0.5)
        with self.vo("Proof for products: a is c plus a multiple of m, b is d plus a multiple of m. Multiply out: you "
                     "get c d plus m times something. So m divides a b minus c d. Sums work the same way."):
            self.play(FadeIn(pf[0]))
            self.play(Write(pf[1]), run_time=2)
        weird = VGroup(tx(r"But mod a composite, strange things happen:", 32, BAD),
                       M(r"6 \cdot 10 = 60 \equiv 0 \pmod{15} \qquad 3 \cdot 5 \equiv 3 \cdot 10 \pmod{15}", font_size=38)).arrange(DOWN, buff=0.25)
        weird.to_edge(DOWN, buff=0.5)
        with self.vo("But watch out. Mod fifteen, six times ten is zero, even though neither is zero. And three times "
                     "five equals three times ten, but you can't cancel the three. We'll see exactly why, using the "
                     "Chinese remainder theorem."):
            self.play(FadeIn(weird))
        self.clear_all()


class Fermat3(VScene):
    def construct(self):
        self.header("Mod a prime $p$", r"$\mathbb Z_p^* = \{1, \dots, p-1\}$")
        props = rows(r"\textbf{Zero product:} \ $ab \equiv 0 \pmod p \Rightarrow a \equiv 0$ or $b \equiv 0$ \ (Euclid's lemma)",
                     r"\textbf{Cancellation:} \ $a \not\equiv 0$ and $ab \equiv ac \Rightarrow b \equiv c$",
                     fs=32, buff=0.3).to_edge(UP, buff=1.15)
        with self.vo("Modulo a prime, multiplication behaves. If a product is zero mod p, one factor is zero, because a "
                     "prime dividing a product divides one of the factors. And you can cancel any nonzero factor."):
            self.play(FadeIn(props[0]))
            self.play(FadeIn(props[1]))
        th = tx(r"\textbf{Fermat's little theorem:} \ $a \in \mathbb Z_p^* \Rightarrow a^{p-1} \equiv 1 \pmod p$", 36, HL).next_to(props, DOWN, buff=0.5)
        with self.vo("Fermat's little theorem: for any nonzero a mod a prime p, a to the p minus one is one."):
            self.play(Write(th))
        base = VGroup(*[M(str(x), font_size=38) for x in range(1, 7)]).arrange(RIGHT, buff=0.55).move_to(LEFT * 2.8 + DOWN * 0.5)
        times = VGroup(*[M(str(3 * x % 7), font_size=38, color=HL) for x in range(1, 7)]).arrange(RIGHT, buff=0.55).next_to(base, DOWN, buff=0.6)
        lb = tx(r"$x$", 30).next_to(base, LEFT, buff=0.4)
        lt = tx(r"$3x \bmod 7$", 30, HL).next_to(times, LEFT, buff=0.4)
        with self.vo("Why? Take p equals seven and a equals three. Multiply each of one through six by three, mod seven. "
                     "You get three, six, two, five, one, four: the same six numbers, shuffled. Cancellation guarantees "
                     "no two collide, and zero never appears.") as d:
            self.play(FadeIn(base), FadeIn(lb))
            self.play(LaggedStart(*[TransformFromCopy(b, t) for b, t in zip(base, times)], lag_ratio=0.15), FadeIn(lt))
        pf = VGroup(M(r"(3\cdot1)(3\cdot2)\cdots(3\cdot6) \equiv 1\cdot2\cdots6", font_size=32),
                    M(r"3^6 \cdot 6! \equiv 6! \;\Rightarrow\; 3^6 \equiv 1", font_size=32, color=HL)).arrange(DOWN, buff=0.25)
        pf.move_to(RIGHT * 3.7 + DOWN * 1.0)
        with self.vo("Multiply everything in each row. The products are equal because it's the same set. The left one "
                     "is three to the sixth times six factorial. Cancel the six factorial, and three to the sixth is one."):
            self.play(Write(pf[0]))
            self.play(Write(pf[1]))
        self.clear_all()
        inv = VGroup(tx(r"\textbf{Inverses:} \ $a \cdot a^{p-2} = a^{p-1} \equiv 1$, \ so \ $a^{-1} \equiv a^{p-2} \pmod p$", 34, HL),
                     M(r"\text{e.g. } 3^{-1} \equiv 3^{5} = 243 \equiv 5 \pmod 7, \qquad 3 \cdot 5 = 15 \equiv 1 \;\checkmark", font_size=36),
                     tx(r"computed fast with repeated squaring $\Rightarrow$ inverses mod $p$ are PPT", 30, GOOD)).arrange(DOWN, buff=0.4)
        with self.vo("A corollary: a times a to the p minus two is a to the p minus one, which is one. So a to the p "
                     "minus two is the inverse of a. For example, the inverse of three mod seven is three to the fifth, "
                     "which is five. And repeated squaring computes it efficiently.") as d:
            for x in inv:
                self.play(FadeIn(x, shift=0.2 * UP))
                self.wait(d / 7)
        self.clear_all()


class CRT3(VScene):
    def construct(self):
        self.header("Chinese Remainder Theorem", r"$N = pq$")
        p, q = 5, 7
        cells = VGroup()
        hdr = VGroup(*[M(str(b), font_size=28, color=C2) for b in range(q)])
        side = VGroup(*[M(str(a), font_size=28, color=C1) for a in range(p)])
        grid = {}
        for a in range(p):
            for b in range(q):
                c = next(c for c in range(p * q) if c % p == a and c % q == b)
                t = M(str(c), font_size=28)
                grid[(a, b)] = t
                cells.add(t)
        cells.arrange_in_grid(rows=p, cols=q, buff=(0.42, 0.22))
        cells.move_to(LEFT * 2.6 + DOWN * 0.4)
        for b in range(q):
            hdr[b].next_to(grid[(0, b)], UP, buff=0.35)
        for a in range(p):
            side[a].next_to(grid[(a, 0)], LEFT, buff=0.45)
        lh = tx(r"$c \bmod 7$", 26, C2).next_to(hdr, UP, buff=0.15)
        ls = tx(r"$c \bmod 5$", 26, C1).next_to(side, LEFT, buff=0.15).rotate(PI / 2)
        with self.vo("The Chinese remainder theorem. Lay out the numbers zero to thirty four in a table: the row is the "
                     "remainder mod five, the column is the remainder mod seven. Every cell gets exactly one number, and "
                     "every number lands in exactly one cell."):
            self.play(FadeIn(hdr), FadeIn(side), FadeIn(lh), FadeIn(ls))
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.02), run_time=2.5)
        b17, b29, b11 = (boxed(grid[(2, 3)], C1, 0.08), boxed(grid[(4, 1)], C2, 0.08), boxed(grid[(1, 4)], HL, 0.08))
        ex = VGroup(M(r"17 \leftrightarrow (2, 3)", font_size=34, color=C1), M(r"29 \leftrightarrow (4, 1)", font_size=34, color=C2),
                    M(r"17 + 29 \leftrightarrow (2{+}4,\ 3{+}1) = (1, 4)", font_size=34),
                    M(r"\leftrightarrow 11 = [46 \bmod 35] \;\checkmark", font_size=34, color=HL)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        ex.move_to(RIGHT * 3.9 + DOWN * 0.2)
        with self.vo("So each number mod thirty five is really a pair: its remainder mod five and mod seven. Seventeen is "
                     "the pair two, three. Twenty nine is four, one. Add them coordinate by coordinate, mod five and mod "
                     "seven separately: one, four. Look up that cell: eleven. And indeed forty six mod thirty five is "
                     "eleven. Multiplication works coordinatewise too.") as d:
            self.play(Create(b17), FadeIn(ex[0]))
            self.play(Create(b29), FadeIn(ex[1]))
            self.play(FadeIn(ex[2]))
            self.play(Create(b11), FadeIn(ex[3]))
        self.clear_all()
        th = VGroup(tx(r"\textbf{Theorem 3.2 (CRT).} For $a \in \mathbb Z_p,\ b \in \mathbb Z_q$ there is a unique $c \in \mathbb Z_N$ with", 32),
                    M(r"c \equiv a \pmod p, \qquad c \equiv b \pmod q \qquad\text{written } c = \mathrm{crt}(a, b)", font_size=36, color=HL),
                    tx(r"Formula: \ $r = p^{-1} \bmod q$, \ $s = q^{-1} \bmod p$, \quad $c = [\,r p\, b + s q\, a \bmod N\,]$", 32),
                    tx(r"mod $p$: the $rpb$ term vanishes and $sq \equiv 1$, leaving $a$. \ Mod $q$: symmetric.", 28, GREY_A)).arrange(DOWN, buff=0.3)
        th.to_edge(UP, buff=1.15)
        fit(th, 12.9)
        with self.vo("The theorem: for any pair a, b there's exactly one c below N with those remainders, called c r t of "
                     "a b. Here's a formula. Let r be the inverse of p mod q, and s the inverse of q mod p. Then c is r p b "
                     "plus s q a, mod N. Why? Mod p, the first term has a factor p so it vanishes, and s q is one, so "
                     "you're left with a. Mod q it's the mirror image.") as d:
            for x in th:
                self.play(FadeIn(x, shift=0.2 * UP))
                self.wait(d / 8)
        q3 = tx(r"\textbf{Ex.\ 3.3} \ $p = 5$, $q = 13$, $N = 65$: \ find $5^{-1} \bmod 13$, \ $13^{-1} \bmod 5$, \ crt$(2, 6)$", 30, HL)
        q3.next_to(th, DOWN, buff=0.4)
        s3 = VGroup(M(r"5 \cdot 8 = 40 = 3\cdot 13 + 1 \Rightarrow 5^{-1} \equiv 8 \pmod{13}", font_size=32),
                    M(r"13 \equiv 3,\ 3 \cdot 2 = 6 \equiv 1 \Rightarrow 13^{-1} \equiv 2 \pmod 5", font_size=32),
                    M(r"\mathrm{crt}(2,6) = [\,8\cdot5\cdot6 + 2\cdot13\cdot2 \bmod 65\,] = [292 \bmod 65] = 32", font_size=32, color=HL)).arrange(DOWN, buff=0.22)
        s3.next_to(q3, DOWN, buff=0.3)
        fit(s3, 12.9)
        with self.vo("Exercise three point three. Five times eight is forty, one more than thirty nine, so the inverse of "
                     "five mod thirteen is eight. Thirteen is three mod five, and three times two is six, which is one, so "
                     "the inverse of thirteen mod five is two. Plug into the formula with a equals two and b equals six: "
                     "two hundred ninety two, which is thirty two mod sixty five.") as d:
            self.play(FadeIn(q3))
            for x in s3:
                self.play(Write(x))
                self.wait(d / 10)
        chk = tx(r"check: $32 = 6\cdot5 + 2$ \checkmark \quad $32 = 2\cdot13 + 6$ \checkmark", 30, GOOD).to_edge(DOWN, buff=0.3)
        with self.vo("Always check: thirty two leaves remainder two mod five, and six mod thirteen. Correct."):
            self.play(FadeIn(chk))
            self.play(Create(boxed(s3[2])))
        self.clear_all()


class ZN3(VScene):
    def construct(self):
        self.header(r"Units mod $N$", r"$\mathbb Z_N^*$")
        why = VGroup(tx(r"Back to $N = 15 = 3 \cdot 5$: \ $6 = \mathrm{crt}(0, 1)$, \ $10 = \mathrm{crt}(1, 0)$", 32),
                     M(r"6 \cdot 10 \leftrightarrow (0\cdot 1,\ 1 \cdot 0) = (0, 0) \leftrightarrow 0", font_size=38),
                     tx(r"each factor is $0$ in \emph{one} coordinate $\Rightarrow$ product is $0$ in both", 30, GREY_A)).arrange(DOWN, buff=0.3)
        why.to_edge(UP, buff=1.15)
        with self.vo("Now the weirdness makes sense. Mod fifteen, six is zero mod three, and ten is zero mod five. In "
                     "coordinates, each has a zero somewhere, so the product is zero in both coordinates, which is zero."):
            for x in why:
                self.play(FadeIn(x, shift=0.2 * UP))
        d = VGroup(tx(r"$\mathbb Z_N^* = $ elements with an inverse mod $N$ $= \{\mathrm{crt}(a,b) : a \ne 0,\ b \ne 0\} = \{x : \gcd(x, N) = 1\}$", 30, HL),
                   M(r"|\mathbb Z_N^*| = (p-1)(q-1), \qquad \mathrm{crt}(a,b)^{-1} = \mathrm{crt}(a^{-1}, b^{-1})", font_size=36),
                   tx(r"Inverses mod $N$ are PPT even \emph{without} knowing $p, q$ (extended Euclid; Prop.\ 3.6).", 30, GOOD)).arrange(DOWN, buff=0.35)
        d.next_to(why, DOWN, buff=0.55)
        fit(d, 12.9)
        with self.vo("The invertible elements mod N, written Z N star, are exactly the pairs with both coordinates "
                     "nonzero. Equivalently, numbers sharing no factor with N. There are p minus one times q minus one "
                     "of them, and you invert coordinatewise. Inverses mod N can also be computed efficiently without "
                     "knowing p and q.") as dd:
            for x in d:
                self.play(FadeIn(x, shift=0.2 * UP))
                self.wait(dd / 7)
        self.clear_all()


class QRp3(VScene):
    def construct(self):
        self.header(r"Squares mod $p$", "quadratic residues")
        d = tx(r"$y \in \mathbb Z_m^*$ is a \textbf{quadratic residue} ($y \in QR_m$) if $x^2 \equiv y$ for some $x \in \mathbb Z_m^*$", 34, HL)
        d.to_edge(UP, buff=1.15)
        with self.vo("A quadratic residue mod m is an invertible number that is a perfect square mod m. The number x "
                     "with x squared equal to y is a square root of y."):
            self.play(FadeIn(d))
        xs = VGroup(*[M(str(x), font_size=34) for x in range(1, 11)]).arrange(RIGHT, buff=0.45).move_to(UP * 1.1)
        ys = VGroup(*[M(str(x * x % 11), font_size=34, color=HL) for x in range(1, 11)]).arrange(RIGHT, buff=0.45).next_to(xs, DOWN, buff=0.55)
        for a, b in zip(xs, ys):
            b.set_x(a.get_x())
        lx = tx(r"$x$", 30).next_to(xs, LEFT, buff=0.4)
        ly = tx(r"$x^2 \bmod 11$", 30, HL).next_to(ys, LEFT, buff=0.4)
        with self.vo("Square everything mod eleven. One through five give one, four, nine, five, three. Six through ten "
                     "give the same values in reverse, because ten is minus one, nine is minus two, and so on, and minus x "
                     "squared equals x squared.") as dd:
            self.play(FadeIn(xs), FadeIn(lx))
            self.play(LaggedStart(*[TransformFromCopy(a, b) for a, b in zip(xs, ys)], lag_ratio=0.1), FadeIn(ly))
        res = VGroup(M(r"QR_{11} = \{1, 3, 4, 5, 9\}", font_size=38, color=HL),
                     tx(r"each QR has exactly two roots $\pm x$ \ $\Rightarrow$ \ $|QR_p| = \tfrac{p-1}{2}$", 32)).arrange(DOWN, buff=0.3)
        res.next_to(ys, DOWN, buff=0.5)
        with self.vo("So the quadratic residues mod eleven are one, three, four, five and nine: exactly half. Mod an odd "
                     "prime, every residue has exactly two roots, x and minus x, so exactly half the nonzero numbers are "
                     "squares."):
            self.play(Write(res[0]))
            self.play(FadeIn(res[1]))
        self.clear_all()
        eu = VGroup(tx(r"\textbf{Euler's criterion} \ ($p$ odd prime, $y \in \mathbb Z_p^*$):", 36, HL),
                    M(r"y \in QR_p \iff y^{(p-1)/2} \equiv 1 \pmod p \qquad (\text{otherwise } y^{(p-1)/2} \equiv -1)", font_size=36),
                    tx(r"easy direction: $y = x^2 \Rightarrow y^{(p-1)/2} = x^{p-1} \equiv 1$ by Fermat", 30, GREY_A)).arrange(DOWN, buff=0.35)
        eu.to_edge(UP, buff=1.15)
        with self.vo("The single most useful fact for exam proofs: Euler's criterion. y is a quadratic residue exactly "
                     "when y to the p minus one over two is one. Otherwise it's minus one. One direction is easy: if y is "
                     "x squared, then y to the p minus one over two is x to the p minus one, which is one by Fermat.") as d:
            self.play(FadeIn(eu[0]))
            self.play(Write(eu[1]), run_time=2)
            self.play(FadeIn(eu[2]))
            self.play(Create(boxed(eu[1])))
        rt = VGroup(tx(r"\textbf{Square roots when $p \equiv 3 \pmod 4$:} \quad $x = \pm\, y^{(p+1)/4} \bmod p$", 34, HL),
                    M(r"x^2 = y^{(p+1)/2} = y^{(p-1)/2} \cdot y \equiv 1 \cdot y = y", font_size=36),
                    tx(r"($p \equiv 3 \bmod 4$ makes $(p+1)/4$ an integer)", 28, GREY_A)).arrange(DOWN, buff=0.3)
        rt.next_to(eu, DOWN, buff=0.55)
        with self.vo("And when p is three mod four, square roots have a formula: y to the p plus one over four. Check: "
                     "squaring gives y to the p plus one over two, which is y to the p minus one over two, times y. The "
                     "first factor is one by Euler, so we get y. Three mod four is exactly what makes the exponent a "
                     "whole number."):
            self.play(FadeIn(rt[0]))
            self.play(Write(rt[1]))
            self.play(FadeIn(rt[2]))
        self.clear_all()
        ex = VGroup(tx(r"\textbf{Example:} $p = 11$, $y = 5$", 34, HL),
                    M(r"5^{5} \equiv 1 \pmod{11} \Rightarrow 5 \in QR_{11}", font_size=36),
                    M(r"x = 5^{(11+1)/4} = 5^3 = 125 \equiv 4, \qquad 4^2 = 16 \equiv 5\ \checkmark", font_size=36),
                    M(r"\text{roots: } 4 \text{ and } -4 \equiv 7", font_size=36, color=HL)).arrange(DOWN, buff=0.35)
        with self.vo("Example: p is eleven, y is five. Five to the fifth is one mod eleven, so five is a residue. Its root "
                     "is five cubed, a hundred twenty five, which is four mod eleven. Check: sixteen is five. The two "
                     "roots are four and seven.") as d:
            for x in ex:
                self.play(FadeIn(x, shift=0.2 * UP))
                self.wait(d / 8)
        self.clear_all()


class Ex34(VScene):
    def construct(self):
        self.header("Exam-style", r"Ex.\ 3.4: $QR_{17}$")
        q = tx(r"List the quadratic residues and non-residues modulo 17.", 34).to_edge(UP, buff=1.15)
        with self.vo("Exercise three point four: list the residues and non residues mod seventeen."):
            self.play(FadeIn(q))
        xs = VGroup(*[M(str(x), font_size=36) for x in range(1, 9)]).arrange(RIGHT, buff=0.7).move_to(UP * 1.0)
        sq = [x * x for x in range(1, 9)]
        ys = VGroup(*[M(f"{s}" + (rf"\to{s % 17}" if s >= 17 else ""), font_size=30, color=HL) for s in sq])
        for a, b in zip(xs, ys):
            b.next_to(a, DOWN, buff=0.45)
        with self.vo("Only square one through eight. Nine through sixteen are the negatives of these, and give the same "
                     "squares. One, four, nine, sixteen, then twenty five is eight, thirty six is two, forty nine is "
                     "fifteen, sixty four is thirteen.") as d:
            self.play(FadeIn(xs))
            self.play(LaggedStart(*[FadeIn(y, shift=0.2 * DOWN) for y in ys], lag_ratio=0.25), run_time=d * 0.7)
        ans = VGroup(M(r"QR_{17} = \{1, 2, 4, 8, 9, 13, 15, 16\}", font_size=40, color=GOOD),
                     M(r"\text{non-residues} = \{3, 5, 6, 7, 10, 11, 12, 14\}", font_size=40, color=BAD)).arrange(DOWN, buff=0.35)
        ans.next_to(ys, DOWN, buff=0.7)
        with self.vo("Sort them: one, two, four, eight, nine, thirteen, fifteen, sixteen are the residues. The other eight "
                     "are non residues. Eight and eight, half each, as promised."):
            self.play(Write(ans[0]))
            self.play(Write(ans[1]))
        self.clear_all()


class QRN3(VScene):
    def construct(self):
        self.header(r"Squares mod $N = pq$", "via CRT")
        c = VGroup(tx(r"\textbf{Claim 3.1:} \ $y = \mathrm{crt}(a, b) \in QR_N \iff a \in QR_p$ \ and \ $b \in QR_q$", 34, HL),
                   tx(r"\textbf{Prop.\ 3.13:} if $\pm u$ are the roots mod $p$ and $\pm v$ the roots mod $q$,", 32),
                   tx(r"then $y$ has exactly \textbf{four} roots: \ $\mathrm{crt}(u, v),\ \mathrm{crt}(u,-v),\ \mathrm{crt}(-u,v),\ \mathrm{crt}(-u,-v)$", 32),
                   M(r"|QR_N| = \tfrac14 |\mathbb Z_N^*| = \tfrac{(p-1)(q-1)}{4}", font_size=36)).arrange(DOWN, buff=0.3)
        c.to_edge(UP, buff=1.15)
        fit(c, 12.9)
        with self.vo("Mod N, use coordinates. y is a square mod N exactly when it's a square in both coordinates. And "
                     "since each coordinate has two roots, plus or minus, y has four roots: every combination of signs. "
                     "So a quarter of the units are squares.") as d:
            for x in c:
                self.play(FadeIn(x, shift=0.2 * UP))
                self.wait(d / 8)
        alg = algo(r"Roots of $y$ mod $N$ \emph{given} $p, q \equiv 3 \bmod 4$",
                   [r"check $y^{(p-1)/2} \equiv 1 \pmod p$ and $y^{(q-1)/2} \equiv 1 \pmod q$",
                    r"$u := y^{(p+1)/4} \bmod p$, \quad $v := y^{(q+1)/4} \bmod q$",
                    r"return $\mathrm{crt}(\pm u, \pm v)$"], fs=28).next_to(c, DOWN, buff=0.4)
        with self.vo("With the factors in hand, it's all efficient: check Euler's criterion mod each prime, take each "
                     "coordinate's root with the formula, and combine with C R T. Remember this: knowing p and q makes "
                     "square roots easy."):
            self.play(FadeIn(alg))
        self.clear_all()
        ex = tx(r"\textbf{Example 3.6:} \ $N = 77 = 7 \cdot 11$, \ $y = 9$", 34, HL).to_edge(UP, buff=1.15)
        st = VGroup(M(r"\bmod 7:\ y \equiv 2,\ \ 2^3 \equiv 1 \checkmark,\ \ u = 2^{2} = 4 \Rightarrow \pm u = \{4, 3\}", font_size=34),
                    M(r"\bmod 11:\ y \equiv 9,\ \ 9^5 \equiv 1 \checkmark,\ \ v = 9^{3} \equiv 3 \Rightarrow \pm v = \{3, 8\}", font_size=34)).arrange(DOWN, buff=0.3)
        st.next_to(ex, DOWN, buff=0.4)
        with self.vo("Example. N is seventy seven, y is nine. Mod seven, y is two. Euler: two cubed is one, so it's a "
                     "residue, and its roots are four and three. Mod eleven, y is nine, a residue, with roots three and "
                     "eight."):
            self.play(FadeIn(ex))
            self.play(Write(st[0]))
            self.play(Write(st[1]))
        tbl = VGroup(*[M(s, font_size=34) for s in [r"u \bmod 7", r"v \bmod 11", r"\mathrm{crt}(u,v)",
                                                     "3", "3", "3", "3", "8", "52", "4", "3", "25", "4", "8", "74"]])
        tbl.arrange_in_grid(rows=5, cols=3, buff=(0.9, 0.22)).next_to(st, DOWN, buff=0.45)
        with self.vo("Combine every pair with C R T. The four square roots of nine mod seventy seven are three, fifty "
                     "two, twenty five and seventy four."):
            self.play(FadeIn(tbl))
            self.play(Indicate(VGroup(tbl[5], tbl[8], tbl[11], tbl[14]), color=HL))
        self.clear_all()


class Ex38(VScene):
    def construct(self):
        self.header("Exam-style", r"Ex.\ 3.8 = Quiz 4")
        q = tx(r"$p, q \equiv 3 \pmod 4$ distinct primes, $N = pq$.", 34, HL).to_edge(UP, buff=1.1)
        a = VGroup(tx(r"\textbf{(a)} \ $-1 \notin QR_p$.", 32),
                   tx(r"Write $p = 4i + 3$, so $\tfrac{p-1}{2} = 2i + 1$ is \textbf{odd}. \ Euler: \ $(-1)^{(p-1)/2} = (-1)^{\text{odd}} = -1 \not\equiv 1$.", 30),
                   tx(r"So $-1$ fails Euler's criterion: \ $-1 \notin QR_p$. \ $\blacksquare$", 30, GOOD)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        b = VGroup(tx(r"\textbf{(b)} \ $y \in QR_p \Rightarrow -y \notin QR_p$.", 32),
                   M(r"(-y)^{\frac{p-1}{2}} = (-1)^{\frac{p-1}{2}} \cdot y^{\frac{p-1}{2}} \equiv (-1)\cdot(1) = -1 \not\equiv 1", font_size=34),
                   tx(r"using (a) for the first factor and Euler for $y \in QR_p$. \ So $-y \notin QR_p$. \ $\blacksquare$", 30, GOOD)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        g = VGroup(a, b).arrange(DOWN, buff=0.5, aligned_edge=LEFT).next_to(q, DOWN, buff=0.4)
        fit(g, 12.9)
        with self.vo("Exercise three point eight was all of quiz four. Primes p and q, both three mod four. Part a: minus "
                     "one is not a residue mod p. Use Euler's criterion. p is four i plus three, so p minus one over two "
                     "is two i plus one, an odd number. Minus one to an odd power is minus one, not one. So minus one "
                     "fails the criterion.") as d:
            self.play(FadeIn(q))
            for x in a:
                self.play(FadeIn(x, shift=0.15 * RIGHT))
                self.wait(d / 9)
        with self.vo("Part b: if y is a residue, minus y isn't. Raise minus y to the p minus one over two. It splits into "
                     "minus one to that power, which is minus one by part a, times y to that power, which is one by "
                     "Euler since y is a residue. The product is minus one, so minus y is not a residue.") as d:
            for x in b:
                self.play(FadeIn(x, shift=0.15 * RIGHT))
                self.wait(d / 8)
        self.clear_all()
        c = tx(r"\textbf{(c)} \ every $y \in QR_N$ has \textbf{exactly one} square root that is itself in $QR_N$.", 32, HL).to_edge(UP, buff=1.1)
        with self.vo("Part c, the big one: every residue mod N has exactly one square root that is itself a residue. On "
                     "the quiz, the answer claimed there's only one root to begin with. That's only true mod a prime. "
                     "Mod N there are four roots. Let's see which one is special, with N equals seventy seven, both "
                     "primes three mod four."):
            self.play(FadeIn(c))
        y = 23
        roots = [10, 32, 45, 67]
        hdr = VGroup(*[tx(s, 28, GREY_A) for s in ["root $x$", r"$x \bmod 7$", r"in $QR_7$?", r"$x \bmod 11$", r"in $QR_{11}$?", r"in $QR_{77}$?"]])
        rowsv = []
        for r in roots:
            a7, a11 = r % 7, r % 11
            ok7, ok11 = a7 in QR7, a11 in QR11
            rowsv.append([M(str(r), font_size=32), M(str(a7), font_size=32), tx(r"\checkmark" if ok7 else r"$\times$", 30, GOOD if ok7 else BAD),
                          M(str(a11), font_size=32), tx(r"\checkmark" if ok11 else r"$\times$", 30, GOOD if ok11 else BAD),
                          tx(r"\textbf{yes}" if ok7 and ok11 else "no", 30, HL if ok7 and ok11 else GREY_B)])
        tb = VGroup(*hdr, *[x for r in rowsv for x in r]).arrange_in_grid(rows=5, cols=6, buff=(0.55, 0.25))
        tb.next_to(c, DOWN, buff=0.45)
        lab = tx(r"$y = 23$; \ $QR_7 = \{1,2,4\}$, \ $QR_{11} = \{1,3,4,5,9\}$", 28, GREY_A).next_to(tb, DOWN, buff=0.3)
        with self.vo("Take y equals twenty three. Its four roots are ten, thirty two, forty five and sixty seven. Reduce "
                     "each mod seven: three, four, three, four. That's plus or minus one value. Mod eleven: ten, ten, "
                     "one, one, again a plus minus pair.") as d:
            self.play(FadeIn(VGroup(*hdr)), FadeIn(lab))
            for r in rowsv:
                self.play(FadeIn(VGroup(r[0], r[1], r[3])), run_time=0.5)
        with self.vo("Now check residues. Mod seven, exactly one of three and four is a residue: four. Mod eleven, exactly "
                     "one of ten and one: one. That's part b at work. Only sixty seven has a residue in both coordinates, "
                     "so only sixty seven is in Q R seventy seven."):
            for r in rowsv:
                self.play(FadeIn(VGroup(r[2], r[4])), run_time=0.4)
            for r in rowsv:
                self.play(FadeIn(r[5]), run_time=0.3)
            self.play(Create(boxed(VGroup(*rowsv[3]))))
        self.clear_all()
        pf = VGroup(tx(r"\textbf{Proof of (c).} Let $y \in QR_N$. By Prop.\ 3.13 its roots are $\mathrm{crt}(\pm u, \pm v)$,", 30),
                    tx(r"where $\pm u$ are the roots of $[y \bmod p]$ and $\pm v$ the roots of $[y \bmod q]$.", 30),
                    tx(r"For any $x \in \mathbb Z_p^*$, $x^{(p-1)/2} \equiv \pm1$, and $(-x)^{(p-1)/2} = -x^{(p-1)/2}$ (by (a)).", 30),
                    tx(r"So by Euler, \textbf{exactly one} of $u, -u$ is in $QR_p$; \ likewise exactly one of $v, -v$ is in $QR_q$.", 30),
                    tx(r"By Claim 3.1, $\mathrm{crt}(s, t) \in QR_N \iff s \in QR_p$ and $t \in QR_q$.", 30),
                    tx(r"Exactly one sign choice makes both hold $\Rightarrow$ exactly one root lies in $QR_N$. \ $\blacksquare$", 30, GOOD)).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
        fit(pf, 12.9)
        with self.vo("Here's the general proof. The roots are c r t of plus or minus u, plus or minus v. For any x mod p, x "
                     "to the p minus one over two is plus or minus one, since its square is one. And flipping x's sign "
                     "flips that value, by part a. So exactly one of u and minus u passes Euler's test. Same for v. By "
                     "claim three point one, a root is a residue mod N exactly when both its coordinates are, and exactly "
                     "one sign choice achieves that.") as d:
            for x in pf:
                self.play(FadeIn(x, shift=0.15 * RIGHT))
                self.wait(d / 10)
        nm = tx(r"This special root is the \textbf{principal root} --- the key to Parts 4 and 5.", 30, HL).to_edge(DOWN, buff=0.4)
        with self.vo("This special root is called the principal root, and it's the hinge for parts four and five."):
            self.play(FadeIn(nm))
        self.clear_all()


class Ex36(VScene):
    def construct(self):
        self.header("Exam-style", r"Ex.\ 3.6: $N = 329 = 47 \cdot 7$")
        a = VGroup(tx(r"\textbf{(a)} $2 \in QR_{47}$? \ $2^{23} \equiv 1 \pmod{47}$ \checkmark \ \ roots $\pm 2^{12}$: \ $2^{12} \equiv 7$, so $\{7, 40\}$", 30),
                   tx(r"\textbf{(b)} $40 \in QR_{47}$? \ $40 \equiv -7$ and $40^2 \equiv 49 \equiv 2$, so 40 is a \emph{root} of 2.", 30),
                   M(r"40^{23} = (40^2)^{11}\cdot 40 \equiv 2^{11} \cdot 40 \equiv 27 \cdot 40 \equiv 46 \equiv -1 \Rightarrow 40 \notin QR_{47}", font_size=32),
                   tx(r"(Or: 7 is the principal root of 2, so by Ex.\ 3.8(b) $-7 = 40$ is not a residue.)", 28, GREY_A)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        a.to_edge(UP, buff=1.15)
        fit(a, 12.9)
        with self.vo("Exercise three point six uses p equals forty seven and q equals seven. Part a: is two a residue mod "
                     "forty seven? Two to the twenty third is one, so yes. Forty seven is three mod four, so its roots are "
                     "plus or minus two to the twelfth, which is seven, so the roots are seven and forty."):
            self.play(FadeIn(a[0]))
        with self.vo("Part b: is forty a residue? The hint shows forty squared is two, so forty is a square root of two, "
                     "but that doesn't make forty itself a square. Euler: forty to the twenty third is two to the eleventh "
                     "times forty, twenty seven times forty, which is minus one. Not a residue. Equivalently, seven is the "
                     "principal root of two, and forty is minus seven.") as d:
            self.play(FadeIn(a[1]))
            self.play(Write(a[2]))
            self.play(FadeIn(a[3]))
        c = VGroup(tx(r"\textbf{(c)} $2 \in QR_{329}$? \ mod 7: $2 \equiv 3^2$ \checkmark, mod 47 \checkmark \ $\Rightarrow$ yes.", 30),
                   M(r"\text{roots} = \mathrm{crt}(\pm 7, \pm 3):\ \ 101,\ 87,\ 242,\ 228 \qquad (\text{principal: } 242 = \mathrm{crt}(7, 4))", font_size=32, color=HL),
                   tx(r"\textbf{(d)} $40 \in QR_{329}$? \ No: $40 \notin QR_{47}$ (and $40 \equiv 5 \notin QR_7 = \{1,2,4\}$).", 30)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        c.next_to(a, DOWN, buff=0.4)
        fit(c, 12.9)
        with self.vo("Part c: two mod seven is three squared, and two is a residue mod forty seven, so two is a residue mod "
                     "three twenty nine. Its four roots combine plus or minus seven with plus or minus three: one oh one, "
                     "eighty seven, two forty two, and two twenty eight."):
            self.play(FadeIn(c[0]))
            self.play(Write(c[1]))
        with self.vo("Part d: forty is not a residue mod forty seven, so it can't be one mod three twenty nine. Both "
                     "coordinates must be residues."):
            self.play(FadeIn(c[2]))
        self.clear_all()


class Ex37(VScene):
    def construct(self):
        self.header("Exam-style", r"Ex.\ 3.5 and 3.7")
        e37 = VGroup(tx(r"\textbf{Ex.\ 3.7} \ Solve $x^2 \equiv 9 \pmod{21}$.", 34, HL),
                     tx(r"$x \equiv 0 \pmod 3$ \ and \ $x \equiv \pm 3 \pmod 7$ \ $\Rightarrow$ \ $x \in \{3, 18\}$: \ only \textbf{two} solutions", 30),
                     tx(r"No contradiction: $\gcd(9, 21) = 3$, so $9 \notin \mathbb Z_{21}^*$ --- it isn't a QR by definition.", 30, GOOD),
                     tx(r"Mod 3, $9 \equiv 0$ has the single root $0$ (no $\pm$ pair).", 28, GREY_A)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        e37.to_edge(UP, buff=1.15)
        fit(e37, 12.9)
        with self.vo("Exercise three point seven: solve x squared equals nine mod twenty one. In coordinates, mod three we "
                     "need x squared equal zero, so x is zero. Mod seven we need plus or minus three. That gives only two "
                     "solutions, three and eighteen, not four. Contradiction? No: nine shares a factor three with twenty "
                     "one, so it isn't invertible and isn't a quadratic residue by definition. Mod three, zero has just one "
                     "root.") as d:
            for x in e37:
                self.play(FadeIn(x, shift=0.15 * RIGHT))
                self.wait(d / 8)
        e35 = VGroup(tx(r"\textbf{Ex.\ 3.5} \ roots of $1$ mod $65 = 5 \cdot 13$: \ $\mathrm{crt}(\pm1, \pm1) = 1,\ 64,\ 14,\ 51$", 30, HL),
                     tx(r"All four are QRs! \ $-1 \equiv 4 = 2^2 \pmod 5$, \ $-1 \equiv 12 \equiv 5^2 \pmod{13}$", 30),
                     tx(r"Because $5 \equiv 13 \equiv 1 \pmod 4$, Ex.\ 3.8 doesn't apply. \ Blum integers ($\equiv 3 \bmod 4$) matter!", 30, GOOD)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        e35.next_to(e37, DOWN, buff=0.5)
        fit(e35, 12.9)
        with self.vo("Exercise three point five: the four square roots of one mod sixty five are c r t of plus or minus "
                     "one, plus or minus one: one, sixty four, fourteen and fifty one. Which are residues? All four! "
                     "Minus one is a square mod five and mod thirteen. That's because five and thirteen are one mod four, "
                     "so exercise three point eight doesn't apply. This is why we insist on Blum integers.") as d:
            for x in e35:
                self.play(FadeIn(x, shift=0.15 * RIGHT))
                self.wait(d / 7)
        self.clear_all()


class Reduct3(VScene):
    def construct(self):
        self.header("Proofs by reduction", "the core technique")
        bx = Rectangle(width=6.2, height=3.0, color=HON).move_to(DOWN * 0.3)
        bl = tx(r"$B$ \ (solves X)", 32, HON).next_to(bx, UP, buff=0.12).align_to(bx, LEFT)
        ax = Rectangle(width=2.2, height=1.4, color=ADV, fill_opacity=0.15).move_to(bx.get_center() + RIGHT * 1.4)
        al = tx(r"$A$ \ (solves Y)", 30, ADV).move_to(ax)
        inx = Arrow(LEFT * 6.3 + DOWN * 0.3, bx.get_left(), buff=0, color=WHITE)
        outx = Arrow(bx.get_right(), RIGHT * 6.3 + DOWN * 0.3, buff=0, color=WHITE)
        lin = tx(r"instance of X", 26).next_to(inx, UP, buff=0.1)
        lout = tx(r"answer for X", 26).next_to(outx, UP, buff=0.1)
        toA = Arrow(bx.get_center() + LEFT * 2.2, ax.get_left(), buff=0.05, color=GREY_B, stroke_width=3)
        frA = Arrow(ax.get_bottom(), bx.get_center() + LEFT * 2.2 + DOWN * 1.0, buff=0.05, color=GREY_B, stroke_width=3)
        with self.vo("A reduction from problem X to problem Y is an algorithm B for X that uses any algorithm A for Y as a "
                     "subroutine. B turns its X instance into Y instances, feeds them to A, and turns A's answers back into "
                     "an answer for X. B can't assume anything about how A works, only that it works.") as d:
            self.play(Create(bx), FadeIn(bl), GrowArrow(inx), FadeIn(lin))
            self.play(FadeIn(ax), FadeIn(al), GrowArrow(toA))
            self.play(GrowArrow(frA), GrowArrow(outx), FadeIn(lout))
        msg = tx(r"Efficient reduction: if Y is easy then X is easy. \ So \textbf{if X is hard, Y is hard.}", 32, HL).to_edge(DOWN, buff=0.4)
        with self.vo("If B is efficient whenever A is, then solving Y easily would solve X easily. Flip it around: if X is "
                     "hard, Y must be hard too. Hardness flows in the direction of the reduction."):
            self.play(FadeIn(msg))
        self.clear_all()
        tmpl = VGroup(tx(r"\textbf{Template for ``if Factoring, then Y is hard''}", 36, HL),
                      tx(r"1. \ Suppose for contradiction: a PPT $A$ solves Y with \textbf{non-negligible} probability.", 30),
                      tx(r"2. \ Build PPT $B$ for factoring that calls $A$. \ \emph{Feed $A$ inputs with exactly the right distribution.}", 30),
                      tx(r"3. \ Show $\mathrm{Adv}_B \ge \mathrm{Adv}_A / \mathrm{poly}(n)$, \ so $\mathrm{Adv}_B$ is non-negligible.", 30),
                      tx(r"4. \ That contradicts the factoring assumption. \ $\blacksquare$", 30)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        fit(tmpl, 12.9)
        with self.vo("Here's the template we'll use for every security proof in this course. Assume for contradiction "
                     "there's an efficient A that succeeds with non negligible probability. Build an efficient B for the "
                     "hard problem that calls A, making sure A sees inputs distributed exactly as it expects. Show B's "
                     "success is at least A's divided by a polynomial. That contradicts the assumption.") as d:
            for x in tmpl:
                self.play(FadeIn(x, shift=0.2 * RIGHT))
                self.wait(d / 9)
        self.clear_all()


class Thm33(VScene):
    def construct(self):
        self.header("Theorem 3.3", r"square roots $\Rightarrow$ factoring")
        alg = algo(r"$B(N)$: \ factor using a square-root finder $A$",
                   [r"1. \ $x \xleftarrow{\$} \mathbb Z_N^*$; \ $y := [x^2 \bmod N]$",
                    r"2. \ $\hat x \leftarrow A(N, y)$",
                    r"3. \ if $\hat x^2 \not\equiv y$: return $\perp$",
                    r"4. \ if $\hat x \equiv \pm x$: return $\perp$",
                    r"5. \ return $\gcd(x + \hat x, N)$"], fs=30).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        with self.vo("Now the main event. Suppose A computes square roots mod N. Here's B, which factors N. Pick a random "
                     "x, square it to get y, and ask A for a square root of y. If A fails, give up. If A returns x or "
                     "minus x, give up. Otherwise, output the g c d of x plus x hat with N.") as d:
            self.play(FadeIn(alg[0]), FadeIn(alg[1]))
            for ln in alg[2]:
                self.play(FadeIn(ln, shift=0.15 * RIGHT))
                self.wait(d / 10)
        ex = VGroup(tx(r"$N = 77$, \ $x = 10$, \ $y = 23$", 30, HL),
                    tx(r"roots of 23: \ $10,\ 32,\ 45,\ 67$", 30),
                    M(r"\hat x = 32: \ \gcd(42, 77) = 7", font_size=34, color=GOOD),
                    M(r"\hat x = 45: \ \gcd(55, 77) = 11", font_size=34, color=GOOD),
                    M(r"\hat x = 10 \text{ or } 67 = \pm x: \text{ useless}", font_size=34, color=BAD)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        ex.to_edge(RIGHT, buff=0.6).shift(DOWN * 0.3)
        with self.vo("Try it with N equals seventy seven. B picks x equals ten, so y is twenty three, which has four roots. "
                     "If A returns thirty two, the g c d of forty two and seventy seven is seven: a factor! If A returns "
                     "forty five, we get eleven. Only x itself or minus x are useless.") as d:
            for x in ex:
                self.play(FadeIn(x, shift=0.15 * LEFT))
                self.wait(d / 10)
        self.clear_all()
        an = VGroup(tx(r"\textbf{Why it works}", 36, HL),
                    tx(r"(i) \ $A$'s input is right: $y$ is a uniform QR, exactly as in the inversion problem $\Rightarrow$ $\Pr[\hat x^2 \equiv y] = \mathrm{Adv}^{inv}_A$.", 30),
                    tx(r"(ii) \ $A$ sees only $y$, and $x$ is uniform among $y$'s 4 roots. Whatever $A$ outputs, $\Pr[\hat x \equiv \pm x] = \tfrac12$.", 30),
                    tx(r"(iii) \ If $\hat x^2 \equiv x^2$ but $\hat x \not\equiv \pm x$, then $\gcd(x + \hat x, N) \in \{p, q\}$ \ (Ex.\ 3.9).", 30),
                    M(r"\Rightarrow\ \mathrm{Adv}^{factor}_B = \tfrac12\, \mathrm{Adv}^{inv}_A", font_size=40, color=GOOD),
                    tx(r"non-negligible $\Rightarrow$ non-negligible: contradicts Factoring. \ $\blacksquare$", 30)).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        fit(an, 12.9)
        with self.vo("Why it works, in three steps. One: A gets exactly the input distribution it expects, a uniformly "
                     "random residue, so it succeeds with its usual advantage. Two: A sees only y, and x is equally likely "
                     "to be any of y's four roots. So no matter what A does, it hits plus or minus x only half the time. "
                     "Three: two square roots that aren't plus or minus each other reveal a factor through the g c d.") as d:
            for x in an[:4]:
                self.play(FadeIn(x, shift=0.15 * RIGHT))
                self.wait(d / 8)
        with self.vo("So B factors with half of A's success probability. If A's success is non negligible, so is B's, "
                     "contradicting factoring. Square roots mod N are hard."):
            self.play(Write(an[4]))
            self.play(FadeIn(an[5]))
        self.clear_all()
        e39 = VGroup(tx(r"\textbf{Ex.\ 3.9} \ $x^2 \equiv z^2 \pmod N$, \ $x \not\equiv \pm z$ \ $\Rightarrow$ \ $\gcd(x+z, N) \in \{p, q\}$", 32, HL),
                     tx(r"$N \mid x^2 - z^2 = (x - z)(x + z)$, so $p$ divides one factor and $q$ divides one factor (Euclid).", 30),
                     tx(r"If $p, q$ both divide $x + z$: \ $N \mid x + z$, \ i.e.\ $x \equiv -z$. \ Contradiction.", 30),
                     tx(r"If neither divides $x + z$: \ both divide $x - z$, \ i.e.\ $x \equiv z$. \ Contradiction.", 30),
                     tx(r"So exactly one of $p, q$ divides $x + z$, and $\gcd(x + z, N)$ is that prime. \ $\blacksquare$", 30, GOOD)).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        fit(e39, 12.9)
        with self.vo("Exercise three point nine proves step three. N divides x squared minus z squared, which factors as x "
                     "minus z times x plus z. Each prime divides one of the two factors. If both primes divided x plus z, "
                     "then x would be minus z. If neither did, both would divide x minus z, so x would be z. Both are "
                     "ruled out, so exactly one prime divides x plus z, and the g c d is that prime.") as d:
            for x in e39:
                self.play(FadeIn(x, shift=0.15 * RIGHT))
                self.wait(d / 9)
        self.clear_all()


class Recap3(VScene):
    def construct(self):
        self.header("Part 3", "recap")
        r = recap_list([r"Mod $p$: cancel freely; Fermat $a^{p-1} \equiv 1$; inverse $a^{p-2}$.",
                        r"CRT: $x \bmod N$ $\leftrightarrow$ $(x \bmod p, x \bmod q)$; compute coordinatewise.",
                        r"Euler: $y \in QR_p \iff y^{(p-1)/2} \equiv 1$. \ Roots for $p\equiv 3$: $\pm y^{(p+1)/4}$.",
                        r"Mod $N$: four roots $\mathrm{crt}(\pm u, \pm v)$; Blum $\Rightarrow$ exactly one is a QR.",
                        r"Reduction template: assume $A$ succeeds, build $B$, match $A$'s input distribution.",
                        r"Two roots $\hat x \ne \pm x$ give a factor: $\gcd(x + \hat x, N)$."], fs=30)
        fit(r, 12.8).move_to(DOWN * 0.2)
        with self.vo("Recap. Mod a prime, you can cancel, Fermat holds, and inverses are powers. C R T turns arithmetic mod "
                     "N into arithmetic on pairs. Euler's criterion tests residues, and for primes three mod four, roots "
                     "have a formula. Mod N there are four roots, and for Blum integers exactly one is itself a residue. "
                     "Reductions build an attacker on the hard problem from an attacker on the new one. And two "
                     "essentially different square roots reveal a factor.") as d:
            for line in r:
                self.play(FadeIn(line, shift=0.2 * RIGHT), run_time=0.6)
                self.wait(d / 8)
        nxt = tx(r"Next: Part 4 --- what squaring hides: the least significant bit", 32, HL).to_edge(DOWN, buff=0.4)
        with self.vo("Next, part four: if square roots are hard, what exactly does squaring hide?"):
            self.play(FadeIn(nxt))
        self.wait(1)
