from cx import *


def channel():
    a = party("Alice", HON).move_to(LEFT * 4.6 + UP * 1.0)
    b = party("Bob", HON).move_to(RIGHT * 4.6 + UP * 1.0)
    e = party("Eve", ADV).move_to(DOWN * 1.6)
    wire = Line(a[0].get_right(), b[0].get_left(), color=GREY_B, stroke_width=3)
    tap = DashedLine(e[0].get_top(), wire.get_center(), color=ADV, stroke_width=2)
    return VGroup(a, b, e, wire, tap)


class Intro1(VScene):
    def construct(self):
        title = tx(r"\textbf{Part 1: Encryption and Perfect Secrecy}", 50, HL).move_to(UP * 0.4)
        sub = tx(r"Week 1 \quad (notes chapter 1)", 32, GREY_A).next_to(title, DOWN)
        with self.vo("Part one: encryption, and our first security definition, perfect secrecy."):
            self.play(Write(title), FadeIn(sub))
        self.play(FadeOut(title), FadeOut(sub))
        self.header("Part 1", "the setting")
        ch = channel()
        with self.vo("Alice wants to send Bob a message. The channel is public, and Eve can read everything on it."):
            self.play(FadeIn(ch[0]), FadeIn(ch[1]), Create(ch[3]))
            self.play(FadeIn(ch[2]), Create(ch[4]))
        m = tx(r"$m$", 40, MSG).next_to(ch[0], UP, buff=0.2)
        enc = chip(r"Enc$_k$", KEY).move_to(LEFT * 2.2 + UP * 1.6)
        c = tx(r"$c$", 40, CT).move_to(ch[3].get_center() + UP * 0.35)
        dec = chip(r"Dec$_k$", KEY).move_to(RIGHT * 2.2 + UP * 1.6)
        m2 = tx(r"$m$", 40, MSG).next_to(ch[1], UP, buff=0.2)
        with self.vo("So Alice encrypts. The plaintext m goes in, and a scrambled ciphertext c comes out. "
                     "Only c travels over the channel. Bob decrypts c to get m back."):
            self.play(FadeIn(m))
            self.play(FadeIn(enc), TransformFromCopy(m, c))
            self.play(FadeIn(dec), TransformFromCopy(c, m2))
        kk = tx(r"key $k$: shared by Alice and Bob, \textbf{unknown to Eve}", 32, KEY).to_edge(DOWN, buff=0.4)
        with self.vo("Bob must know something Eve doesn't. Otherwise Eve could decrypt exactly the way Bob does. "
                     "That secret is the key k."):
            self.play(FadeIn(kk, shift=0.2 * UP))
        self.clear_all()
        kp = VGroup(tx(r"\textbf{Kerckhoffs' principle} (1883)", 38, HL),
                    tx(r"The method may fall into enemy hands. \ Only the \emph{key} is secret.", 34),
                    tx(r"So: Eve knows Enc and Dec. \ She does not know $k$.", 34, GREY_A)).arrange(DOWN, buff=0.35)
        with self.vo("One rule we always follow is Kerckhoffs' principle. Assume the enemy knows exactly how the "
                     "scheme works, the encryption and decryption algorithms. The only secret is the key."):
            self.play(LaggedStart(*[FadeIn(x, shift=0.2 * UP) for x in kp], lag_ratio=0.4))
        self.clear_all()
        three = roadmap([("1. Syntax", "which algorithms, inputs, outputs"),
                         ("2. Correctness", "honest use works"),
                         ("3. Security", "what Eve can't do")], cols=3, w=4.0, h=1.3)
        with self.vo("Defining any cryptographic scheme takes three ingredients. Syntax: which algorithms exist "
                     "and what they take in and put out. Correctness: when used honestly, it works. And security: "
                     "what the adversary can't do. Security is the subtle one."):
            self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in three], lag_ratio=0.4), run_time=2.5)
            self.play(Indicate(three[2], color=HL))
        self.clear_all()


class Syntax1(VScene):
    def construct(self):
        self.header("Symmetric encryption", "syntax and correctness")
        sp = tx(r"Sets: \ messages $\mathcal M$, \ ciphertexts $\mathcal C$, \ keys $\mathcal K$ (finite)", 34).to_edge(UP, buff=1.15)
        enc = tx(r"$\mathrm{Enc}: \mathcal K \times \mathcal M \to \mathcal C$, \quad $c \leftarrow \mathrm{Enc}_k(m)$ \quad (may be randomized)", 32)
        dec = tx(r"$\mathrm{Dec}: \mathcal K \times \mathcal C \to \mathcal M$, \quad $m := \mathrm{Dec}_k(c)$ \quad (deterministic)", 32)
        key = tx(r"keys are always uniform: \ $k \xleftarrow{\$} \mathcal K$", 32, KEY)
        g = VGroup(enc, dec, key).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(sp, DOWN, buff=0.4)
        with self.vo("The syntax. There's a message space, a ciphertext space, and a finite key space. "
                     "Encryption takes a key and a message and outputs a ciphertext, and it may use randomness. "
                     "Decryption takes a key and a ciphertext and outputs a message, deterministically. And the key "
                     "is always chosen uniformly at random.") as d:
            self.play(FadeIn(sp))
            for x in g:
                self.play(FadeIn(x, shift=0.2 * RIGHT))
                self.wait(d / 8)
        cor = M(r"\forall k \in \mathcal K,\ \forall m \in \mathcal M:\quad \Pr\big[\mathrm{Dec}_k(\mathrm{Enc}_k(m)) = m\big] = 1",
                font_size=38, color=HL).next_to(g, DOWN, buff=0.55)
        with self.vo("Correctness says: for every key and every message, decrypting the encryption gives the message "
                     "back, with probability one."):
            self.play(Write(cor), run_time=2)
            self.play(Create(boxed(cor)))
        self.clear_all()
        ex = algo(r"Correct but insecure (Ex.\ 1.3)",
                  [r"$\mathrm{Enc}_k(m) = (k,\ k \oplus m)$", r"$\mathrm{Dec}_k(c_1, c_2) = k \oplus c_2$"], fs=32)
        ex.move_to(LEFT * 3.2 + UP * 0.6)
        with self.vo("Correctness has nothing to do with security. Exercise one point three encrypts by outputting the "
                     "key itself, next to k XOR m."):
            self.play(FadeIn(ex))
        c1 = rows(r"Correct: \ $k \oplus c_2 = k \oplus k \oplus m = m$ \checkmark",
                  r"Insecure: Eve computes $c_1 \oplus c_2 = k \oplus k \oplus m = m$", fs=32, buff=0.4)
        c1.move_to(RIGHT * 2.9 + UP * 0.6)
        fit(c1, 6.4)
        with self.vo("Decryption XORs the key with the second part, and the keys cancel, so it's correct. But Eve can "
                     "do the same thing using the first part of the ciphertext, which is the key. She reads m directly."):
            self.play(FadeIn(c1[0], shift=0.2 * RIGHT))
            self.play(FadeIn(c1[1], shift=0.2 * RIGHT))
            self.play(c1[1].animate.set_color(BAD))
        corr = VGroup(tx(r"\textbf{Proving correctness} (Ex.\ 1.2): \ plug Enc into Dec and simplify", 30, HL),
                      tx(r"SUB: $\varphi^{-1}(\varphi(m_i)) = m_i$ \quad VIG: shift$(\text{shift}(m_i,k_j),-k_j) = m_i$ \quad OTP: $k \oplus (k\oplus m) = m$", 28))
        corr.arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        fit(corr, 12.8)
        with self.vo("And for correctness proofs, like exercise one point two, the recipe is always the same: fix an "
                     "arbitrary key and message, plug encryption into decryption, and simplify until you get m. "
                     "The inverse permutation undoes the permutation, shifting back undoes shifting, and XOR undoes XOR."):
            self.play(FadeIn(corr, shift=0.2 * UP))
        self.clear_all()


class Classic1(VScene):
    def construct(self):
        self.header("Historical ciphers", "and how they break")
        st = tx(r"\textbf{Shift cipher}: \ $\mathcal K = \{0,\dots,25\}$, \ shift every letter by $k$", 34).to_edge(UP, buff=1.15)
        m = bitrow("HELLOWORLD", MSG, size=0.52, fs=30).move_to(UP * 1.1)
        c = bitrow("OLSSVDVYSK", CT, size=0.52, fs=30).next_to(m, DOWN, buff=0.7)
        arrows = VGroup(*[Arrow(a.get_bottom(), b.get_top(), buff=0.06, stroke_width=2, color=KEY, tip_length=0.12)
                          for a, b in zip(m, c)])
        k7 = tx(r"$k=7$", 30, KEY).next_to(arrows, RIGHT, buff=0.3)
        with self.vo("The shift cipher moves every letter forward by k places, wrapping from Z back to A. With key "
                     "seven, HELLOWORLD becomes O L S S V D V Y S K."):
            self.play(FadeIn(st))
            self.play(FadeIn(m))
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.05), FadeIn(k7))
            self.play(FadeIn(c))
        bf = tx(r"Only 26 keys $\Rightarrow$ Eve tries them all (\emph{brute force}); \ one decryption reads as English.", 30, BAD)
        bf.next_to(c, DOWN, buff=0.6)
        with self.vo("It breaks instantly. There are only twenty six keys, so Eve decrypts with every one, and exactly "
                     "one candidate reads as English. Lesson one: the key space must be too large to search."):
            self.play(FadeIn(bf))
        self.clear_all()
        sub = VGroup(tx(r"\textbf{Substitution cipher}: key = a permutation $\varphi$ of the alphabet", 34),
                     M(r"|\mathcal K| = 26! \approx 4 \times 10^{26} \quad (\text{Ex. } 1.1)", font_size=40, color=KEY),
                     tx(r"Still broken: \emph{frequency analysis}. The same letter always maps to the same letter,", 30),
                     tx(r"so the most common ciphertext letter is probably \texttt{E}.", 30)).arrange(DOWN, buff=0.3)
        sub.to_edge(UP, buff=1.15)
        with self.vo("The substitution cipher's key is any rearrangement of the alphabet. How many keys? Twenty six "
                     "choices for where A goes, twenty five for B, and so on: twenty six factorial, about four times "
                     "ten to the twenty six. That's part of exercise one point one.") as d:
            self.play(FadeIn(sub[0]))
            self.play(Write(sub[1]))
        with self.vo("But it's still easy to break, with frequency analysis. Each letter always becomes the same "
                     "letter, so the most common ciphertext letter is probably E. Lesson two: a big key space is "
                     "necessary, but not sufficient."):
            self.play(FadeIn(sub[2]), FadeIn(sub[3]))
        self.clear_all()
        vt = tx(r"\textbf{Vigen\`ere}: key $k = (k_1,\dots,k_\ell)$; \ position $i$ uses shift $k_j$, \ $j = ((i-1) \bmod \ell) + 1$", 32)
        vt.to_edge(UP, buff=1.15)
        fit(vt, 12.8)
        m = bitrow("HELLOWORLD", MSG, size=0.52, fs=30).move_to(UP * 1.2)
        ks = bitrow("1231231231", KEY, size=0.52, fs=30).next_to(m, DOWN, buff=0.2)
        c = bitrow("IGOMQZPTOE", CT, size=0.52, fs=30).next_to(ks, DOWN, buff=0.2)
        lab = VGroup(tx("$m$", 32, MSG).next_to(m, LEFT), tx("shift", 28, KEY).next_to(ks, LEFT), tx("$c$", 32, CT).next_to(c, LEFT))
        with self.vo("The Vigenere cipher uses several shifts in rotation. With key one, two, three, the first letter "
                     "shifts by one, the second by two, the third by three, then the pattern repeats."):
            self.play(FadeIn(vt))
            self.play(FadeIn(m), FadeIn(lab[0]))
            self.play(FadeIn(ks), FadeIn(lab[1]))
            self.play(FadeIn(c), FadeIn(lab[2]))
        cnt = M(r"|\mathcal K| = 26^\ell \quad (\text{Ex. } 1.1)", font_size=40, color=KEY).next_to(c, DOWN, buff=0.5)
        with self.vo("Each of the ell key entries has twenty six choices, so there are twenty six to the ell keys."):
            self.play(Write(cnt))
        hl = VGroup(*[ks[i] for i in (0, 3, 6, 9)])
        weak = tx(r"Weakness: positions $1, 4, 7, 10$ all use the \emph{same} shift $k_1$.", 32, BAD).to_edge(DOWN, buff=0.5)
        with self.vo("Notice the repeated L becomes O, then M, then O again, so simple frequency analysis fails. "
                     "But positions one, four, seven and ten all use the same shift. That's the weakness, and it's "
                     "exactly what the next exam style problem exploits."):
            self.play(*[Indicate(x, color=BAD) for x in hl])
            self.play(FadeIn(weak))
        self.clear_all()


class Vig1(VScene):
    def construct(self):
        self.header("Exam-style", r"Quiz 2 Q1 / Ex.\ 1.5")
        q = VGroup(tx(r"Eve knows Alice sent $m_0 = \texttt{ABCD}$ or $m_1 = \texttt{EFGZ}$, encrypted with Vigen\`ere,", 32),
                   tx(r"key length $\ell \ge 2$. \ For which $\ell$ can Eve determine the message \emph{with certainty}?", 32)).arrange(DOWN, buff=0.15)
        q.to_edge(UP, buff=1.1)
        fit(q, 13)
        with self.vo("Here's quiz two, question one. Eve knows Alice sent either A B C D or E F G Z, using Vigenere "
                     "with some key length ell of at least two. For which ell can Eve tell which message it was, "
                     "with certainty? Think about it for a moment.") as d:
            self.play(FadeIn(q))
        self.wait(2.5)
        key = VGroup(tx(r"\textbf{Key idea:} if positions $i$ and $j$ use the same shift $s$,", 32, HL),
                     M(r"c_j - c_i \equiv (m_j + s) - (m_i + s) \equiv m_j - m_i \pmod{26}", font_size=38),
                     tx(r"The key \emph{cancels}. Eve learns the gap between those two message letters.", 30, GOOD))
        key.arrange(DOWN, buff=0.25).next_to(q, DOWN, buff=0.45)
        with self.vo("The key idea. Suppose two positions use the same shift s. Subtract the two ciphertext letters. "
                     "The s cancels, and what's left is the gap between the two plaintext letters. Eve can compute "
                     "that gap without knowing the key."):
            self.play(FadeIn(key[0]))
            self.play(Write(key[1]), run_time=2)
            self.play(FadeIn(key[2]))
        self.clear_all()

        def letters(s, col):
            return bitrow(s, col, size=0.55, fs=30)
        r0 = letters("ABCD", MSG).move_to(LEFT * 4.2 + UP * 1.6)
        r1 = letters("EFGZ", C4).next_to(r0, DOWN, buff=0.35)
        l0 = tx(r"$m_0$", 30, MSG).next_to(r0, LEFT)
        l1 = tx(r"$m_1$", 30, C4).next_to(r1, LEFT)
        idx = VGroup(*[tx(str(i + 1), 24, GREY_B).next_to(r0[i], UP, buff=0.1) for i in range(4)])
        with self.vo("Letters are numbers: A is zero, B is one, and so on up to Z, twenty five."):
            self.play(FadeIn(r0), FadeIn(r1), FadeIn(l0), FadeIn(l1), FadeIn(idx))
        t2 = VGroup(tx(r"$\ell = 2$: \ positions 2 and 4 share $k_2$", 30, HL),
                    tx(r"$m_0$: \ D $-$ B $= 3 - 1 = 2$", 30, MSG),
                    tx(r"$m_1$: \ Z $-$ F $= 25 - 5 = 20$", 30, C4),
                    tx(r"different $\Rightarrow$ Eve computes $c_4 - c_2$ and \textbf{knows}", 30, GOOD)).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        t2.move_to(RIGHT * 2.6 + UP * 1.4)
        with self.vo("Key length two. Positions two and four share a shift. In m zero, D minus B is two. In m one, "
                     "Z minus F is twenty. Different gaps! So Eve's attack is: compute c four minus c two. If it's "
                     "two, the message was A B C D. If it's twenty, E F G Z. Certain.") as d:
            self.play(FadeIn(t2[0]))
            self.play(Indicate(VGroup(r0[1], r0[3], r1[1], r1[3]), color=HL))
            self.play(FadeIn(t2[1]), FadeIn(t2[2]))
            self.wait(0.15 * d)
            self.play(FadeIn(t2[3]))
        t3 = VGroup(tx(r"$\ell = 3$: \ positions 1 and 4 share $k_1$", 30, HL),
                    tx(r"$m_0$: \ D $-$ A $= 3$ \qquad $m_1$: \ Z $-$ E $= 21$", 30),
                    tx(r"different $\Rightarrow$ Eve \textbf{knows}", 30, GOOD)).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        t3.next_to(t2, DOWN, buff=0.45, aligned_edge=LEFT)
        with self.vo("Key length three. Now positions one and four share a shift. D minus A is three, Z minus E is "
                     "twenty one. Different again, so Eve knows."):
            self.play(FadeIn(t3[0]))
            self.play(Indicate(VGroup(r0[0], r0[3], r1[0], r1[3]), color=HL))
            self.play(FadeIn(t3[1]), FadeIn(t3[2]))
        t4 = VGroup(tx(r"$\ell \ge 4$: each position has", 30, HL),
                    tx(r"its \emph{own} uniform shift", 30, HL),
                    tx(r"every $c_i$ is uniform either way", 30, BAD),
                    tx(r"$\Rightarrow$ Eve \textbf{can't} tell", 30, BAD)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        t4.next_to(VGroup(r0, r1, l0, l1), DOWN, buff=0.7).align_to(l0, LEFT)
        with self.vo("Key length four or more. Then a four letter message never reuses a shift. Each ciphertext letter is "
                     "its message letter plus its own independent uniform shift, so it's uniformly random either "
                     "way. Both messages produce exactly the same ciphertext distribution, and Eve can't do better "
                     "than guessing."):
            self.play(FadeIn(t4))
        ans = tx(r"Answer: $\ell \in \{2, 3\}$", 38, HL).to_edge(DOWN, buff=0.45).shift(RIGHT * 3.2)
        with self.vo("So the answer is ell equals two or three."):
            self.play(Write(ans), Create(boxed(ans)))
        self.clear_all()
        notes = VGroup(tx(r"Notes' version (Ex.\ 1.5): \ $\texttt{ABCD}$ vs.\ $\texttt{AKTD}$", 34, HL),
                       tx(r"$\ell = 2$: \ positions 1, 3: \ C$-$A $= 2$ \ vs.\ T$-$A $= 19$ \ $\Rightarrow$ knows", 30),
                       tx(r"$\ell = 3$: \ positions 1, 4: \ D$-$A $= 3$ \ vs.\ D$-$A $= 3$ \ $\Rightarrow$ same gap, \textbf{can't}", 30),
                       tx(r"$\ell \ge 4$: can't. \qquad Answer: only $\ell = 2$", 30, HL)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        with self.vo("Same method, different numbers: the notes' version uses A B C D versus A K T D. With key length "
                     "two, positions one and three give gaps two versus nineteen, so Eve knows. With key length three, "
                     "positions one and four give three versus three. Same gap, so no information, and positions two "
                     "and three are hidden by their own shifts. Only ell equals two works.") as d:
            for x in notes:
                self.play(FadeIn(x, shift=0.2 * RIGHT))
                self.wait(d / 7)
        fb = tx(r"Grader's note: say \emph{how} Eve uses the shared shift --- give the actual test.", 30, BAD).to_edge(DOWN, buff=0.5)
        with self.vo("The grader's comment on the quiz was: how does the attacker use this fact? So always write the "
                     "actual test: compute this ciphertext difference, compare it to the two possible message gaps."):
            self.play(FadeIn(fb))
        self.clear_all()


class PS1(VScene):
    def construct(self):
        self.header("Perfect secrecy", "Shannon, 1949")
        prior = VGroup(tx(r"Eve's \textbf{prior} beliefs about the message $M$:", 32),
                       M(r"\texttt{SEL NVDA}: \tfrac13 \qquad \texttt{BUY NVDA}: \tfrac12 \qquad \texttt{BUY AAPL}: \tfrac16", font_size=36, color=MSG))
        prior.arrange(DOWN, buff=0.25).to_edge(UP, buff=1.15)
        with self.vo("In nineteen forty nine, Claude Shannon gave the first mathematical definition of security. "
                     "Start with what Eve believes before seeing anything. Say Alice's message is sell NVIDIA with "
                     "probability one third, buy NVIDIA one half, buy Apple one sixth. That's the prior."):
            self.play(FadeIn(prior[0]))
            self.play(Write(prior[1]), run_time=2)
        seen = VGroup(tx(r"Eve sees the substitution-cipher ciphertext \ $c = \texttt{WNX TTAD}$", 32, CT),
                      tx(r"repeated letter \texttt{TT} $\Rightarrow$ the message has a repeated letter $\Rightarrow$ \texttt{BUY AAPL}", 30),
                      M(r"\textbf{posterior: } \Pr[M = \texttt{BUY AAPL} \mid c] = 1 \neq \tfrac16", font_size=36, color=BAD)).arrange(DOWN, buff=0.3)
        seen.next_to(prior, DOWN, buff=0.6)
        with self.vo("Now Eve sees a substitution cipher ciphertext, W N X, T T A D. Any substitution maps equal letters "
                     "to equal letters, so a repeated T in the ciphertext means a repeated letter in the message. Only "
                     "buy Apple has one. Eve's belief, the posterior, jumped from one sixth to one. The ciphertext "
                     "leaked information.") as d:
            self.play(FadeIn(seen[0]))
            self.play(FadeIn(seen[1]))
            self.play(Write(seen[2]))
        self.clear_all()
        dfn = VGroup(tx(r"\textbf{Definition (perfect secrecy).} For every distribution of $M$, every $m$, every $c$:", 32, HL),
                     M(r"\Pr[M = m \mid \mathrm{Enc}_k(M) = c] \;=\; \Pr[M = m]", font_size=44),
                     tx(r"(or $\Pr[\mathrm{Enc}_k(M) = c] = 0$, \ when $c$ can never appear)", 28, GREY_B)).arrange(DOWN, buff=0.4)
        with self.vo("Perfect secrecy demands that never happens. For every possible message distribution, every "
                     "message, and every ciphertext that can occur, the posterior equals the prior. Seeing the "
                     "ciphertext changes nothing about what Eve believes.") as d:
            self.play(FadeIn(dfn[0]))
            self.play(Write(dfn[1]), run_time=2)
            self.play(FadeIn(dfn[2]))
            self.play(Create(boxed(dfn[1])))
        self.clear_all()


class Ex16(VScene):
    def construct(self):
        self.header("Exam-style", r"Ex.\ 1.6 (posteriors)")
        q = tx(r"Same prior, substitution cipher, \ $c = \texttt{NCO QPEZ}$. \ Find each posterior.", 34).to_edge(UP, buff=1.15)
        with self.vo("Exercise one point six. Same prior, same cipher, but now the ciphertext is N C O, Q P E Z. "
                     "Find each message's posterior probability."):
            self.play(FadeIn(q))
        s1 = rows(r"$c$ has 7 \emph{distinct} letters. \ \texttt{BUY AAPL} repeats A $\Rightarrow$ impossible: posterior $0$.",
                  r"\texttt{SEL NVDA}, \texttt{BUY NVDA}: 7 distinct letters each.",
                  r"A uniform permutation sends them to $c$ with the \emph{same} probability $q = \tfrac{1}{26\cdot25\cdots20}$.",
                  fs=30, buff=0.3).next_to(q, DOWN, buff=0.5)
        fit(s1, 12.8)
        with self.vo("Step one: which messages are even possible? The ciphertext has seven different letters. Buy "
                     "Apple has a repeated A, which would produce a repeated letter, so it's impossible. Its "
                     "posterior is zero.") as d:
            self.play(FadeIn(s1[0]))
        with self.vo("The other two messages each have seven distinct letters. Then a random permutation sends them to "
                     "this exact ciphertext with the same small probability. Call it q. The exact value won't matter."):
            self.play(FadeIn(s1[1]))
            self.play(FadeIn(s1[2]))
        tot = M(r"\Pr[\mathrm{Enc}_k(M) = c] = \tfrac13 q + \tfrac12 q + \tfrac16\cdot 0 = \tfrac56 q", font_size=38).next_to(s1, DOWN, buff=0.45)
        with self.vo("Total probability gives the chance of seeing c: one third q, plus one half q, plus zero, which "
                     "is five sixths q. That's part a."):
            self.play(Write(tot))
        post = M(r"\Pr[\texttt{SEL NVDA}\mid c] = \frac{\tfrac13 q}{\tfrac56 q} = \tfrac25 \qquad \Pr[\texttt{BUY NVDA}\mid c] = \frac{\tfrac12 q}{\tfrac56 q} = \tfrac35",
                 font_size=36, color=HL).next_to(tot, DOWN, buff=0.45)
        fit(post, 12.8)
        with self.vo("Bayes for parts b and c: each posterior is prior times q, divided by five sixths q. The q's "
                     "cancel. Sell NVIDIA goes from one third to two fifths, and buy NVIDIA from one half to three fifths."):
            self.play(Write(post), run_time=2)
            self.play(Create(boxed(post)))
        punch = tx(r"Posteriors $\ne$ priors $\Rightarrow$ substitution is \textbf{not} perfectly secret.", 32, BAD).to_edge(DOWN, buff=0.4)
        with self.vo("The posteriors differ from the priors, so once again, the substitution cipher is not perfectly secret."):
            self.play(FadeIn(punch))
        self.clear_all()


class PI1(VScene):
    def construct(self):
        self.header("Perfect indistinguishability", "the usable form")
        prob = tx(r"``For every distribution of $M$'' is hard to work with. \ Shannon's equivalent condition:", 32).to_edge(UP, buff=1.15)
        fit(prob, 12.8)
        dfn = M(r"\forall m_1, m_2 \in \mathcal M,\ \forall c:\qquad \Pr_k[\mathrm{Enc}_k(m_1) = c] = \Pr_k[\mathrm{Enc}_k(m_2) = c]",
                font_size=40, color=HL).next_to(prob, DOWN, buff=0.5)
        with self.vo("Checking every distribution of messages is painful. Shannon gave an equivalent condition that's "
                     "much easier. Perfect indistinguishability: for any two messages and any ciphertext, the two "
                     "messages produce that ciphertext with exactly the same probability, over a random key."):
            self.play(FadeIn(prob))
            self.play(Write(dfn), run_time=2.5)
        thm = tx(r"\textbf{Theorem 1.1:} \ perfectly secret \ $\iff$ \ perfectly indistinguishable", 36, GOOD).next_to(dfn, DOWN, buff=0.55)
        with self.vo("Theorem one point one says the two definitions are equivalent."):
            self.play(FadeIn(thm))
        why = VGroup(M(r"\Pr[M{=}m \mid c] = \Pr[M{=}m]\cdot \frac{\Pr[\mathrm{Enc}_k(m) = c]}{\Pr[\mathrm{Enc}_k(M) = c]}", font_size=36),
                     tx(r"denominator = weighted average of the numbers $\Pr[\mathrm{Enc}_k(m') = c]$; \ if they're all equal, ratio $= 1$", 28, GREY_A))
        why.arrange(DOWN, buff=0.25).next_to(thm, DOWN, buff=0.45)
        fit(why, 12.8)
        with self.vo("Why? Bayes' rule says the posterior is the prior times a ratio. The bottom of that ratio is an "
                     "average of the probabilities that each message produces c. If all of those are equal, the "
                     "average equals each one, the ratio is one, and the posterior equals the prior."):
            self.play(Write(why[0]), run_time=2)
            self.play(FadeIn(why[1]))
        self.clear_all()
        recipe = VGroup(tx(r"\textbf{Proof recipe for ``prove $\Pi$ is perfectly secret''}", 36, HL),
                        tx(r"1. \ Fix arbitrary $m \in \mathcal M$ and $c \in \mathcal C$.", 32),
                        tx(r"2. \ Compute $\Pr_k[\mathrm{Enc}_k(m) = c]$ exactly (usually: count keys that work).", 32),
                        tx(r"3. \ Show the answer does \textbf{not depend on $m$}.", 32),
                        tx(r"4. \ Conclude perfect indistinguishability, so perfect secrecy by Theorem 1.1.", 32)).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        with self.vo("That gives the recipe for any prove this is perfectly secret question. Fix an arbitrary message "
                     "and ciphertext. Compute the probability the message encrypts to that ciphertext, usually by "
                     "counting keys. Show the answer doesn't depend on the message. Then conclude perfect "
                     "indistinguishability, and hence perfect secrecy.") as d:
            for x in recipe:
                self.play(FadeIn(x, shift=0.2 * RIGHT))
                self.wait(d / 9)
            self.play(Create(boxed(recipe)))
        self.clear_all()


class OTP1(VScene):
    def construct(self):
        self.header("One-time pad", r"$\mathcal M = \mathcal C = \mathcal K = \{0,1\}^\ell$")
        enc = M(r"\mathrm{Enc}_k(m) = k \oplus m \qquad \mathrm{Dec}_k(c) = k \oplus c", font_size=44).to_edge(UP, buff=1.15)
        with self.vo("The one time pad. Messages, ciphertexts and keys are all ell bit strings. Encrypt by XOR with the "
                     "key, decrypt by XOR with the key again. Correctness is the XOR rule: the key cancels."):
            self.play(Write(enc), run_time=2)
        q = qframe(r"Quiz 2 Q2 / Ex.\ 1.7: \ Prove OTP$_\ell$ is perfectly secret.", 36).next_to(enc, DOWN, buff=0.4)
        with self.vo("Quiz two, question two: prove it's perfectly secret. Use the recipe."):
            self.play(FadeIn(q))
        m = bitrow("101", MSG, size=0.5).move_to(LEFT * 4.6 + DOWN * 0.3)
        c = bitrow("110", CT, size=0.5).next_to(m, DOWN, buff=0.35)
        lm = tx("$m$", 30, MSG).next_to(m, LEFT)
        lc = tx("$c$", 30, CT).next_to(c, LEFT)
        keys = ["000", "001", "010", "011", "100", "101", "110", "111"]
        kg = VGroup(*[bitrow(s, KEY, size=0.36, fs=22) for s in keys]).arrange_in_grid(rows=2, buff=(0.35, 0.3))
        kg.move_to(RIGHT * 2.2 + DOWN * 0.7)
        kl = tx(r"all $2^3 = 8$ keys, each with probability $\tfrac18$", 28, KEY).next_to(kg, UP, buff=0.25)
        with self.vo("Step one: fix any message and any ciphertext. Here's an example with three bits: m is one zero "
                     "one, c is one one zero. On the right are all eight possible keys."):
            self.play(FadeIn(m), FadeIn(c), FadeIn(lm), FadeIn(lc))
            self.play(FadeIn(kg), FadeIn(kl))
        target = bitrow("011", HL, size=0.36, fs=22).move_to(kg[3])
        eq = M(r"k \oplus m = c \iff k = m \oplus c = 011", font_size=36).next_to(c, DOWN, buff=0.45).align_to(lm, LEFT)
        with self.vo("Step two: count the keys that work. XOR both sides with m: k XOR m equals c exactly when k "
                     "equals m XOR c. That's one specific key, zero one one. Every other key gives a different "
                     "ciphertext.") as d:
            self.play(Write(eq))
            self.play(kg.animate.set_opacity(0.3), run_time=0.6)
            self.play(Transform(kg[3], target))
        res = M(r"\Pr_k[\mathrm{Enc}_k(m) = c] = \Pr_k[k = m\oplus c] = \frac{1}{2^\ell}", font_size=38, color=HL).to_edge(DOWN, buff=0.5)
        with self.vo("So the probability is one over the number of keys: one over two to the ell. Step three: that "
                     "number does not mention m at all. It's the same for every message."):
            self.play(Write(res))
            self.play(Create(boxed(res)))
        self.clear_all()
        proof = VGroup(tx(r"\textbf{Proof.} Let $m, c \in \{0,1\}^\ell$ be arbitrary. Since $k \xleftarrow{\$} \{0,1\}^\ell$ is uniform,", 32),
                       M(r"\Pr_k[\mathrm{Enc}_k(m) = c] = \Pr_k[k \oplus m = c] = \Pr_k[k = c \oplus m] = 2^{-\ell},", font_size=38),
                       tx(r"because exactly one key, $c \oplus m$, satisfies the equation. This holds for every $m$,", 32),
                       tx(r"so for all $m_1, m_2, c$: \ $\Pr[\mathrm{Enc}_k(m_1)=c] = 2^{-\ell} = \Pr[\mathrm{Enc}_k(m_2)=c]$.", 32),
                       tx(r"That is perfect indistinguishability, so OTP is perfectly secret by Theorem 1.1. \ $\blacksquare$", 32)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        fit(proof, 12.9)
        with self.vo("Here's the write up you'd hand in. Fix arbitrary m and c. The key is uniform. Encrypting m gives c "
                     "exactly when k equals c XOR m, a single key, so the probability is two to the minus ell. Since "
                     "that's true for every message, any two messages hit c with equal probability. That's perfect "
                     "indistinguishability, and Theorem one point one finishes the job.") as d:
            for x in proof:
                self.play(FadeIn(x, shift=0.15 * RIGHT))
                self.wait(d / 8)
        fb = tx(r"Quiz feedback: prove \emph{indistinguishability} (unique key) --- don't argue ``$c$ is random''.", 30, BAD).to_edge(DOWN, buff=0.35)
        with self.vo("On the quiz, the answer tried to argue from the definition of perfect secrecy, saying c is random. "
                     "The grader wanted exactly this: a unique key, so equal probabilities, so indistinguishability."):
            self.play(FadeIn(fb))
        self.clear_all()


class OTPLim1(VScene):
    def construct(self):
        self.header("One-time pad", "limits")
        lim = VGroup(tx(r"\textbf{1. Long keys:} \ $|k| = |m|$. \ The key must be shared in advance.", 32),
                     tx(r"\textbf{2. Never reuse a key:} \ $c_1 \oplus c_2 = (k\oplus m_1)\oplus(k \oplus m_2) = m_1 \oplus m_2$", 32),
                     tx(r"\textbf{3. Malleable:} \ $c \oplus \Delta$ decrypts to $m \oplus \Delta$ (Eve flips bits blindly)", 32)).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        lim.to_edge(UP, buff=1.2)
        fit(lim, 12.8)
        with self.vo("Three limits of the one time pad. One: the key is as long as the message, and has to be shared "
                     "ahead of time. Two: never reuse a key. XOR two ciphertexts made with the same key, and the key "
                     "cancels, leaving m one XOR m two. Three: it's malleable. Eve can XOR any pattern into the "
                     "ciphertext, and the same pattern lands in the plaintext, without her knowing either.") as d:
            for x in lim:
                self.play(FadeIn(x, shift=0.2 * RIGHT))
                self.wait(d / 6)
        self.play(lim.animate.set_opacity(0.35))
        q = tx(r"Ex.\ 1.8(a): same 8-bit key, letters or space. \ $C_1 = \texttt{10110111}$, $C_2 = \texttt{11100111}$", 30, HL)
        q.next_to(lim, DOWN, buff=0.45)
        fit(q, 12.8)
        with self.vo("Exercise one point eight shows the reuse attack. Two ASCII characters, letters or spaces, "
                     "encrypted with the same eight bit key."):
            self.play(FadeIn(q))
        sol = VGroup(tx(r"$C_1 \oplus C_2 = m_1 \oplus m_2 = \texttt{01010000}$", 30),
                     tx(r"ASCII: letters start \texttt{01}, \ space $= \texttt{00100000}$ starts \texttt{00}", 30),
                     tx(r"two letters $\Rightarrow$ XOR starts \texttt{00}; \ ours starts \texttt{01} $\Rightarrow$ one is a \textbf{space}", 30),
                     tx(r"other $= \texttt{00100000} \oplus \texttt{01010000} = \texttt{01110000} = $ `\texttt{p}'", 30, HL)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        sol.next_to(q, DOWN, buff=0.35)
        fit(sol, 12.8)
        with self.vo("XOR the ciphertexts: the key cancels and we get m one XOR m two, zero one zero one zero zero zero "
                     "zero. Now the trick: in ASCII, every letter starts with zero one, and the space is zero zero one "
                     "zero zero zero zero zero. Two letters would XOR to something starting zero zero. Ours starts zero "
                     "one, so exactly one character is a space. The other is space XOR this pattern, which is a "
                     "lower case p.") as d:
            for x in sol:
                self.play(FadeIn(x, shift=0.15 * RIGHT))
                self.wait(d / 7)
            self.play(Create(boxed(sol[3])))
        self.clear_all()


class Shannon1(VScene):
    def construct(self):
        self.header("Shannon's theorem", "long keys are unavoidable")
        thm = tx(r"\textbf{Theorem 1.3:} \ correct $+$ perfectly secret \ $\Rightarrow$ \ $|\mathcal K| \ge |\mathcal M|$", 38, HL).to_edge(UP, buff=1.15)
        with self.vo("Is the long key just a flaw of the one time pad? No. Shannon's theorem says any correct, perfectly "
                     "secret scheme needs at least as many keys as messages."):
            self.play(Write(thm))
        cstar = Dot(LEFT * 4.5 + DOWN * 0.6, radius=0.12, color=CT)
        cl = tx(r"$c^*$", 34, CT).next_to(cstar, LEFT)
        msgs = VGroup(*[Dot(RIGHT * 2.5 + UP * (1.2 - 0.6 * i), color=MSG) for i in range(6)])
        ml = VGroup(*[tx(f"$m_{i + 1}$", 26, MSG).next_to(d, RIGHT) for i, d in enumerate(msgs)])
        lines = VGroup(*[Line(cstar.get_center(), d.get_center(), color=KEY, stroke_width=2) for d in msgs])
        klab = VGroup(*[tx(f"$k_{i + 1}$", 24, KEY).move_to(l.point_from_proportion(0.78) + UP * 0.17) for i, l in enumerate(lines)])
        with self.vo("Fix one ciphertext c star that can actually occur. By perfect indistinguishability, every message "
                     "must be able to encrypt to c star, with the same positive probability.") as d:
            self.play(FadeIn(cstar), FadeIn(cl))
            self.play(FadeIn(msgs), FadeIn(ml))
        with self.vo("Correctness means decrypting c star with a key that produced it from m gives back m. And each key "
                     "decrypts c star to just one message, because decryption is deterministic. So every message needs "
                     "its own key."):
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.15), FadeIn(klab))
        res = tx(r"distinct messages need distinct keys $\Rightarrow |\mathcal M| \le |\mathcal K|$", 34, GOOD).to_edge(DOWN, buff=0.6)
        with self.vo("Different messages need different keys, so there are at least as many keys as messages."):
            self.play(FadeIn(res))
        self.clear_all()
        use = VGroup(tx(r"\textbf{Use it as a one-line disproof:}", 34, HL),
                     tx(r"if $|\mathcal K| < |\mathcal M|$, the scheme is \textbf{not} perfectly secret (if correct).", 34)).arrange(DOWN, buff=0.3)
        with self.vo("On an exam this is a one line disproof. If a correct scheme has fewer keys than messages, it is not "
                     "perfectly secret, by Shannon's theorem. Done."):
            self.play(FadeIn(use))
        self.clear_all()


class NotPS1(VScene):
    def construct(self):
        self.header("Exam-style", "proving NOT perfectly secret")
        rec = VGroup(tx(r"\textbf{Two ways to show $\Pi$ is not perfectly secret}", 36, HL),
                     tx(r"\textbf{A.} \ $|\mathcal K| < |\mathcal M|$ $\Rightarrow$ Shannon's theorem. \ One line.", 32),
                     tx(r"\textbf{B.} \ Find $m, m', c$ with \ $\Pr[\mathrm{Enc}_k(m) = c] = 0$ \ but \ $\Pr[\mathrm{Enc}_k(m') = c] > 0$.", 32),
                     tx(r"\qquad That breaks perfect indistinguishability, so not perfectly secret.", 30, GREY_A)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        with self.vo("Now the opposite kind of question: show a scheme is not perfectly secret. Two tools. One: if there "
                     "are fewer keys than messages, cite Shannon. Two: find a ciphertext that one message can never "
                     "produce, but another message can. That's the strategy the grader recommended on quiz two.") as d:
            for x in rec:
                self.play(FadeIn(x, shift=0.2 * RIGHT))
                self.wait(d / 7)
        self.clear_all()
        q = tx(r"Quiz 3 Q1 / Ex.\ 1.14: \ $\mathrm{Enc}_k(m) = [m + k \bmod 3]$. \ Perfectly secret?", 34, HL).to_edge(UP, buff=1.1)
        with self.vo("Quiz three, question one, which is exercise one point fourteen. Encrypt by adding the key mod three. "
                     "Four versions."):
            self.play(FadeIn(q))

        def table(Ms, Ks):
            rows_ = [[M(r"m \backslash k", font_size=32)] + [M(str(k), font_size=34, color=KEY) for k in Ks]]
            for m in Ms:
                rows_.append([M(str(m), font_size=34, color=MSG)] + [M(str((m + k) % 3), font_size=34, color=CT) for k in Ks])
            g = VGroup(*[x for r in rows_ for x in r]).arrange_in_grid(rows=len(rows_), cols=len(Ks) + 1, buff=(0.4, 0.22))
            return g, rows_
        parts = [((0, 1), (0, 1), r"(a) $\mathcal M{=}\{0,1\}, \mathcal K{=}\{0,1\}$",
                  r"$m{=}1$ never gives $c{=}0$,\\ $m{=}0$ does $\Rightarrow$ \textbf{not} PS", BAD),
                 ((0, 1, 2), (0, 1, 2), r"(b) $\mathcal M{=}\{0,1,2\}, \mathcal K{=}\{0,1,2\}$",
                  r"each $m$ hits each $c$\\ w.p.\ $\tfrac13$ $\Rightarrow$ \textbf{PS}", GOOD),
                 ((0, 1), (0, 1, 2), r"(c) $\mathcal M{=}\{0,1\}, \mathcal K{=}\{0,1,2\}$",
                  r"each $m$ hits each $c$\\ w.p.\ $\tfrac13$ $\Rightarrow$ \textbf{PS}", GOOD),
                 ((0, 1, 2), (0, 1), r"(d) $\mathcal M{=}\{0,1,2\}, \mathcal K{=}\{0,1\}$",
                  r"$|\mathcal K| = 2 < 3 = |\mathcal M|$\\ $\Rightarrow$ Shannon: \textbf{not} PS", BAD)]
        cells = VGroup()
        for i, (Ms, Ks, ttl, verdict, col) in enumerate(parts):
            g, _ = table(Ms, Ks)
            t = tx(ttl, 30)
            v = tx(verdict, 28, col)
            cell = VGroup(t, g, v).arrange(DOWN, buff=0.22)
            cells.add(cell)
        cells.arrange(RIGHT, buff=0.45, aligned_edge=UP).next_to(q, DOWN, buff=0.6)
        fit(cells, 13.2, 5.6)
        narr = [
            "Part a: messages and keys are both zero or one. Make the table of ciphertexts. Message one never produces "
            "ciphertext zero, but message zero does, half the time. So here's a ciphertext one message can't make and another "
            "can: not perfectly secret.",
            "Part b: three messages, three keys. Every row of the table contains zero, one and two exactly once, so "
            "each message hits each ciphertext with probability one third. That doesn't depend on the message: "
            "perfectly secret.",
            "Part c: two messages, three keys. Same thing, each row hits every ciphertext once out of three keys. "
            "Perfectly secret. Fewer messages than keys is fine.",
            "Part d: three messages but only two keys. Shannon's theorem, one line: not perfectly secret.",
        ]
        for cell, text in zip(cells, narr):
            with self.vo(text):
                self.play(FadeIn(cell[0]), FadeIn(cell[1]))
                self.play(FadeIn(cell[2]))
        self.clear_all()


class NotPS1b(VScene):
    def construct(self):
        self.header("Exam-style", r"Ex.\ 1.10, 1.13, 1.15")
        a = VGroup(tx(r"\textbf{1.10(a)} \ OTP but never use the key $0^\ell$: \ $|\mathcal K'| = 2^\ell - 1 < 2^\ell = |\mathcal M|$", 30),
                   tx(r"$\Rightarrow$ not perfectly secret by Shannon. \ (One line!)", 30, BAD)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        b = VGroup(tx(r"\textbf{1.10(b)} \ also remove message $0^\ell$: \ now $|\mathcal K''| = |\mathcal M''|$, Shannon is silent.", 30),
                   tx(r"Key $\ne 0^\ell$ $\Rightarrow$ $c = m \oplus k \ne m$: \ $\Pr[\mathrm{Enc}_k(m) = m] = 0$", 30),
                   tx(r"but for $m' \ne m$: \ $\Pr[\mathrm{Enc}_k(m') = m] = \Pr[k = m \oplus m'] = \tfrac{1}{2^\ell - 1} > 0$", 30),
                   tx(r"$\Rightarrow$ not perfectly secret (method B). \ (Needs $\ell \ge 2$ so that $m' \neq m$ exists.)", 30, BAD)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        g = VGroup(a, b).arrange(DOWN, buff=0.5, aligned_edge=LEFT).to_edge(UP, buff=1.15)
        fit(g, 12.9)
        with self.vo("Exercise one point ten. Part a: the one time pad, but we forbid the all zero key. Now there's one "
                     "fewer key than messages. Shannon, one line, not perfectly secret."):
            self.play(FadeIn(a))
        with self.vo("Part b also removes the all zero message, so keys and messages are equally many, and Shannon says "
                     "nothing. Use method B. Since the key is never zero, the ciphertext is never equal to the message, "
                     "so the probability that m encrypts to m is zero. But a different message m prime encrypts to m "
                     "when the key is m XOR m prime, which is a nonzero, allowed key, so that probability is positive. "
                     "Not perfectly secret. One small caveat: this needs at least two messages, so ell at least two.") as d:
            for x in b:
                self.play(FadeIn(x, shift=0.15 * RIGHT))
                self.wait(d / 8)
        self.play(g.animate.set_opacity(0.3))
        c = VGroup(tx(r"\textbf{1.13} \ messages end in $0$, \ $\mathrm{Enc}_k(m) = m \oplus (k \Vert 0)$: \ it's an OTP on the first $\ell{-}1$ bits", 30),
                   tx(r"$\Pr[\mathrm{Enc}_k(m) = c] = 2^{-(\ell-1)}$ if $c$ ends in 0 (else 0), \ same for every $m$ $\Rightarrow$ \textbf{PS}", 30, GOOD),
                   tx(r"\textbf{1.15(a)} \ variable-length messages, pad $k_{1:|m|}\oplus m$: \ $|c| = |m|$ leaks the length", 30),
                   tx(r"$\Pr[\mathrm{Enc}(\texttt{0}) = \texttt{0}] = \tfrac12$ \ but \ $\Pr[\mathrm{Enc}(\texttt{00}) = \texttt{0}] = 0$ $\Rightarrow$ \textbf{not} PS", 30, BAD)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        c.next_to(g, DOWN, buff=0.4)
        fit(c, 12.9)
        with self.vo("Two more. Exercise one point thirteen: messages always end in zero, and we XOR with the key followed "
                     "by a zero. That's just a one time pad on the first ell minus one bits. Any possible ciphertext "
                     "comes from exactly one key, for every message, so it's perfectly secret."):
            self.play(FadeIn(c[0]), FadeIn(c[1]))
        with self.vo("Exercise one point fifteen a: messages of different lengths, padded with a prefix of the key. "
                     "The ciphertext has the same length as the message, so it leaks the length. So a one bit message can "
                     "encrypt to the string zero, but a two bit message never can. Method B: not perfectly secret."):
            self.play(FadeIn(c[2]), FadeIn(c[3]))
        self.clear_all()


class Recap1(VScene):
    def construct(self):
        self.header("Part 1", "recap")
        r = recap_list([r"Scheme = syntax + correctness + security. Correct $\ne$ secure.",
                        r"Vigen\`ere: positions $\equiv \bmod \ell$ share a shift; $c_j - c_i = m_j - m_i$ leaks.",
                        r"Perfect secrecy: posterior $=$ prior for every distribution.",
                        r"Prove PS via indistinguishability: $\Pr_k[\mathrm{Enc}_k(m) = c]$ independent of $m$.",
                        r"OTP: unique key $c \oplus m$ $\Rightarrow 2^{-\ell}$. Never reuse the key.",
                        r"Not PS: Shannon ($|\mathcal K| < |\mathcal M|$) or a $c$ that $m$ can't hit but $m'$ can."], fs=30)
        fit(r, 12.8).move_to(DOWN * 0.2)
        with self.vo("Recap. Every scheme needs syntax, correctness and security, and correct doesn't mean secure. In "
                     "Vigenere, positions that share a shift leak the gap between message letters. Perfect secrecy "
                     "means the posterior equals the prior. To prove it, show the probability of hitting each "
                     "ciphertext doesn't depend on the message. The one time pad does this with a unique key, as long "
                     "as the key is never reused. And to disprove it, use Shannon's theorem or find a ciphertext one "
                     "message can't produce but another can.") as d:
            for line in r:
                self.play(FadeIn(line, shift=0.2 * RIGHT), run_time=0.6)
                self.wait(d / 8)
        nxt = tx(r"Next: Part 2 --- efficient algorithms, negligible functions, factoring", 32, HL).to_edge(DOWN, buff=0.4)
        with self.vo("Perfect secrecy needs keys as long as messages, which is impractical. Next, in part two, we trade "
                     "it for security against efficient attackers."):
            self.play(FadeIn(nxt))
        self.wait(1)
