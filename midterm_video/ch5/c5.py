from cx import *


def game(left_lines, right_lines, msgs):
    """Challenger (left) vs adversary (right) diagram. msgs = [(text, direction)] with direction 'r' or 'l'."""
    ch = VGroup(*[tx(s, 28) for s in left_lines]).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    ad = VGroup(*[tx(s, 28) for s in right_lines]).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    chb = panel(ch, HON)
    adb = panel(ad, ADV)
    cg = VGroup(chb, ch, tx(r"\textbf{Challenger}", 30, HON).next_to(chb, UP, buff=0.12))
    ag = VGroup(adb, ad, tx(r"\textbf{Adversary $A$}", 30, ADV).next_to(adb, UP, buff=0.12))
    cg.move_to(LEFT * 4.0)
    ag.move_to(RIGHT * 4.0)
    arrows = VGroup()
    ys = np.linspace(0.8, -0.8, len(msgs))
    for (t, d), y in zip(msgs, ys):
        a, b = (LEFT * 1.4, RIGHT * 1.4) if d == "r" else (RIGHT * 1.4, LEFT * 1.4)
        ar = Arrow(a + UP * y, b + UP * y, buff=0, color=GREY_B, stroke_width=3)
        lab = tx(t, 28).next_to(ar, UP, buff=0.08)
        arrows.add(VGroup(ar, lab))
    return cg, ag, arrows


class Intro5(VScene):
    def construct(self):
        title = tx(r"\textbf{Part 5: Public-Key Encryption from Factoring}", 48, HL).move_to(UP * 0.4)
        sub = tx(r"Week 5 \quad (notes chapter 5)", 30, GREY_A).next_to(title, DOWN)
        with self.vo("Part five: public key encryption, built from factoring."):
            self.play(Write(title), FadeIn(sub))
        self.play(FadeOut(title), FadeOut(sub))
        self.header("Public-key encryption", r"Def.\ 5.1, 5.2")
        mot = tx(r"Symmetric keys: 1000 people talking pairwise need $\binom{1000}{2} \approx 500{,}000$ shared keys.", 32)
        mot.to_edge(UP, buff=1.15)
        fit(mot, 12.9)
        with self.vo("With symmetric encryption, every pair of people needs its own shared key. A thousand people need "
                     "about half a million. Public key encryption fixes this: Bob publishes one public key that anyone can "
                     "encrypt with, and keeps a secret key for decrypting."):
            self.play(FadeIn(mot))
        syn = VGroup(tx(r"$\mathrm{Gen}(1^n) \to (pk, sk)$ \quad key generation; $n$ in unary", 32),
                     tx(r"$\mathrm{Enc}(pk, m) \to c$ \quad \textbf{randomized}, uses only the \emph{public} key", 32),
                     tx(r"$\mathrm{Dec}(sk, c) \to m$ \quad deterministic, needs the \emph{secret} key", 32)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        syn.next_to(mot, DOWN, buff=0.5)
        with self.vo("The syntax has three algorithms. Gen takes the security parameter in unary and outputs a key pair. "
                     "Enc uses only the public key, and is randomized. Dec uses the secret key, deterministically.") as d:
            for x in syn:
                self.play(FadeIn(x, shift=0.2 * RIGHT))
                self.wait(d / 7)
        cor = M(r"\text{for all large } n,\ \forall m:\quad \Pr_{(pk,sk)\leftarrow \mathrm{Gen}(1^n),\,\mathrm{Enc}}\big[\mathrm{Dec}(sk, \mathrm{Enc}(pk, m)) = m\big] = 1",
                font_size=34, color=HL).next_to(syn, DOWN, buff=0.5)
        fit(cor, 12.9)
        with self.vo("Correctness: for all large enough n and every message, decrypting gives the message back with "
                     "probability one, over the key generation and the encryption randomness. Probability one means no "
                     "bad keys at all."):
            self.play(Write(cor), run_time=2)
        self.clear_all()
        bad = VGroup(tx(r"\textbf{Ex.\ 5.2 (correct, insecure):} \ $pk = (x, p)$, \ $sk = (x^{-1} \bmod p, p)$", 32, HL),
                     tx(r"$\mathrm{Enc}(pk, m) = [x m \bmod p]$, \quad $\mathrm{Dec}(sk, c) = [x^{-1} c \bmod p] = m$ \checkmark", 32),
                     tx(r"Insecure: anyone computes $x^{-1} = x^{p-2} \bmod p$ from $pk$. \ The secret key must be \emph{hard} to derive.", 32, BAD)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        fit(bad, 12.9)
        with self.vo("A warning example from the notes. Make the public key a number x and a prime p, and encrypt by "
                     "multiplying by x mod p. Decrypting multiplies by the inverse. Correct, but useless: anyone can compute "
                     "the inverse from the public key using Fermat. The secret key must be hard to compute from the public "
                     "key, and that's where factoring comes in.") as d:
            for x in bad:
                self.play(FadeIn(x, shift=0.2 * RIGHT))
                self.wait(d / 6)
        self.clear_all()


class Rabin5(VScene):
    def construct(self):
        self.header("Rabin's PKE", r"Def.\ 5.4 (1-bit messages)")
        gen = algo(r"$\mathrm{Gen}(1^n)$", [r"$(p, q, N) \leftarrow \mathrm{Blum}(1^n)$", r"$pk := N$, \ $sk := (p, q)$"], fs=28)
        enc = algo(r"$\mathrm{Enc}(N, m)$", [r"$r \xleftarrow{\$} QR_N$", r"$z := \mathrm{LSB}(r) \oplus m$", r"$y := [r^2 \bmod N]$", r"return $(z, y)$"], fs=28)
        dec = algo(r"$\mathrm{Dec}((p,q), (z, y))$", [r"$r := \mathrm{sqrtBlum}(y, p, q)$", r"\quad (the principal root)", r"return $\mathrm{LSB}(r) \oplus z$"], fs=28)
        g = VGroup(gen, enc, dec).arrange(RIGHT, buff=0.35, aligned_edge=UP).to_edge(UP, buff=1.15)
        fit(g, 13.0)
        with self.vo("Rabin's scheme, exactly the one from the end of part four. The public key is a Blum integer N; the "
                     "secret key is its factors. To encrypt a bit, pick a random residue r, and send m XOR the LSB of r, "
                     "together with r squared. To decrypt, use the factors to find the principal root of y, which is r, "
                     "and XOR its LSB back off.") as d:
            self.play(FadeIn(gen))
            self.play(FadeIn(enc))
            self.play(FadeIn(dec))
        ex = VGroup(tx(r"\textbf{Toy run:} $N = 77$, \ $m = 1$, \ $r = 67 \in QR_{77}$, \ LSB$(r) = 1$", 30, HL),
                    tx(r"$z = 1 \oplus 1 = 0$, \ \ $y = 67^2 \bmod 77 = 23$, \ \ $c = (0, 23)$", 30, CT),
                    tx(r"Bob: principal root of 23 is 67 (Part 3) $\Rightarrow$ $\mathrm{LSB}(67) \oplus 0 = 1 = m$ \checkmark", 30, GOOD)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        ex.next_to(g, DOWN, buff=0.45)
        fit(ex, 12.9)
        with self.vo("A toy run with N equals seventy seven. Encrypt the bit one with r equals sixty seven, a residue. Its "
                     "LSB is one, so z is zero, and y is sixty seven squared, which is twenty three. Bob finds the principal "
                     "root of twenty three, sixty seven, and recovers one.") as d:
            for x in ex:
                self.play(FadeIn(x, shift=0.2 * RIGHT))
                self.wait(d / 7)
        cl = tx(r"\textbf{Correctness (Claim 5.1):} $r \in QR_N$ is \emph{the} principal root of $y$, so Dec recomputes it: \ $\mathrm{LSB}(r) \oplus \mathrm{LSB}(r) \oplus m = m$.", 28)
        cl.to_edge(DOWN, buff=0.4)
        fit(cl, 12.9)
        with self.vo("The correctness proof is one line: r is a residue, so it is the principal root of y, so decryption "
                     "recomputes exactly r, and the two LSBs cancel."):
            self.play(FadeIn(cl))
        self.clear_all()


class IND5(VScene):
    def construct(self):
        self.header("IND security", r"Def.\ 5.5 -- 5.8")
        why = VGroup(tx(r"Perfect secrecy as a game: any $A$ given only $c^* \leftarrow \mathrm{Enc}_k(b)$ guesses $b$ w.p.\ exactly $\tfrac12$.", 30),
                     tx(r"For PKE, $A$ also gets $pk$ --- and $(pk, c^*)$ determines $b$ (correctness)!", 30, BAD),
                     tx(r"So: only demand security against \textbf{PPT} $A$, up to \textbf{negligible} advantage.", 30, HL)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        why.to_edge(UP, buff=1.15)
        fit(why, 12.9)
        with self.vo("How do we define security for public key encryption? Perfect secrecy can be phrased as a guessing "
                     "game: given a ciphertext of a random bit, no one guesses the bit better than half. But in public key "
                     "encryption, the adversary also has the public key, and together with the ciphertext that pins down "
                     "the message, by correctness. An all powerful adversary could just search. So we only ask for security "
                     "against efficient adversaries, up to negligible advantage.") as d:
            for x in why:
                self.play(FadeIn(x, shift=0.2 * RIGHT))
                self.wait(d / 6)
        self.clear_all()
        cg, ag, arrows = game([r"$(pk, sk) \leftarrow \mathrm{Gen}(1^n)$", r"$b \xleftarrow{\$} \{0,1\}$", r"$c^* \leftarrow \mathrm{Enc}(pk, b)$"],
                              [r"sees $pk$ and $c^*$", r"outputs a guess $\hat b$"],
                              [(r"$pk,\ c^*$", "r"), (r"$\hat b$", "l")])
        VGroup(cg, ag, arrows).shift(UP * 0.6)
        with self.vo("Here's the experiment. The challenger generates keys, flips a secret bit b, and encrypts it. The "
                     "adversary sees the public key and the challenge ciphertext, and outputs a guess b hat."):
            self.play(FadeIn(cg))
            self.play(FadeIn(ag))
            self.play(LaggedStart(*[FadeIn(a) for a in arrows], lag_ratio=0.5))
        adv = VGroup(M(r"\mathrm{Adv}^{IND}_{\Pi, A}(n) = \Big|\Pr[\hat b = b] - \tfrac12\Big|", font_size=40, color=HL),
                     tx(r"$\Pi$ is \textbf{IND secure} if this is negligible for \textbf{every PPT} $A$.", 32),
                     M(r"\text{Equivalent: } \big|\Pr[A(pk, \mathrm{Enc}(pk,0)) = 1] - \Pr[A(pk, \mathrm{Enc}(pk,1)) = 1]\big| \text{ negligible } (= 2\,\mathrm{Adv})", font_size=30)).arrange(DOWN, buff=0.3)
        adv.to_edge(DOWN, buff=0.4)
        fit(adv, 12.9)
        with self.vo("The advantage is how much better than a coin flip the guess is. The scheme is IND secure if every "
                     "efficient adversary has negligible advantage. An equivalent form, often easier: the probability A "
                     "says one on an encryption of zero, minus the probability it says one on an encryption of one. That "
                     "difference is exactly twice the advantage."):
            self.play(Write(adv[0]))
            self.play(FadeIn(adv[1]))
            self.play(FadeIn(adv[2]))
        self.clear_all()
        pf = VGroup(tx(r"\textbf{Ex.\ 5.3 / Claim 5.2:} \ write $P_b = \Pr[\mathrm{Exp}(n, b) = 1]$ (A outputs a bit).", 32, HL),
                    M(r"\Pr[\hat b = b] = \tfrac12 \Pr[\hat b = 0 \mid b=0] + \tfrac12 \Pr[\hat b = 1 \mid b = 1] = \tfrac12(1 - P_0) + \tfrac12 P_1", font_size=34),
                    M(r"= \tfrac12 + \tfrac12 (P_1 - P_0) \;\Rightarrow\; \big|\Pr[\hat b = b] - \tfrac12\big| = \tfrac12 |P_0 - P_1|", font_size=36, color=GOOD)).arrange(DOWN, buff=0.35)
        fit(pf, 12.9)
        with self.vo("Why twice? Split on the bit b, each case with probability one half. Being right when b is zero means "
                     "outputting zero, which happens with probability one minus P zero. Being right when b is one has "
                     "probability P one. Rearranging, the distance from one half is half the gap between P zero and P one."):
            for x in pf:
                self.play(FadeIn(x, shift=0.2 * UP))
        self.clear_all()


class Ex51(VScene):
    def construct(self):
        self.header("Exam-style", r"Ex.\ 5.1 (= Quiz 6 Q1)")
        q = tx(r"$\Pi$ correct, 1-bit messages. Show an \textbf{unbounded} adversary finds $m$ from $(pk, c)$ w.p.\ 1.", 32, HL).to_edge(UP, buff=1.15)
        fit(q, 12.9)
        with self.vo("Exercise five point one, quiz six question one. Show that an adversary with unlimited time recovers the "
                     "message from the public key and ciphertext, with probability one."):
            self.play(FadeIn(q))
        trick = tx(r"Key trick (grader's hint): write $\mathrm{Enc}(pk, m; \rho)$ with \textbf{all its random coins} $\rho$ as an input.", 30, GOOD)
        trick.next_to(q, DOWN, buff=0.4)
        fit(trick, 12.9)
        with self.vo("The trick is to treat encryption's random coins as an extra input, rho. Encryption is randomized, but "
                     "once you fix the coins it's a deterministic function."):
            self.play(FadeIn(trick))
        alg = algo(r"$A(pk, c)$ \quad (exponential time is allowed)",
                   [r"for every possible coin string $\rho$:", r">if $\mathrm{Enc}(pk, 0; \rho) = c$: \ return $0$", r"return $1$"], fs=30)
        alg.next_to(trick, DOWN, buff=0.4)
        with self.vo("The adversary tries every possible coin string. If some coins make the encryption of zero equal c, it "
                     "says zero. Otherwise it says one."):
            self.play(FadeIn(alg))
        why = VGroup(tx(r"If $m = 0$: the real coins are in the list, so $A$ returns $0$. \checkmark", 30),
                     tx(r"If $m = 1$: could $c$ also be an encryption of $0$? Then $\mathrm{Dec}(sk, c)$ would have to equal", 30),
                     tx(r"both $0$ and $1$ --- impossible, since Dec is deterministic and correct. \ So $A$ returns $1$. \checkmark", 30)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        why.next_to(alg, DOWN, buff=0.4)
        fit(why, 12.9)
        with self.vo("If m is zero, the real coins are somewhere in the list, so it answers zero. If m is one, can c also be "
                     "an encryption of zero? No: then decrypting c would have to give both zero and one, impossible for a "
                     "correct, deterministic decryption. So it answers one. Always right. On the quiz, the answer assumed "
                     "encryption was deterministic. In general it's randomized, which is why we loop over coins."):
            for x in why:
                self.play(FadeIn(x, shift=0.15 * RIGHT))
        self.clear_all()


class Ex52(VScene):
    def construct(self):
        self.header("Exam-style", r"Ex.\ 5.2 (= Quiz 6 Q2)")
        q = tx(r"$\Pi$ correct with \textbf{deterministic} Enc, $|\mathcal M| > 1$. \ Prove $\Pi$ is \textbf{not} IND secure.", 32, HL).to_edge(UP, buff=1.15)
        with self.vo("Exercise five point two, quiz six question two. If encryption is deterministic, the scheme can't be "
                     "IND secure, for any message space with at least two messages. To show a scheme is not secure, you "
                     "must give a concrete efficient adversary and compute its advantage."):
            self.play(FadeIn(q))
        cg, ag, arrows = game([r"$(pk, sk) \leftarrow \mathrm{Gen}(1^n)$", r"$b \xleftarrow{\$} \{0, 1\}$", r"$c^* := \mathrm{Enc}(pk, m_b)$"],
                              [r"pick distinct $m_0, m_1$, same length", r"$c_0 := \mathrm{Enc}(pk, m_0)$ \ (pk is public!)",
                               r"return $0$ if $c^* = c_0$, else $1$"],
                              [(r"$pk$", "r"), (r"$m_0, m_1$", "l"), (r"$c^*$", "r"), (r"$\hat b$", "l")])
        grp = VGroup(cg, ag, arrows).next_to(q, DOWN, buff=0.6)
        fit(grp, 13.0)
        with self.vo("Use the general experiment, where the adversary picks two messages. Our adversary picks any two "
                     "different messages of the same length. Since the public key is public, it encrypts m zero itself. "
                     "When the challenge arrives, it answers zero if the challenge matches its own ciphertext, and one "
                     "otherwise.") as d:
            self.play(FadeIn(cg), FadeIn(ag))
            self.play(LaggedStart(*[FadeIn(a) for a in arrows], lag_ratio=0.4), run_time=2.5)
        an = VGroup(tx(r"$b = 0$: deterministic $\Rightarrow c^* = c_0$ $\Rightarrow \hat b = 0$ \checkmark", 30),
                    tx(r"$b = 1$: if $\mathrm{Enc}(m_1) = \mathrm{Enc}(m_0)$, Dec couldn't return both $\Rightarrow c^* \ne c_0 \Rightarrow \hat b = 1$ \checkmark", 30),
                    M(r"\Pr[\hat b = b] = 1 \;\Rightarrow\; \mathrm{Adv} = \tfrac12 \ (\text{or } |P_0 - P_1| = 1): \text{ not negligible}", font_size=34, color=HL)).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        an.to_edge(DOWN, buff=0.4)
        fit(an, 12.9)
        with self.vo("Analyze both cases, using the law of total probability. If b is zero, determinism means the challenge "
                     "equals the adversary's own encryption, so it answers zero. If b is one, the two encryptions must "
                     "differ, by correctness, so it answers one. It's always right: advantage one half, which is "
                     "certainly not negligible. Moral: IND security requires randomized encryption.") as d:
            for x in an:
                self.play(FadeIn(x, shift=0.15 * RIGHT))
                self.wait(d / 8)
        self.clear_all()
        e54 = VGroup(tx(r"\textbf{Ex.\ 5.4} \ ciphertexts only $L(n) = O(\log n)$ bits $\Rightarrow$ at most $2^{L} = \mathrm{poly}(n)$ of them.", 30, HL),
                     algo(r"$A(pk, c^*)$", [r"$c_0 \leftarrow \mathrm{Enc}(pk, 0)$ \ (fresh coins)", r"return $0$ if $c^* = c_0$, else $1$"], fs=28),
                     tx(r"$b = 1$: never equal (correctness) $\Rightarrow$ always right. \ $b = 0$: two independent encryptions of 0 collide", 28),
                     tx(r"w.p.\ $\sum_c p_c^2 \ge 1/2^{L}$ (Cauchy--Schwarz). \ So $\mathrm{Adv} \ge \tfrac12 \cdot 2^{-L(n)} = 1/\mathrm{poly}(n)$: not negligible.", 28, GOOD)).arrange(DOWN, buff=0.28)
        fit(e54, 12.9)
        with self.vo("Exercise five point four uses the same idea when encryption is randomized but ciphertexts are short, "
                     "only log n bits, so there are only polynomially many. Encrypt zero yourself and compare. If b is one "
                     "you're always right. If b is zero, two independent encryptions of zero collide with probability at "
                     "least one over the number of possible ciphertexts, which is one over a polynomial. So the advantage "
                     "is non negligible.") as d:
            for x in e54:
                self.play(FadeIn(x, shift=0.15 * UP))
                self.wait(d / 8)
        self.clear_all()


class Thm53(VScene):
    def construct(self):
        self.header("Theorem 5.3", "Rabin is IND secure (if Factoring)")
        plan = tx(r"Plan: an IND attacker $A$ on Rabin $\Rightarrow$ an LSB predictor $B$ $\Rightarrow$ contradicts Theorem 4.3.", 32, HL).to_edge(UP, buff=1.15)
        fit(plan, 12.9)
        with self.vo("Now the main theorem: if factoring is hard, Rabin's scheme is IND secure. The plan: turn any IND "
                     "attacker A into a predictor B for the LSB of the principal root, which theorem four point three says "
                     "can't exist."):
            self.play(FadeIn(plan))
        obs = VGroup(tx(r"\textbf{Key observation:} for $x \in QR_N$, $y = x^2$, and \emph{any} bit $z$:", 32),
                     tx(r"$(z, y)$ is exactly $\mathrm{Enc}(N, m)$ with coins $r = x$, for the message $m = z \oplus \mathrm{LSB}(x)$.", 32, GOOD)).arrange(DOWN, buff=0.2)
        obs.next_to(plan, DOWN, buff=0.45)
        fit(obs, 12.9)
        with self.vo("The key observation. B is given N and y, the square of an unknown principal root x. Pick any bit z. "
                     "The pair z, y is a perfectly valid Rabin ciphertext, made with coins x, of the message z XOR LSB of x. "
                     "B doesn't know that message, but A might figure it out."):
            self.play(FadeIn(obs))
        alg = algo(r"$B(N, y)$", [r"$z \xleftarrow{\$} \{0, 1\}$", r"$\hat b \leftarrow A(N, (z, y))$", r"return $\hat b \oplus z$"], fs=30)
        alg.next_to(obs, DOWN, buff=0.4).to_edge(LEFT, buff=1.0)
        an = VGroup(tx(r"$z$ uniform $\Rightarrow$ $m$ uniform: $A$'s view $= $ IND game exactly", 28),
                    tx(r"$A$ right ($\hat b = m$) $\iff$ $\hat b \oplus z = \mathrm{LSB}(x)$ $\iff$ $B$ right", 28),
                    M(r"\big|\Pr[B = \mathrm{LSB}(x)] - \tfrac12\big| = \mathrm{Adv}^{IND}_A", font_size=34, color=HL)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        an.next_to(alg, RIGHT, buff=0.5)
        fit(an, 7.4)
        with self.vo("So here's B: pick z at random, hand A the ciphertext z, y, and XOR A's answer with z. Because z is "
                     "uniform, the hidden message is a uniform bit, and A sees exactly what it sees in the IND game. A is "
                     "right exactly when B outputs the true LSB. So B's distance from one half equals A's advantage.") as d:
            self.play(FadeIn(alg))
            for x in an:
                self.play(FadeIn(x, shift=0.15 * RIGHT))
                self.wait(d / 9)
        con = tx(r"Non-negligible $\Rightarrow$ $B$ (or its flip, Ex.\ 4.1) beats $\tfrac12 + $negl: contradicts Thm 4.3 $\Rightarrow$ Factoring false. $\blacksquare$", 28, GOOD)
        con.to_edge(DOWN, buff=0.4)
        fit(con, 12.9)
        with self.vo("If A's advantage were non negligible, B or its flipped version would predict the LSB noticeably better "
                     "than half, contradicting theorem four point three, and therefore factoring. So Rabin is IND secure. "
                     "Notice the pattern: matching the input distribution is the heart of every reduction."):
            self.play(FadeIn(con))
        self.clear_all()


class Hybrid5(VScene):
    def construct(self):
        self.header("Longer messages", "Thm 5.4: the hybrid argument")
        cons = VGroup(tx(r"$\mathrm{Enc}'(pk, m_1 m_2 \dots m_\ell) = (\mathrm{Enc}(pk, m_1), \dots, \mathrm{Enc}(pk, m_\ell))$ \ with fresh coins each time", 30),
                      tx(r"\textbf{Thm 5.4:} \ 1-bit $\Pi$ IND secure \ $\Rightarrow$ \ $\ell$-bit $\Pi'$ IND secure.", 32, HL),
                      tx(r"(General IND game: $A$ picks $m_0, m_1$ of \emph{equal length}; ciphertexts can't hide length.)", 26, GREY_A)).arrange(DOWN, buff=0.25)
        cons.to_edge(UP, buff=1.15)
        fit(cons, 12.9)
        with self.vo("One bit at a time is enough. Encrypt a long message bit by bit, with fresh randomness each time. "
                     "Theorem five point four says this is IND secure if the one bit scheme is. In the general game the "
                     "adversary picks two messages, which must have equal length, since ciphertext length can't be hidden."):
            self.play(FadeIn(cons))
        m0, m1 = "0000", "1111"
        rowsv = VGroup()
        for j in range(5):
            s = m1[:j] + m0[j:]
            cells = VGroup()
            for i, ch in enumerate(s):
                col = C4 if i < j else C1
                sq = Square(0.5, stroke_color=col, fill_color=col, fill_opacity=0.25, stroke_width=2)
                cells.add(VGroup(sq, tx(r"$m_1^{%d}$" % (i + 1) if i < j else r"$m_0^{%d}$" % (i + 1), 24, col).move_to(sq)))
            cells.arrange(RIGHT, buff=0.05)
            lab = tx(rf"$\mathrm{{Hyb}}_{j}$" + (r" $= \mathrm{Exp}(0)$" if j == 0 else (r" $= \mathrm{Exp}(1)$" if j == 4 else "")), 28)
            lab.next_to(cells, LEFT, buff=0.35)
            rowsv.add(VGroup(lab, cells))
        rowsv.arrange(DOWN, buff=0.18, aligned_edge=RIGHT).move_to(LEFT * 2.6 + DOWN * 1.35)
        with self.vo("The proof uses hybrids: experiments that slide from one world to the other, one bit at a time. Hybrid "
                     "zero encrypts m zero; that's the real experiment with b equal zero. Hybrid j encrypts the first j bits "
                     "of m one and the rest of m zero. The last hybrid encrypts all of m one.") as d:
            for r in rowsv:
                self.play(FadeIn(r, shift=0.15 * DOWN), run_time=0.6)
                self.wait(d / 9)
        tri = VGroup(M(r"\varepsilon \le |P_0 - P_\ell| \le \sum_{j=0}^{\ell-1} |P_j - P_{j+1}|", font_size=34),
                     tx(r"$\Rightarrow$ some adjacent pair has gap $\ge \varepsilon/\ell$ (non-negligible)", 28),
                     tx(r"$\mathrm{Hyb}_j$, $\mathrm{Hyb}_{j+1}$ differ in \emph{one} bit's encryption $\Rightarrow$ $B_j$ breaks 1-bit $\Pi$:", 28),
                     tx(r"$B_j$ plants its challenge at position $j{+}1$ and encrypts the other bits itself, \emph{using $pk$}.", 28, GOOD)).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        tri.move_to(RIGHT * 3.2 + DOWN * 1.35)
        fit(tri, 6.6)
        with self.vo("If the attacker's success differs by epsilon between the first and last hybrid, the triangle inequality "
                     "says the steps add up to at least epsilon, so some single step has a gap of at least epsilon over ell, "
                     "still non negligible. But adjacent hybrids differ in just one bit's encryption. So an adversary B j "
                     "breaks the one bit scheme: it puts its own challenge ciphertext in position j plus one, and encrypts "
                     "every other bit itself, which it can do because the key is public. Contradiction.") as d:
            for x in tri:
                self.play(FadeIn(x, shift=0.15 * RIGHT))
                self.wait(d / 8)
        self.clear_all()


class Recap5(VScene):
    def construct(self):
        self.header("Part 5", "recap")
        r = recap_list([r"PKE: Gen, Enc (public key, randomized), Dec (secret key); correct with prob.\ 1.",
                        r"Rabin: $(\mathrm{LSB}(r) \oplus m,\ r^2)$ with $r \in QR_N$; decrypt via the principal root.",
                        r"IND: $|\Pr[\hat b = b] - \tfrac12|$ negligible for all PPT $A$; $= \tfrac12|P_0 - P_1|$.",
                        r"Not IND? Give an explicit $A$ and compute its advantage (deterministic Enc fails).",
                        r"Unbounded $A$ always wins: loop over Enc's coins; correctness rules out collisions.",
                        r"Reductions: match the input distribution. Hybrids: change one bit per step."], fs=30)
        fit(r, 12.8).move_to(DOWN * 0.2)
        with self.vo("Recap. Public key encryption: generate keys, encrypt with the public key using randomness, decrypt "
                     "with the secret key. Rabin encrypts a bit by masking it with the LSB of a random residue. IND "
                     "security means no efficient adversary guesses the bit noticeably better than half. To show a scheme "
                     "isn't IND secure, give an explicit adversary and compute its advantage. Deterministic encryption "
                     "always fails. And the proof tools: reductions that match input distributions, and hybrids that "
                     "change one thing at a time.") as d:
            for line in r:
                self.play(FadeIn(line, shift=0.2 * RIGHT), run_time=0.6)
                self.wait(d / 8)
        self.clear_all()
        final = VGroup(tx(r"\textbf{Midterm checklist}", 40, HL),
                       tx(r"Perfectly secret? \ count keys with $\mathrm{Enc}_k(m) = c$; is it independent of $m$?", 30),
                       tx(r"Not perfectly secret? \ Shannon, or a $c$ that $m$ can't hit but $m'$ can.", 30),
                       tx(r"Negligible / PPT? \ fix arbitrary $c$; unpack definitions; mind input \emph{length}.", 30),
                       tx(r"QR questions? \ Euler's criterion + CRT coordinates.", 30),
                       tx(r"Security proof? \ assume $A$, build $B$, match distributions, compare advantages.", 30)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        fit(final, 12.9)
        with self.vo("Your midterm checklist. Proving perfect secrecy: count the keys that send m to c, and check it doesn't "
                     "depend on m. Disproving it: Shannon, or a ciphertext one message can't reach. Negligible or P P T: "
                     "fix an arbitrary c, unpack the definitions, and measure input length. Residue questions: Euler's "
                     "criterion and C R T coordinates. Security proofs: assume an attacker, build a reduction, match the "
                     "distributions, compare advantages. Write your solutions in your own words, and good luck tomorrow.") as d:
            for x in final:
                self.play(FadeIn(x, shift=0.2 * RIGHT))
                self.wait(d / 9)
        self.wait(1.5)
