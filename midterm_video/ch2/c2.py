from cx import *


class Intro2(VScene):
    def construct(self):
        title = tx(r"\textbf{Part 2: Efficient Attackers, Negligible Chances}", 48, HL).move_to(UP * 0.4)
        sub = tx(r"Week 2 \quad (notes chapter 2: asymptotics and the factoring assumption)", 30, GREY_A).next_to(title, DOWN)
        with self.vo("Part two: efficient algorithms, negligible probabilities, and the factoring assumption."):
            self.play(Write(title), FadeIn(sub))
        self.play(FadeOut(title), FadeOut(sub))
        self.header("Part 2", "why change the goal?")
        why = VGroup(tx(r"Perfect secrecy forces $|\mathcal K| \ge |\mathcal M|$ \ (Shannon) --- impractical.", 34),
                     tx(r"New goal: \ \textbf{If problem X is hard, then scheme $\Pi$ is secure.}", 36, HL),
                     tx(r"secure against \emph{efficient} attackers, except with \emph{tiny} probability", 32, GREY_A)).arrange(DOWN, buff=0.45)
        with self.vo("Shannon showed perfect secrecy needs keys as long as the messages. That's impractical. So we "
                     "change the goal: if some problem X is hard, then our scheme is secure. Secure against attackers "
                     "who are efficient, except with tiny probability. That's computational security.") as d:
            for x in why:
                self.play(FadeIn(x, shift=0.2 * UP))
                self.wait(d / 6)
        self.clear_all()
        need = roadmap([("Efficient", r"PPT: poly time"), ("Tiny", r"negligible functions"),
                        ("Hard", r"the factoring assumption")], cols=3, w=4.0, h=1.3).move_to(UP * 1.4)
        with self.vo("To make that precise we need three definitions. What efficient means: probabilistic polynomial "
                     "time. What tiny means: negligible. And what hard means: the factoring assumption."):
            self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in need], lag_ratio=0.3), run_time=2)
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 100, 20], x_length=6.5, y_length=3.0,
                  axis_config={"include_numbers": False, "stroke_color": GREY_B}).to_edge(DOWN, buff=0.6)
        poly = ax.plot(lambda n: n ** 2, x_range=[0, 10], color=HON)
        expo = ax.plot(lambda n: 2 ** n, x_range=[0, 6.64], color=ADV)
        lp = tx(r"user's work $\approx n^2$", 26, HON).next_to(ax.c2p(10, 100), LEFT, buff=0.1).shift(DOWN * 0.3)
        le = tx(r"attacker's work $\approx 2^n$", 26, ADV).next_to(ax.c2p(6.6, 100), LEFT, buff=0.2)
        xl = tx(r"security parameter $n$ (e.g.\ key length)", 24, GREY_B).next_to(ax, DOWN, buff=0.1)
        with self.vo("The security parameter n is a dial. Turn it up, and honest users' work grows slowly, like a "
                     "polynomial, while the attacker's work, like trying every key, grows exponentially. That gap is "
                     "why we study how things grow as n goes to infinity."):
            self.play(Create(ax), FadeIn(xl))
            self.play(Create(poly), FadeIn(lp))
            self.play(Create(expo), FadeIn(le))
        self.clear_all()


class BigO2(VScene):
    def construct(self):
        self.header("Big O and poly", r"Def.\ 2.1, 2.2")
        d1 = VGroup(tx(r"$f(n) = O(g(n))$ \ means: \ there exist $C \ge 0$ and $n_0$ with", 34),
                    M(r"f(n) \le C \cdot g(n) \quad \text{for all } n \ge n_0", font_size=42, color=HL),
                    tx(r"``for all sufficiently large $n$'' $=$ ``there is an $n_0$ such that for all $n \ge n_0$''", 28, GREY_A)).arrange(DOWN, buff=0.3)
        d1.to_edge(UP, buff=1.2)
        with self.vo("Big O. f of n is big O of g of n if, past some starting point n zero, f is at most a constant "
                     "times g. The phrase for all sufficiently large n is shorthand for exactly that: there's some n "
                     "zero after which it holds."):
            self.play(FadeIn(d1[0]))
            self.play(Write(d1[1]))
            self.play(FadeIn(d1[2]))
        d2 = VGroup(tx(r"\textbf{Polynomially bounded:} \ $f(n) = O(n^c)$ for some constant $c$", 34, HL),
                    tx(r"poly: \ $7$, \ $n^3 + 2n$, \ $n \log n$, \ $\sqrt n$, \ $n^{100}$", 32, GOOD),
                    tx(r"not poly: \ $2^n$, \ $n!$, \ $2^{\sqrt n}$", 32, BAD)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        d2.next_to(d1, DOWN, buff=0.6)
        with self.vo("We say a function is polynomially bounded, poly for short, if it's big O of n to some fixed power. "
                     "Seven, n cubed plus two n, n log n, square root of n, even n to the hundred, are all poly. Two to "
                     "the n and n factorial are not: they eventually beat every power of n."):
            self.play(FadeIn(d2[0]))
            self.play(FadeIn(d2[1]))
            self.play(FadeIn(d2[2]))
        self.clear_all()


class PPT2(VScene):
    def construct(self):
        self.header("Efficient = PPT", r"Def.\ 2.3")
        d = VGroup(tx(r"\textbf{PPT} (probabilistic polynomial time): randomized $A$ whose", 34),
                   tx(r"\emph{worst-case} running time on inputs of \textbf{length} $n$ is poly$(n)$", 34, HL)).arrange(DOWN, buff=0.2)
        d.to_edge(UP, buff=1.2)
        with self.vo("An algorithm is efficient, P P T, if it's allowed randomness, and its worst case running time on "
                     "inputs of length n is polynomial in n. The word length is everything."):
            self.play(FadeIn(d))
        td = algo(r"Trial division $A(N)$", [r"for $d = 2, 3, \dots, \lfloor\sqrt N\rfloor$:", r">if $d \mid N$: return $d$"], fs=30)
        td.move_to(LEFT * 3.5 + DOWN * 0.6)
        an = VGroup(tx(r"input length: $\|N\| \approx \log N$ bits", 30),
                    tx(r"loop count: $\sqrt N = 2^{\log N / 2} \approx 2^{\|N\|/2}$", 30),
                    tx(r"exponential in the length $\Rightarrow$ \textbf{not PPT}", 30, BAD)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        an.move_to(RIGHT * 2.9 + DOWN * 0.6)
        with self.vo("Here's the classic trap. Factor N by trying every divisor up to root N. That sounds efficient. "
                     "But the input is N written in binary, about log N bits. Root N is two to the half of that length. "
                     "Exponential in the input length. Not P P T.") as d:
            self.play(FadeIn(td))
            for x in an:
                self.play(FadeIn(x, shift=0.2 * RIGHT))
                self.wait(d / 8)
        self.clear_all()
        un = VGroup(tx(r"Task: output an $n$-bit string. \ Input $n$ in binary has only $\approx \log n$ bits,", 32),
                    tx(r"so even printing $0^n$ takes time $n \approx 2^{\log n}$: exponential!", 32, BAD),
                    tx(r"Fix: give the input in \textbf{unary}, $1^n$ (a string of $n$ ones). \ Its length is $n$.", 32, GOOD),
                    tx(r"That's why we write $\mathrm{Gen}(1^n)$, $\mathrm{Blum}(1^n)$, $\mathrm{Primes}(1^n)$.", 32, HL)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        with self.vo("The same issue explains a strange notation. Say an algorithm takes n and must output n bits. If n "
                     "is written in binary, the input is only log n bits, and writing n output bits is exponential in "
                     "that. The fix is to hand it n in unary, as n ones, an input of length n. That's why key "
                     "generation and samplers take one to the n as input.") as d:
            for x in un:
                self.play(FadeIn(x, shift=0.2 * RIGHT))
                self.wait(d / 8)
        self.clear_all()


class Ex21(VScene):
    def construct(self):
        self.header("Exam-style", r"Ex.\ 2.1: PPT or not?")
        algs = VGroup(
            algo(r"$A_1(x)$", [r"$z = 0$", r"for $i = 1..n$:", r">$z := z+1$", r"return $z$"], fs=26),
            algo(r"$A_2(x)$", [r"$z = 0$", r"for $i = 1..2^{10000}$:", r">$z := z+1$", r"return $z$"], fs=26),
            algo(r"$A_3(x)$", [r"$z = 0$", r"for $i = 1..x$:", r">$z := z+1$", r"return $z$"], fs=26),
            algo(r"$A_4(1^x)$", [r"$z = 0$", r"for $i = 1..x$:", r">$z := z+1$", r"return $z$"], fs=26),
        ).arrange(RIGHT, buff=0.3).to_edge(UP, buff=1.15)
        fit(algs, 13.0)
        with self.vo("Exercise two point one. Input x is an n bit string, read as a number. Which of these are P P T? "
                     "The hint says three are. Pause and decide.") as d:
            self.play(LaggedStart(*[FadeIn(a, shift=0.2 * DOWN) for a in algs], lag_ratio=0.2))
        self.wait(2.5)
        verdicts = [(r"$n$ steps", r"\textbf{PPT}", GOOD), (r"constant! ($2^{10000}$ is a fixed number)", r"\textbf{PPT}", GOOD),
                    (r"$x$ can be $2^n - 1$", r"\textbf{not PPT}", BAD), (r"input length is $x$; \ $x$ steps", r"\textbf{PPT}", GOOD)]
        vs = VGroup()
        for (why, v, col), a in zip(verdicts, algs):
            g = VGroup(tx(why, 24, GREY_A), tx(v, 30, col)).arrange(DOWN, buff=0.15)
            if g.width > a.width:
                g.scale_to_fit_width(a.width)
            g.next_to(a, DOWN, buff=0.35)
            vs.add(g)
        narr = ["A one loops n times. Linear in the input length: P P T.",
                "A two loops two to the ten thousand times. Huge, but it's a fixed constant that doesn't grow with n. "
                "Constant time is polynomial: P P T. Asymptotics only care about growth.",
                "A three loops x times, the value of the input. An n bit x can be two to the n minus one. Exponential: "
                "not P P T.",
                "A four gets its input in unary, one to the x, so the input length is x itself, and x loop steps is "
                "linear: P P T. Same loop as A three, different input encoding."]
        for v, t in zip(vs, narr):
            with self.vo(t):
                self.play(FadeIn(v, shift=0.2 * UP))
        self.clear_all()


class Ex22(VScene):
    def construct(self):
        self.header("Exam-style", r"Ex.\ 2.2 = Quiz 3 Q2")
        b2 = algo(r"$B_2(x)$", [r"for $i = 1..n$:", r">$z_i := A(x)$", r"return $(z_1..z_n)$"], fs=28)
        b3 = algo(r"$B_3(x)$", [r"$z_0 := x$", r"for $i = 1..n$:", r">$z_i := A(z_{i-1})$", r"return $(z_1..z_n)$"], fs=28)
        b2.move_to(LEFT * 3.6).to_edge(UP, buff=1.15)
        b3.move_to(RIGHT * 3.0).to_edge(UP, buff=1.15)
        with self.vo("Exercise two point two, which was quiz three, question two. A is any P P T algorithm. B two calls "
                     "A n times on the same input x. B three feeds each output back in as the next input."):
            self.play(FadeIn(b2), FadeIn(b3))
        s2 = VGroup(tx(r"$B_2$: $n$ calls, each poly$(n)$", 30, GOOD),
                    tx(r"$\Rightarrow$ $n\cdot$poly$(n)$ = poly: \textbf{PPT}", 30, GOOD)).arrange(DOWN, buff=0.15)
        s2.next_to(b2, DOWN, buff=0.4)
        fit(s2, 5.4)
        with self.vo("B two is P P T. Each call runs on the same n bit input, so each takes polynomial time, and n of "
                     "them is still polynomial."):
            self.play(FadeIn(s2))
        q = qframe(r"Find a PPT $A$ that makes $B_3$ \emph{not} PPT.", 34)
        fit(q, 6.0).next_to(b3, DOWN, buff=0.4)
        with self.vo("B three is the interesting one. Can you find a P P T algorithm A that makes B three slow?"):
            self.play(FadeIn(q))
        self.wait(2.5)
        self.play(FadeOut(q))
        A = algo(r"Counterexample: \ $A(z) = z \Vert z$", [r"(copy the input twice: linear time, so PPT)"], fs=28, title_color=GOOD)
        fit(A, 6.2).next_to(b3, DOWN, buff=0.4)
        with self.vo("Let A double its input: output z concatenated with itself. That's linear time, clearly P P T."):
            self.play(FadeIn(A))
        lens = VGroup(M(r"|z_0| = n", font_size=34), M(r"|z_1| = 2n", font_size=34), M(r"|z_2| = 4n", font_size=34),
                      M(r"\cdots", font_size=34), M(r"|z_n| = 2^n \cdot n", font_size=34, color=BAD))
        lens.arrange(RIGHT, buff=0.45).move_to(DOWN * 1.9)
        fit(lens, 12.8)
        with self.vo("Now trace B three. The input has length n. After one round, two n. Then four n. Each round "
                     "doubles. After n rounds the last output has length two to the n times n.") as d:
            for x in lens:
                self.play(FadeIn(x, shift=0.2 * RIGHT), run_time=0.5)
                self.wait(d / 9)
        con = tx(r"Just \emph{writing} $z_n$ takes $2^n n$ steps $\Rightarrow$ $B_3$ is \textbf{not PPT}.", 32, HL).to_edge(DOWN, buff=0.5)
        with self.vo("Just writing down that output takes exponential time, so B three is not P P T. The lesson: "
                     "calling a polynomial time algorithm on growing inputs can compound. On the quiz, the A that was "
                     "given only grew its input by a constant amount, which isn't enough."):
            self.play(FadeIn(con))
            self.play(Create(boxed(con)))
        self.clear_all()


class ModExp2(VScene):
    def construct(self):
        self.header("Fast arithmetic", "repeated squaring")
        pr = rows(r"$+, -, \times, \div$, and $[x \bmod m]$ on $n$-bit numbers: poly time \checkmark",
                  r"$a^x \bmod m$ by multiplying $x$ times: $x \approx 2^{\|x\|}$ steps --- \textbf{not} poly",
                  fs=32, buff=0.3).to_edge(UP, buff=1.15)
        with self.vo("Basic arithmetic on n bit numbers, including taking remainders, is polynomial time. But computing "
                     "a to the x mod m by multiplying x times is not, since x is exponential in its bit length."):
            self.play(FadeIn(pr[0]))
            self.play(FadeIn(pr[1]))
        ex = tx(r"Example: \ $3^{13} \bmod 7$, \quad $13 = 8 + 4 + 1 = \texttt{1101}_2$", 34, HL).next_to(pr, DOWN, buff=0.5)
        sq = VGroup(M(r"3^1 \equiv 3", font_size=36), M(r"3^2 \equiv 9 \equiv 2", font_size=36),
                    M(r"3^4 \equiv 2^2 = 4", font_size=36), M(r"3^8 \equiv 4^2 = 16 \equiv 2", font_size=36)).arrange(RIGHT, buff=0.6)
        sq.next_to(ex, DOWN, buff=0.45)
        fit(sq, 12.8)
        with self.vo("Repeated squaring fixes this. To get three to the thirteen mod seven, write thirteen in binary: "
                     "eight plus four plus one. Then square repeatedly, reducing each time. Three, then nine which is "
                     "two, then two squared is four, then four squared is sixteen, which is two.") as d:
            self.play(FadeIn(ex))
            for x in sq:
                self.play(FadeIn(x, shift=0.2 * RIGHT))
                self.wait(d / 10)
        res = M(r"3^{13} = 3^8 \cdot 3^4 \cdot 3^1 \equiv 2 \cdot 4 \cdot 3 = 24 \equiv 3 \pmod 7", font_size=40, color=HL).next_to(sq, DOWN, buff=0.5)
        with self.vo("Multiply the powers for the one bits: eight, four and one. Two times four times three is twenty "
                     "four, which is three mod seven."):
            self.play(Indicate(VGroup(sq[0], sq[2], sq[3])))
            self.play(Write(res))
            self.play(Create(boxed(res)))
        cost = tx(r"About $2\|x\|$ multiplications of numbers below $m$ $\Rightarrow$ modular exponentiation is PPT.", 30, GOOD).to_edge(DOWN, buff=0.45)
        with self.vo("That's about two multiplications per bit of x, so modular exponentiation is P P T. We'll lean "
                     "on this constantly in the number theory weeks."):
            self.play(FadeIn(cost))
        self.clear_all()


class Negl2(VScene):
    def construct(self):
        self.header("Negligible", r"Def.\ 2.4")
        mot = VGroup(tx(r"Any attacker can \emph{guess} and get lucky with some tiny probability $\varepsilon(n)$.", 32),
                     tx(r"Repeating $t(n)$ times: \ $\Pr[\text{some try wins}] \le t(n)\,\varepsilon(n)$ \ (union bound)", 32),
                     tx(r"We want this to vanish for \emph{every} polynomial number of tries $t$.", 32, HL)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        mot.to_edge(UP, buff=1.15)
        with self.vo("Why do we need a notion of tiny? Every attacker can guess, and get lucky with some small "
                     "probability epsilon. An efficient attacker can also repeat its attempt a polynomial number of "
                     "times, and by the union bound that multiplies its chance by at most t. So we want epsilon so "
                     "small that t times epsilon still goes to zero, for every polynomial t.") as d:
            for x in mot:
                self.play(FadeIn(x, shift=0.2 * RIGHT))
                self.wait(d / 6)
        dfn = VGroup(tx(r"\textbf{$f$ is negligible} \ if for \textbf{every} $c \ge 0$: \ $f(n) = O(1/n^c)$", 36, HL),
                     tx(r"equivalently: for every $c$, for all sufficiently large $n$, \ $f(n) < 1/n^c$", 30, GREY_A)).arrange(DOWN, buff=0.25)
        dfn.next_to(mot, DOWN, buff=0.55)
        with self.vo("Definition: f is negligible if, for every constant c, f is big O of one over n to the c. In words, "
                     "f eventually drops below every inverse polynomial, and stays there."):
            self.play(Write(dfn[0]))
            self.play(FadeIn(dfn[1]))
            self.play(Create(boxed(dfn[0])))
        self.clear_all()
        hdr = VGroup(M("n", font_size=34), M(r"1/n^5", font_size=34, color=HON), M(r"2^{-n}", font_size=34, color=ADV))
        data = [(10, "10^{-5}", r"\approx 10^{-3}"), (30, r"4\times 10^{-8}", r"\approx 10^{-9}"),
                (50, r"3\times 10^{-9}", r"\approx 10^{-15}"), (100, "10^{-10}", r"\approx 10^{-30}")]
        cells = [*hdr]
        for n, a, b in data:
            cells += [M(str(n), font_size=34), M(a, font_size=34, color=HON), M(b, font_size=34, color=ADV)]
        tbl = VGroup(*cells).arrange_in_grid(rows=5, cols=3, buff=(1.0, 0.3)).move_to(LEFT * 3 + DOWN * 0.1)
        with self.vo("Compare two to the minus n with one over n to the fifth. At n equals ten, two to the minus n is "
                     "actually bigger. But by thirty it's smaller, and by a hundred it's twenty orders of magnitude "
                     "smaller. Negligible functions eventually lose to every inverse polynomial.") as d:
            self.play(FadeIn(VGroup(*cells[:3])))
            for i in range(4):
                self.play(FadeIn(VGroup(*cells[3 + 3 * i: 6 + 3 * i])), run_time=0.6)
                self.wait(d / 9)
        ex = VGroup(tx(r"\textbf{negligible:} \ $2^{-n}$, \ $2^{-\sqrt n}$, \ $n^{-\log n}$, \ $1/n!$", 32, GOOD),
                    tx(r"\textbf{not negligible:} \ $1/n^2$, \ $1/(n\log n)$, \ $1/2$", 32, BAD),
                    tx(r"rule of thumb: $1/\text{(not poly)}$ is negligible", 28, GREY_A)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        ex.move_to(RIGHT * 3.4 + DOWN * 0.1)
        fit(ex, 6.4)
        with self.vo("Negligible: two to the minus n, two to the minus root n, n to the minus log n. Not negligible: "
                     "anything like one over a polynomial, and certainly constants like one half."):
            self.play(FadeIn(ex[0]))
            self.play(FadeIn(ex[1]))
            self.play(FadeIn(ex[2]))
        self.clear_all()


class Closure2(VScene):
    def construct(self):
        self.header("Exam-style", r"closure: Quiz 3 Q3 / Ex.\ 2.5")
        props = rows(r"poly $+$ poly, \ poly $\cdot$ poly, \ poly(poly) \ are poly",
                     r"negl $+$ negl \ is negl", r"\textbf{poly $\cdot$ negl \ is negl} \ (``negligible kills polynomials'')",
                     fs=32, buff=0.25).to_edge(UP, buff=1.15)
        with self.vo("Proposition two point one lists closure rules. Polynomials combined with polynomials stay "
                     "polynomial. Negligible plus negligible is negligible. And the big one: polynomial times "
                     "negligible is negligible. Quiz three asked you to prove that last one."):
            self.play(FadeIn(props))
            self.play(Indicate(props[2], color=HL))
        q = tx(r"\textbf{Claim.} $g$ poly-bounded, $h$ negligible $\Rightarrow$ $f = g \cdot h$ negligible.", 32, HL).next_to(props, DOWN, buff=0.45)
        steps = VGroup(
            tx(r"1. $g$ poly: there are $C_1, d, n_1$ with $g(n) \le C_1 n^d$ for $n \ge n_1$.", 30),
            tx(r"2. Fix an \emph{arbitrary} $c \ge 0$. \ (We must show $f = O(1/n^c)$.)", 30),
            tx(r"3. $h$ negligible: apply its definition with exponent $c + d$: \ $h(n) \le C_2 / n^{c+d}$ for $n \ge n_2$.", 30),
            tx(r"4. For $n \ge \max(n_1, n_2)$: \ $f(n) = g(n)h(n) \le C_1 n^d \cdot \dfrac{C_2}{n^{c+d}} = \dfrac{C_1C_2}{n^c}$.", 30),
            tx(r"5. So $f = O(1/n^c)$; \ $c$ was arbitrary $\Rightarrow$ $f$ is negligible. \ $\blacksquare$", 30, GOOD),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(q, DOWN, buff=0.35)
        fit(steps, 12.9)
        narr = ["Here's the full proof. Step one: unpack poly. There's a constant C one and a power d with g at most C "
                "one times n to the d, for large n.",
                "Step two: to prove negligible, fix an arbitrary c. Our job is to show f is big O of one over n to the c.",
                "Step three is the trick. h is negligible, so its definition works for any exponent we like. Use c plus "
                "d, to leave room to cancel g's growth.",
                "Step four: multiply. n to the d cancels against n to the c plus d, leaving a constant over n to the c.",
                "Step five: that's big O of one over n to the c, and c was arbitrary, so f is negligible. On the quiz, the "
                "start was right; what was missing was choosing the exponent c plus d."]
        with self.vo("Let's prove it, unpacking every definition."):
            self.play(FadeIn(q))
        for s, t in zip(steps, narr):
            with self.vo(t):
                self.play(FadeIn(s, shift=0.2 * RIGHT))
        self.clear_all()
        e23 = VGroup(tx(r"\textbf{Ex.\ 2.3} \ $f$ negligible $\iff$ $f(n) < \mathrm{negl}(n)$ eventually, for some negligible negl", 30, HL),
                     tx(r"($\Leftarrow$) \ $\mathrm{negl}(n) \le C/n^c$ eventually, and $f < \mathrm{negl}$ eventually $\Rightarrow f \le C/n^c$", 30),
                     tx(r"($\Rightarrow$) \ take $\mathrm{negl}(n) = f(n) + 2^{-n}$: \ negligible (negl $+$ negl) and strictly bigger than $f$", 30),
                     tx(r"(not $\mathrm{negl} = f$: we need strict $<$, which fails when $f(n) = 0$)", 26, GREY_A)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        fit(e23, 12.9)
        with self.vo("Exercise two point three is a similar unpacking exercise. If f sits below a negligible function "
                     "eventually, then f is below that function's constant over n to the c, so f is negligible. "
                     "Conversely, pick the bigger function f plus two to the minus n. It's negligible, since it's a "
                     "sum of negligibles, and it's strictly bigger than f, even where f is zero.") as d:
            for x in e23:
                self.play(FadeIn(x, shift=0.2 * RIGHT))
                self.wait(d / 7)
        self.clear_all()


class Ex26(VScene):
    def construct(self):
        self.header("Exam-style", r"Ex.\ 2.4 and 2.6")
        e24 = VGroup(tx(r"\textbf{Ex.\ 2.4} \ $f(n) = 1$ for even $n$, \ $f(n) = 2^n$ for odd $n$", 32, HL),
                     tx(r"not poly: on odd $n$, $2^n$ beats every $C n^c$ \qquad not negligible: on even $n$, $f(n) = 1$", 30)).arrange(DOWN, buff=0.2)
        e24.to_edge(UP, buff=1.15)
        fit(e24, 12.9)
        with self.vo("Exercise two point four: f is one on even n and two to the n on odd n. It's not polynomially "
                     "bounded, because on odd inputs it's exponential. And it's not negligible, because on even inputs "
                     "it's stuck at one. Definitions must hold for all large n, not just some."):
            self.play(FadeIn(e24))
        q = tx(r"\textbf{Ex.\ 2.6} \ each ticket wins w.p.\ $\varepsilon$, independently. \ Buy $t$ tickets so $\Pr[\ge 1 \text{ win}] \ge \tfrac14$.", 30, HL)
        q.next_to(e24, DOWN, buff=0.5)
        fit(q, 12.9)
        ex = M(r"\Pr[\ge 1 \text{ win}] = 1 - (1-\varepsilon)^t", font_size=38).next_to(q, DOWN, buff=0.3)
        with self.vo("Exercise two point six is about repetition. Each lottery ticket wins with probability epsilon, "
                     "independently. The chance at least one of t tickets wins is one minus the chance they all lose, "
                     "one minus one minus epsilon to the t."):
            self.play(FadeIn(q))
            self.play(Write(ex))
        parts = VGroup(
            tx(r"(a) $\varepsilon = \tfrac{1}{100}$: \ $0.99^t \le \tfrac34 \Rightarrow t \ge \tfrac{\ln(3/4)}{\ln(0.99)} \approx 28.6$ \ $\Rightarrow$ \ $t = 29$", 30),
            tx(r"(b) $\varepsilon = n^{-5}$: \ $(1-\varepsilon)^t \le e^{-\varepsilon t}$, so $t = \lceil n^5 \ln\tfrac43 \rceil$ works: \textbf{poly}", 30, GOOD),
            tx(r"(c) $\varepsilon = 2^{-n}$: \ $\Pr \le t\varepsilon$ (union bound), so need $t \ge 2^n/4$: \textbf{not poly}", 30, BAD),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(ex, DOWN, buff=0.4)
        fit(parts, 12.9)
        narr = ["Part a, epsilon one percent. We need point nine nine to the t at most three quarters. Take logs: t at "
                "least about twenty eight point six, so twenty nine tickets.",
                "Part b, epsilon is n to the minus five. Use one minus x is at most e to the minus x. Then t equals n to "
                "the five times log of four thirds is enough. That's a polynomial number of tickets.",
                "Part c, epsilon is two to the minus n. Now flip it around: by the union bound, the win chance is at most "
                "t times epsilon, so reaching one quarter needs t at least two to the n over four. Not polynomial."]
        for p, t in zip(parts, narr):
            with self.vo(t):
                self.play(FadeIn(p, shift=0.2 * RIGHT))
        les = tx(r"Non-negligible success can be boosted by repetition; negligible success cannot.", 30, HL).to_edge(DOWN, buff=0.4)
        with self.vo("That's the whole point of the definition. Any non negligible success chance can be pumped up to a "
                     "constant with polynomially many tries. But a negligible one can't."):
            self.play(FadeIn(les))
        self.clear_all()


class Factoring2(VScene):
    def construct(self):
        self.header("Hardness", "the factoring assumption")
        avg = VGroup(tx(r"Crypto needs \textbf{average-case} hardness: hard on \emph{typical} random instances.", 32),
                     tx(r"Random $n$-bit $N$ is easy: it's even about half the time!", 30, BAD),
                     tx(r"Hard distribution: \ \textbf{Blum integers} \ $N = pq$, \ $p \ne q$ random $n$-bit primes, \ $p, q \equiv 3 \bmod 4$", 30, HL)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        avg.to_edge(UP, buff=1.15)
        fit(avg, 12.9)
        with self.vo("For cryptography, a problem must be hard on typical random instances, not just in the worst case. "
                     "So we must say which random numbers we factor. But a random number is easy: half the time it's even. "
                     "The hard distribution is Blum integers: multiply two distinct random n bit primes, both "
                     "congruent to three mod four.") as d:
            for x in avg:
                self.play(FadeIn(x, shift=0.2 * RIGHT))
                self.wait(d / 6)
        bl = algo(r"$\mathrm{Blum}(1^n)$", [r"$p, q \leftarrow \mathrm{Primes}(1^n)$", r"while $p = q$ or $p \not\equiv 3$ or $q \not\equiv 3 \pmod 4$: resample",
                                            r"return $N = pq$"], fs=28).next_to(avg, DOWN, buff=0.4)
        with self.vo("Here's the sampler. Notice it takes n in unary."):
            self.play(FadeIn(bl))
        self.clear_all()
        asm = VGroup(tx(r"\textbf{Assumption 2.1 (Factoring).} \ For every PPT $A$ there is a negligible negl with", 32, HL),
                     M(r"\Pr\big[\,1 < d < N \ \text{and}\ d \mid N\,\big] < \mathrm{negl}(n)", font_size=42),
                     tx(r"in the experiment: \ $N \leftarrow \mathrm{Blum}(1^n)$, \ $d \leftarrow A(N)$", 32)).arrange(DOWN, buff=0.35)
        asm.move_to(UP * 0.6)
        with self.vo("The factoring assumption: for every P P T algorithm A, the probability that A, given a random "
                     "Blum integer, outputs a nontrivial divisor is negligible in n. Every word in that sentence is "
                     "something we just defined."):
            self.play(FadeIn(asm[0]))
            self.play(Write(asm[1]), run_time=2)
            self.play(FadeIn(asm[2]))
            self.play(Create(boxed(asm)))
        rd = tx(r"Notation: the probability is over \emph{both} sampling $N$ and $A$'s coins; \ both sides are functions of $n$.", 28, GREY_A)
        rd.to_edge(DOWN, buff=0.6)
        fit(rd, 12.9)
        with self.vo("Read the probability carefully: it's over the random choice of N and the algorithm's own coins. "
                     "In week three we'll use this assumption to prove that computing square roots mod N is hard."):
            self.play(FadeIn(rd))
        self.clear_all()


class Recap2(VScene):
    def construct(self):
        self.header("Part 2", "recap")
        r = recap_list([r"Efficient = PPT: worst-case time poly in input \textbf{length}.",
                        r"Loops up to a number's value are exponential; unary $1^n$ fixes input length.",
                        r"Iterating $A$ on its own output can blow up ($A(z) = z\Vert z$).",
                        r"Negligible: below $1/n^c$ eventually, for \emph{every} $c$. \ poly $\cdot$ negl $=$ negl.",
                        r"Proofs: fix arbitrary $c$, unpack each definition, pick exponents (like $c + d$).",
                        r"Factoring: no PPT $A$ factors random Blum integers except w.p.\ negl$(n)$."], fs=30)
        fit(r, 12.8).move_to(DOWN * 0.2)
        with self.vo("Recap. Efficient means polynomial in the input length. Loops up to a number's value are "
                     "exponential, which is why we use unary inputs. Iterating an algorithm on its own output can blow "
                     "up. Negligible means eventually below every inverse polynomial, and polynomial times negligible is "
                     "negligible. For proofs, fix an arbitrary c and unpack each definition. And the factoring "
                     "assumption says random Blum integers can't be factored efficiently.") as d:
            for line in r:
                self.play(FadeIn(line, shift=0.2 * RIGHT), run_time=0.6)
                self.wait(d / 8)
        nxt = tx(r"Next: Part 3 --- number theory: inverses, CRT, square roots, and reductions", 30, HL).to_edge(DOWN, buff=0.4)
        with self.vo("Next, part three: the number theory behind square roots, and our first proof by reduction."):
            self.play(FadeIn(nxt))
        self.wait(1)
