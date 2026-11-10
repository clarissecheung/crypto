#!/bin/bash
# newch.sh chN : create/refresh a chapter folder with copies of the shared pipeline files
set -e
cd "$(dirname "$0")"
mkdir -p "$1"
for f in explainer.py cx.py render.py assemble.py tts_pass.py pronounce.py sheet.sh; do cp shared/$f "$1/"; done
