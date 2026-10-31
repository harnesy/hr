#!/usr/bin/env bash
# Copyright (c) 2026 Pavel Buchnev (harnsy)
# SPDX-License-Identifier: MIT
#
# encode.sh: encode a master video into web files (AV1 WebM, VP9 WebM, H.264 MP4, no audio track)
# and a poster frame (WebP + JPEG), then report each size against the targets given for the page.
# Run with --help for the options.
set -euo pipefail

usage() {
  cat <<'EOF'
usage: encode.sh <master.mp4> <out-dir> [options]

Writes <out-dir>/<name>.av1.webm, <name>.vp9.webm, <name>.mp4, <name>-poster.webp, <name>-poster.jpg.

options:
  --name NAME         base file name (default: video)
  --formats LIST      comma list of av1,vp9,mp4 (default: av1,vp9,mp4)
  --poster-at S       poster frame time in seconds (default 1.0)
  --width N           scale the output to this width, keeping the aspect (default: as the master)
  --av1-crf N         SVT-AV1 CRF (default 44; higher = smaller)
  --av1-preset N      SVT-AV1 preset (default 5; higher = faster)
  --vp9-crf N         VP9 CRF (default 34; above that, screen text tends to ghost)
  --h264-crf N        H.264 CRF (default 28)
  --still             tune H.264 for mostly still screens (-tune stillimage)
  --gop N             keyframe interval in frames (default 150; smaller = faster seeking, bigger files)
  --max-mb LIST       size targets, e.g. av1=1.2,vp9=1.5,mp4=0.9,poster=0.06 (MB); over = exit 3
  --audio             keep the master's audio (default: drop it)
  --parallel          run the encoders at the same time (more memory and CPU)
  -h, --help          this text

Compare text sharpness on a crop of each file against the master before handing over.
EOF
}

[[ $# -ge 1 && ( $1 == -h || $1 == --help ) ]] && { usage; exit 0; }
[[ $# -lt 2 ]] && { usage >&2; exit 1; }
M=$1; O=$2; shift 2
NAME=video; FORMATS=av1,vp9,mp4; POSTER_AT=1.0; WIDTH=; AV1_CRF=44; AV1_PRESET=5; VP9_CRF=34; H264_CRF=28
STILL=; GOP=150; MAX=; AUDIO=; PARALLEL=
while [[ $# -gt 0 ]]; do
  case $1 in
    --name) NAME=$2; shift 2;;
    --formats) FORMATS=$2; shift 2;;
    --poster-at) POSTER_AT=$2; shift 2;;
    --width) WIDTH=$2; shift 2;;
    --av1-crf) AV1_CRF=$2; shift 2;;
    --av1-preset) AV1_PRESET=$2; shift 2;;
    --vp9-crf) VP9_CRF=$2; shift 2;;
    --h264-crf) H264_CRF=$2; shift 2;;
    --still) STILL=1; shift;;
    --gop) GOP=$2; shift 2;;
    --max-mb) MAX=$2; shift 2;;
    --audio) AUDIO=1; shift;;
    --parallel) PARALLEL=1; shift;;
    -h|--help) usage; exit 0;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 1;;
  esac
done
[[ -f $M ]] || { echo "no such file: $M" >&2; exit 1; }
command -v ffmpeg >/dev/null || { echo "ffmpeg not found on PATH" >&2; exit 1; }
mkdir -p "$O"
export SVT_LOG=${SVT_LOG:-1}   # SVT-AV1: errors only

ENC=$(ffmpeg -hide_banner -encoders 2>/dev/null)
need() { grep -q " $1 " <<<"$ENC" || { echo "ffmpeg has no $1 encoder (needed for $2)" >&2; exit 1; }; }

VF=format=yuv420p
[[ -n $WIDTH ]] && VF="scale=$WIDTH:-2:flags=lanczos,format=yuv420p"
if [[ -n $AUDIO ]]; then A_WEBM=(-c:a libopus -b:a 96k); A_MP4=(-c:a aac -b:a 128k); else A_WEBM=(-an); A_MP4=(-an); fi
FF=(ffmpeg -hide_banner -loglevel error -y -i "$M")

jobs_run() { if [[ -n $PARALLEL ]]; then "$@" & else "$@"; fi; }
IFS=, read -ra FL <<<"$FORMATS"
for f in "${FL[@]}"; do
  case $f in
    av1) need libsvtav1 AV1
         jobs_run "${FF[@]}" -vf "$VF" -c:v libsvtav1 -crf "$AV1_CRF" -preset "$AV1_PRESET" -g "$GOP" \
           -svtav1-params tune=0 "${A_WEBM[@]}" "$O/$NAME.av1.webm";;
    vp9) need libvpx-vp9 VP9
         jobs_run "${FF[@]}" -vf "$VF" -c:v libvpx-vp9 -crf "$VP9_CRF" -b:v 0 -row-mt 1 -deadline good -cpu-used 2 \
           -auto-alt-ref 0 -g "$GOP" "${A_WEBM[@]}" "$O/$NAME.vp9.webm";;
    mp4) need libx264 H.264
         T=(); [[ -n $STILL ]] && T=(-tune stillimage)
         jobs_run "${FF[@]}" -vf "$VF" -c:v libx264 -crf "$H264_CRF" -preset slow "${T[@]}" -g "$GOP" \
           -movflags +faststart "${A_MP4[@]}" "$O/$NAME.mp4";;
    *) echo "unknown format: $f" >&2; exit 1;;
  esac
done
wait

# Poster: one frame, WebP and JPEG (the JPEG is the fallback for old browsers and link previews).
PVF=; [[ -n $WIDTH ]] && PVF="-vf scale=$WIDTH:-2:flags=lanczos"
ffmpeg -hide_banner -loglevel error -y -ss "$POSTER_AT" -i "$M" -frames:v 1 $PVF -c:v libwebp -quality 80 "$O/$NAME-poster.webp"
ffmpeg -hide_banner -loglevel error -y -ss "$POSTER_AT" -i "$M" -frames:v 1 $PVF -q:v 4 "$O/$NAME-poster.jpg"

# Report sizes and check them against the targets.
over=0
limit() { local k=$1; tr ',' '\n' <<<"$MAX" | awk -F= -v k="$k" '$1==k{print $2}'; }
report() {
  local file=$1 key=$2 b mb lim
  [[ -f $file ]] || return 0
  b=$(stat -c %s "$file"); mb=$(awk -v b="$b" 'BEGIN{printf "%.3f", b/1048576}')
  lim=$(limit "$key")
  if [[ -n $lim ]] && awk -v a="$mb" -v l="$lim" 'BEGIN{exit !(a>l)}'; then
    echo "  OVER  $(basename "$file")  $mb MB (target $lim MB)"; over=1
  else
    echo "  ok    $(basename "$file")  $mb MB${lim:+ (target $lim MB)}"
  fi
}
echo "files in $O:"
report "$O/$NAME.av1.webm" av1
report "$O/$NAME.vp9.webm" vp9
report "$O/$NAME.mp4" mp4
report "$O/$NAME-poster.webp" poster
report "$O/$NAME-poster.jpg" poster
exit $(( over ? 3 : 0 ))
