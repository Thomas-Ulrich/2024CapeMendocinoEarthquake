#!/usr/bin/env bash

file_param=$1
output_prefix=$2
zoom=2.0
scalar_bar="0.91 0.35 160"
win_size="2000 1000"
time="i-1"

rel=0.7

light_quake_visualizer $file_param --variable mu_s --cmap davos_r --color_range "0.2 0.6" --zoom $zoom --window $win_size --output mus --time $time --view xz --output mu_s1 --vtk_meshes "hypo.vtk blue 1"
light_quake_visualizer $file_param --variable mu_s --cmap davos_r --color_range "0.2 0.6" --zoom $zoom --window $win_size --output mus --time $time --view nxz --output mu_s2 --vtk_meshes "hypo.vtk blue 1"

light_quake_visualizer $file_param --variable d_c --cmap lipari_r --color_range "0.1 0.62" --zoom $zoom --window $win_size --output dc --time $time --view xz --output d_c1 --vtk_meshes "hypo.vtk blue 1"
light_quake_visualizer $file_param --variable d_c --cmap lipari_r --color_range "0.1 0.62" --zoom $zoom --window $win_size --output dc --time $time --view nxz --output d_c2 --vtk_meshes "hypo.vtk blue 1"

light_quake_visualizer $file_param --variable shear_stress_MPa --cmap lapaz_r --color_range "0.0 22.0" --zoom $zoom --window $win_size --output shearstress --time $time --view xz --output st1 --vtk_meshes "hypo.vtk blue 1"
light_quake_visualizer $file_param --variable shear_stress_MPa --cmap lapaz_r --color_range "0.0 22.0" --zoom $zoom --window $win_size --output shearstress --time $time --view nxz --output st2 --vtk_meshes "hypo.vtk blue 1"

image_combiner --inputs output/mu_s1.png output/d_c1.png output/st1.png output/mu_s2.png output/d_c2.png output/st2.png \
  --rel $rel 1.0 \
  --output output/${output_prefix}parameters.png \
  --col 2
