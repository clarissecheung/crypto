"""
pronounce.py — check how Kokoro will say words (you can't listen, but you can read the phonemes).

    python3 pronounce.py "eigenvector" "Hessian" "A times v"

Shows the respelled text (see RESPELL in explainer.py) and its IPA. If a word comes out wrong,
add a (regex, replacement) pair to RESPELL, e.g. (r"\\bLagrangian\\b", "la-GRAHN-jee-un"), and re-check.
Common traps: "eigen" (EYE-jen), a lone capital "A" read as the article "uh", acronyms, and names.
"""
import os
import sys

sys.path.insert(0, os.getcwd())
import explainer  # noqa: E402

k = explainer.kokoro()
for t in sys.argv[1:]:
    say = explainer.spoken(t)
    print(f"{t!r:32} -> {say!r:32} /{k.tokenizer.phonemize(say, 'en-us')}/")
