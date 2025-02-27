file=$1-fault.xdmf
output_prefix=$2
zoom=2.0

if [ $output_prefix == "static" ]; then
    view=normal-flip
    rel=0.5
else
    view=normal
    rel=0.7
fi

light_quake_visualizer $file  --variable SR --cmap magma_r0 --color_range "0 2.0" --zoom $zoom --window 1200 600 --output SR%d --time "4;7;10;15;19" --view $view
image_combiner --inputs output/SR_0.png output/SR_1.png output/SR_2.png output/SR_3.png output/SR_4.png  --rel ${rel} 1.0 --output output/${output_prefix}SR.png --col 1 #--keep_white
