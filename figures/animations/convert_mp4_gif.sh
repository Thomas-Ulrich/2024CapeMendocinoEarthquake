# Step 1: Generate color palette
ffmpeg -i $1.mp4 -vf "fps=15,scale=800:-1:flags=lanczos,palettegen" palette.png

# Step 2: Use palette to create high-quality GIF
ffmpeg -i $1.mp4 -i palette.png -filter_complex "fps=15,scale=800:-1:flags=lanczos[x];[x][1:v]paletteuse" $1.gif

