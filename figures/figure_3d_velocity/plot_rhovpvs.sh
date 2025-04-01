file=$1-fault.xdmf
output_prefix=$2
zoom=2.0

view=normal
rel=0.7

light_quake_visualizer $file  --variable rho --cmap davos_r --color_range "2290 3341" --zoom $zoom --window 1200 600 --output rho --time "i-1" --view $view
light_quake_visualizer $file  --variable Vp --cmap lipari_r --color_range "3341 8140" --zoom $zoom --window 1200 600 --output vp --time "i-1" --view $view
light_quake_visualizer $file  --variable Vs --cmap lapaz_r --color_range "2062 4628" --zoom $zoom --window 1200 600 --output vs --time "i-1" --view $view


generate_color_bar davos_r --crange 2290 3341 --labelfont 12 --height 1.4 3 --nticks 3
generate_color_bar lipari_r --crange 3.34 8.14 --labelfont 12 --height 1.4 3 --nticks 3
generate_color_bar lapaz_r --crange 2.06 4.62 --labelfont 12 --height 1.3 4 --nticks 3

image_combiner --inputs output/rho.png output/vp.png output/vs.png  --rel $rel 1.0 --output output/${output_prefix}rhovpvs.png --col 1 
