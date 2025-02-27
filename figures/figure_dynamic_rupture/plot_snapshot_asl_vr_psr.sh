file=$1-fault.xdmf
zoom=2.0
light_quake_visualizer $file  --variable ASl --cmap davos_r0 --color_range "0 3.0" --contour "file_index=0 var=RT contour=grey,2,0,max,1 contour=black,4,0,max,5" --zoom $zoom --window 1200 600 --output ASl --time "i-1" --view normal
light_quake_visualizer $file  --variable PSR --cmap lipari_r0 --color_range "0 4.0" --zoom $zoom --window 1200 600 --output PSR --time "i-1" --view normal
light_quake_visualizer $file  --variable Vr --cmap lapaz_r0 --color_range "0 6000" --zoom $zoom --window 1200 600 --output Vr --time "i-1" --view normal
image_combiner --inputs output/ASl.png output/PSR.png output/Vr.png  --rel 0.7 1.0 --output output/ASlVrPSR.png --col 1 
