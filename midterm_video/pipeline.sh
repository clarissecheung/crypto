#!/bin/bash
# pipeline.sh WORKDIR chN:outname [chM:outname ...]
# For each chapter: narration (TTS + LaTeX) -> 720p render -> assemble into out/<outname>.mp4
W=$1; shift
for spec in "$@"; do
  ch=${spec%%:*}; name=${spec#*:}
  source /home/user/crypto/midterm_video/env.sh $ch
  export EXPLAINER_WORK=$W
  echo "=== $ch: tts $(date +%T)"
  python3 tts_pass.py 2>&1 | grep -E "CHECK|DONE|Error|Traceback|min of speech" 
  echo "=== $ch: render $(date +%T)"
  python3 render.py --quality mid --budget 0 --jobs 2 2>&1 | grep -E "FAIL|fail|ALL DONE|rror"
  echo "=== $ch: assemble $(date +%T)"
  python3 assemble.py --quality mid /home/user/crypto/midterm_video/out/$name.mp4 2>&1 | tail -1
done
echo "PIPELINE DONE $(date +%T)"
