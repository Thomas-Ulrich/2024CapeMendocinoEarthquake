#!/bin/bash
file="$1"
prefix="$2"
extension="$3"

echo "file: $file"
echo "prefix: $prefix"
echo "format: $extension"

rm output/v3*.png


light_quake_visualizer "$file-surface.xdmf" --variable v3 --cmap vik --color_range "-0.1 0.1" \
    --zoom 1.3 --window 1600 1200 --annotate_time "k 0.08 0.8" --time "i:" \
    --scalar_bar "0.88 0.35 300" --view xy --font_size 20  --lighting 0.1 0.6 0.5 --vtk "../pvcc_vtk/CoastLine_z100.vtk black 2" --output v3%d

if [[ "$extension" == "gif" ]]; then
    ffmpeg -y -i output/SR_%d.png \
           -vf "fps=20,scale=trunc(iw/2)*2:trunc(ih/2)*2:flags=lanczos,palettegen" palette.png

    ffmpeg -y -i output/SR_%d.png \
           -i palette.png \
           -filter_complex "fps=20,scale=trunc(iw/2)*2:trunc(ih/2)*2:flags=lanczos,setpts=2*PTS,paletteuse" \
           "Mendocino_${prefix}_SR.gif"
else
    ffmpeg -y -framerate 20 -i output/v3_%d.png \
           -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -f mp4 -vcodec libx264 \
           -pix_fmt yuv420p -q:v 1 "Mendocino${prefix}_wavefield_vertical_velocity.mp4"
fi

