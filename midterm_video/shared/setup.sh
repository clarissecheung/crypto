#!/bin/bash
# setup.sh — install the explainer-video toolchain. Idempotent; run each step in its own shell call
# (each finishes in well under 3 minutes):
#
#   bash setup.sh check    # what's installed / missing
#   bash setup.sh manim    # Manim CE (works around missing pango headers in locked-down sandboxes)
#   bash setup.sh latex    # only if latex/dvisvgm are missing: user-local TinyTeX + Manim's packages
#   bash setup.sh tts      # Kokoro offline TTS + model weights (~95 MB) into $KOKORO_DIR
#
# Works without sudo. Network needed: PyPI, plus npm registry or GitHub for weights/headers.
set -u
export PATH="$HOME/.local/bin:$PATH"
for d in "$HOME"/Library/TinyTeX/bin/* "$HOME"/.TinyTeX/bin/*; do [ -d "$d" ] && export PATH="$PATH:$d"; done
KOKORO_DIR="${KOKORO_DIR:-$HOME/.cache/explainer-tts}"
PIP="python3 -m pip install -q --break-system-packages"
$PIP --help >/dev/null 2>&1 || PIP="python3 -m pip install -q"   # older pip without that flag
SHA_MODEL=fbae9257e1e05ffc727e951ef9b9c98418e6d79f1c9b6b13bd59f5c9028a1478

have_py() { python3 -c "import $1" >/dev/null 2>&1; }
sha() { (sha256sum "$1" 2>/dev/null || shasum -a 256 "$1" 2>/dev/null) | cut -d' ' -f1; }

check() {
  echo "python      : $(python3 --version 2>&1)"
  for b in ffmpeg latex dvisvgm; do printf "%-12s: %s\n" "$b" "$(command -v $b || echo MISSING)"; done
  for m in manim kokoro_onnx soundfile numpy scipy; do
    printf "%-12s: %s\n" "$m" "$(have_py $m && echo ok || echo MISSING)"; done
  for f in kokoro-q8.onnx voices.npz; do
    printf "%-12s: %s\n" "$f" "$([ -s $KOKORO_DIR/$f ] && echo ok || echo MISSING) ($KOKORO_DIR)"; done
}

pango_headers() {
  # Runtime pango/harfbuzz libs exist but dev headers don't (no sudo/apt). Fetch the matching headers
  # from GitHub via git (works even when codeload/raw.githubusercontent are blocked) and fake pkg-config.
  local P=/tmp/pango-dev/prefix L
  L=$(ls -d /usr/lib/$(uname -m)-linux-gnu 2>/dev/null || echo /usr/lib)
  local pso hso pv hv
  pso=$(ls $L/libpango-1.0.so.0.* 2>/dev/null | head -1); hso=$(ls $L/libharfbuzz.so.0.* 2>/dev/null | head -1)
  [ -n "$pso" ] && [ -n "$hso" ] || { echo "no runtime pango/harfbuzz libs found in $L"; return 1; }
  pv=$(python3 -c "import re,sys;n=int(re.search(r'so\.0\.(\d+)',sys.argv[1]).group(1));m=re.search(r'so\.0\.\d+\.(\d+)',sys.argv[1]);print(f'1.{n//100}.{m.group(1) if m else 0}')" "$pso")
  hv=$(python3 -c "import re,sys;n=int(re.search(r'so\.0\.(\d+)',sys.argv[1]).group(1));v=n-60000 if n>=60000 else None;print(f'{v//100}.{(v//10)%10}.{v%10}' if v is not None else f'{n//10000}.{(n//100)%100}.{n%100}')" "$hso")
  echo "pango $pv, harfbuzz $hv (from $L)"
  rm -rf /tmp/pango-dev && mkdir -p $P/include/pango-1.0/pango $P/include/harfbuzz $P/lib/pkgconfig && cd /tmp/pango-dev
  timeout 150 git clone -q --depth 1 --branch "$pv" --filter=blob:none --sparse https://github.com/GNOME/pango.git 2>/dev/null \
    && (cd pango && git sparse-checkout set pango >/dev/null 2>&1) || { echo "pango clone failed"; return 1; }
  timeout 150 git clone -q --depth 1 --branch "$hv" --filter=blob:none --sparse https://github.com/harfbuzz/harfbuzz.git 2>/dev/null \
    && (cd harfbuzz && git sparse-checkout set src >/dev/null 2>&1) || { echo "harfbuzz clone failed"; return 1; }
  cp pango/pango/*.h $P/include/pango-1.0/pango/
  IFS=. read -r MA MI MC <<< "$pv"
  printf '#ifndef PANGO_FEATURES_H\n#define PANGO_FEATURES_H\n#define PANGO_VERSION_MAJOR %s\n#define PANGO_VERSION_MINOR %s\n#define PANGO_VERSION_MICRO %s\n#define PANGO_VERSION_STRING "%s"\n#endif\n' $MA $MI $MC $pv \
    > $P/include/pango-1.0/pango/pango-features.h
  local HDRS
  HDRS=$(cd pango/pango && python3 -c "import re;s=open('meson.build').read();m=re.search(r'pango_headers\s*=\s*\[(.*?)\]',s,re.S);print(' '.join(re.findall(r\"'([^']+\.h)'\",m.group(1))))")
  (cd pango/pango && glib-mkenums --template pango-enum-types.h.template $HDRS > $P/include/pango-1.0/pango/pango-enum-types.h)
  cp harfbuzz/src/*.h $P/include/harfbuzz/
  for n in pango-1.0 pangocairo-1.0 pangoft2-1.0 harfbuzz; do ln -sf $(ls $L/lib$n.so.0 | head -1) $P/lib/lib$n.so; done
  cat > $P/lib/pkgconfig/harfbuzz.pc <<EOF
Name: harfbuzz
Description: hb
Version: $hv
Libs: -L$P/lib -lharfbuzz
Cflags: -I$P/include/harfbuzz
EOF
  for pc in "pango|glib-2.0 gobject-2.0 harfbuzz|-lpango-1.0" "pangocairo|pango cairo pangoft2|-lpangocairo-1.0" \
            "pangoft2|pango freetype2 fontconfig|-lpangoft2-1.0" "pangofc|pango fontconfig|"; do
    IFS='|' read -r name req lib <<< "$pc"
    printf 'Name: %s\nDescription: %s\nVersion: %s\nRequires: %s\nLibs: -L%s/lib %s\nCflags: -I%s/include/pango-1.0\n' \
      "$name" "$name" "$pv" "$req" "$P" "$lib" "$P" > $P/lib/pkgconfig/$name.pc
  done
  export PKG_CONFIG_PATH=$P/lib/pkgconfig
  pkg-config --cflags pangocairo >/dev/null && echo "pango headers ready"
}

install_manim() {
  if have_py manim; then echo "manim already installed: $(python3 -c 'import manim;print(manim.__version__)')"; return 0; fi
  if [ "$(uname)" = "Darwin" ]; then
    python3 -c 'import sys; sys.exit(sys.version_info < (3, 11))' ||
      echo "WARNING: $(python3 --version) - on macOS use a venv with Python >= 3.11 (e.g. python3.13 -m venv ~/.venvs/manim-explainer)"
    command -v pkg-config >/dev/null || command -v pkgconf >/dev/null ||
      echo "NOTE: pycairo builds from source on macOS and needs pkg-config: brew install pkgconf ffmpeg"
  fi
  $PIP manim scipy soundfile 2>&1 | tail -2
  if ! have_py manim && [ "$(uname)" = "Darwin" ]; then
    echo "FAILED on macOS: run 'brew install pkgconf cairo pango ffmpeg', then rerun setup.sh manim"; return 1
  fi
  if ! have_py manimpango; then
    echo "manimpango failed to build (missing pango headers) -> fetching headers"
    pango_headers || { echo "FAILED: install pango dev headers (e.g. brew install pango / apt install libpango1.0-dev)"; return 1; }
    PKG_CONFIG_PATH=/tmp/pango-dev/prefix/lib/pkgconfig $PIP manim scipy soundfile 2>&1 | tail -2
  fi
  have_py manim && echo "manim ok: $(python3 -c 'import manim;print(manim.__version__)')" || echo "manim install FAILED"
}

install_latex() {
  # Manim needs latex + dvisvgm. TinyTeX installs into the home folder (no sudo); its own PATH step asks for
  # sudo and fails harmlessly - the bin folder is added to PATH at the top of this script and must also go in env.sh.
  if command -v latex >/dev/null && command -v dvisvgm >/dev/null; then echo "latex ok: $(command -v latex)"; return 0; fi
  if ! command -v tlmgr >/dev/null; then
    curl -sfL -m 60 https://yihui.org/tinytex/install-bin-unix.sh -o /tmp/install-tinytex.sh \
      || { echo "TinyTeX installer download FAILED (network?). Alternatives: apt install texlive-latex-extra dvisvgm / brew install --cask basictex"; return 1; }
    sh /tmp/install-tinytex.sh 2>&1 | grep -v -i "sudo\|password" | tail -3
    for d in "$HOME"/Library/TinyTeX/bin/* "$HOME"/.TinyTeX/bin/*; do [ -d "$d" ] && export PATH="$PATH:$d"; done
  fi
  tlmgr install standalone preview doublestroke ms everysel setspace rsfs relsize ragged2e fundus-calligra \
    microtype wasysym physics dvisvgm jknapltx wasy cm-super babel-english gnu-freefont mathastext cbfonts-fd \
    amsfonts bm 2>&1 | tail -1
  if command -v latex >/dev/null && command -v dvisvgm >/dev/null; then
    echo "latex ok. Add to env.sh:  export PATH=\$PATH:$(dirname "$(command -v latex)")"
  else
    echo "latex install FAILED"; return 1
  fi
}

install_tts() {
  $PIP kokoro-onnx onnxruntime soundfile 2>&1 | tail -1
  mkdir -p "$KOKORO_DIR" && cd "$KOKORO_DIR"
  if [ ! -s kokoro-q8.onnx ]; then
    # Source 1: npm registry (often allowed when Hugging Face / GitHub releases are blocked)
    if curl -sfL -m 170 -o shards.tgz https://registry.npmjs.org/kokoro-q8-shards/-/kokoro-q8-shards-1.0.0.tgz; then
      rm -rf shards && mkdir shards && tar xzf shards.tgz -C shards && cat shards/package/kokoro-q8.part{0,1,2,3,4,5}.bin > kokoro-q8.onnx
      rm -rf shards shards.tgz
    fi
    if [ "$(sha kokoro-q8.onnx)" != "$SHA_MODEL" ]; then
      # Source 2: kokoro-onnx GitHub release (normal internet)
      rm -f kokoro-q8.onnx
      curl -sfL -m 170 -o kokoro-q8.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx \
        || { rm -f kokoro-q8.onnx; echo "model download FAILED (npm and GitHub both unreachable)"; }
    fi
  fi
  if [ ! -s voices.npz ]; then
    if curl -sfL -m 120 -o rt.tgz https://registry.npmjs.org/kokoro-local-runtime/-/kokoro-local-runtime-0.1.0.tgz; then
      rm -rf rt && mkdir rt && tar xzf rt.tgz -C rt
      python3 - <<'PY'
import glob, os, numpy as np
vs = {os.path.basename(f)[:-4]: np.fromfile(f, dtype=np.float32).reshape(510, 1, 256)
      for f in glob.glob('rt/package/voices/*.bin')}
np.savez('voices.npz', **vs); print(len(vs), 'voices')
PY
      rm -rf rt rt.tgz
    else
      curl -sfL -m 120 -o voices.npz https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin \
        || { rm -f voices.npz; echo "voices download FAILED"; }
    fi
  fi
  python3 - <<PY 2>&1 | grep -v cpuid
import soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro("$KOKORO_DIR/kokoro-q8.onnx", "$KOKORO_DIR/voices.npz")
s, sr = k.create("Testing, one two three.", voice="af_heart", lang="en-us")
print("kokoro ok: %.1fs of audio" % (len(s) / sr))
PY
}

case "${1:-check}" in
  check) check ;;
  manim) install_manim ;;
  latex) install_latex ;;
  tts) install_tts ;;
  *) echo "usage: setup.sh check|manim|latex|tts" ;;
esac
