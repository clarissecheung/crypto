#!/bin/bash
# sheet.sh — contact sheets (grids of frames) for reviewing a render with the image Read tool.
#
#   bash sheet.sh video.mp4 OUTDIR/_sheet 8              # 4x4 grid, one frame every 8 s -> _sheet_01.png ...
#   bash sheet.sh video.mp4 OUTDIR/_sheet_z 1 60 16      # zoom: one frame/s from t=60 s for 16 s
#   bash sheet.sh video.mp4 OUTDIR/_sheet_big 8 0 0 2    # 2x2 grid (960 px tiles) when small text must be read
#   bash sheet.sh video.mp4 OUTDIR/_sheet_t73.png at 73.5   # one full-size frame at t = 73.5 s
#
# 4x4 tiles (480 px) are good for layout and overlaps but too small to proofread captions or
# headers; use the 2x2 grid or a single frame for that. Keep the "_sheet" prefix so cleanup is easy:
#   rm -f OUTDIR/_sheet*
V=$1; OUT=$2; STEP=$3
if [ "$STEP" = "at" ]; then
  ffmpeg -loglevel error -y -ss "$4" -i "$V" -frames:v 1 -vf scale=1600:-1 "$OUT" && echo "$OUT"; exit
fi
G=${6:-4}; W=$((1920 / G))
SS=()
[ -n "${4:-}" ] && [ "${4:-0}" != "0" ] && SS=(-ss "$4")
[ -n "${5:-}" ] && [ "${5:-0}" != "0" ] && SS+=(-t "$5")
ffmpeg -loglevel error -y "${SS[@]}" -i "$V" -vf "fps=1/$STEP,scale=$W:-1,tile=${G}x${G}" "${OUT}_%02d.png"
ls "${OUT}"_*.png
echo "duration: $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V") s"
