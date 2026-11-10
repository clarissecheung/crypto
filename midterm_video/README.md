# Midterm review videos (weeks 1-5)

Narrated Manim explainer videos built from `lectures/` and the graded `quizzes/`.

| Folder | Video | Notes chapter |
|---|---|---|
| `ch0` | Part 0: the toolkit | 0 (prerequisites) |
| `ch1` | Part 1: encryption and perfect secrecy | 1 |
| `ch2` | Part 2: PPT, negligible functions, factoring | 2 |
| `ch3` | Part 3: algorithmic number theory | 3 |
| `ch4` | Part 4: hiding one bit (LSB) | 4 |
| `ch5` | Part 5: public-key encryption, Rabin, IND security | 5 |

Each chapter folder holds its scene file (`cN.py`), `scenes.txt` (scene order) and copies of the
pipeline scripts from `shared/` (`./newch.sh chN` refreshes them).

## Rebuild a chapter

```bash
source env.sh ch1            # sets PATH (Manim venv) and EXPLAINER_WORK, cds into ch1
python3 tts_pass.py          # narration audio (Kokoro, offline) + LaTeX pre-compile
python3 render.py --quality mid --budget 0 --jobs 3
python3 assemble.py --quality mid ../out/part1.mp4
```

Requirements: Python 3.11+ venv with `manim kokoro-onnx onnxruntime soundfile scipy`, LaTeX with
`dvisvgm`, ffmpeg, and the Kokoro weights in `~/.cache/explainer-tts` (see `shared/setup.sh`).
