#!/bin/bash
file="$1"
prefix="$2"
extension="$3"

echo "file: $file"
echo "prefix: $prefix"
echo "format: $extension"

if [[ "$prefix" == "Geodetic" ]]; then
    view=normal-flip
else
    view=normal
fi

rm output/SR*.png

light_quake_visualizer $file --variable SR --cmap magma_r0 --color_range "0 2" \
    --zoom 1.5 --window 2000 1000 --annotate_time "k 0.15 0.8" --time "i:" \
    --scalar_bar "0.88 0.51 300" --view "$view" --font_size 20 --output SR%d

if [[ "$extension" == "gif" ]]; then
    ffmpeg -y -i output/SR_%d.png \
           -vf "fps=20,scale=trunc(iw/2)*2:trunc(ih/2)*2:flags=lanczos,palettegen" palette.png

    ffmpeg -y -i output/SR_%d.png \
           -i palette.png \
           -filter_complex "fps=20,scale=trunc(iw/2)*2:trunc(ih/2)*2:flags=lanczos,setpts=2*PTS,paletteuse" \
           "Mendocino_${prefix}_SR.gif"
else
    ffmpeg -y -framerate 20 -i output/SR_%d.png \
           -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -f mp4 -vcodec libx264 \
           -pix_fmt yuv420p -q:v 1 "Mendocino_${prefix}_SR.mp4"
fi

