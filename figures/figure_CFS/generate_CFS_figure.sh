#First compute dynCFS with:
#python ~/TuSeisSolScripts/onHdf5/compute_max_dyn_dCFS.py output3d/dyn_0072_coh0.25_1_B1.1_C0.3_R0.55cas-fault.xdmf
# extract regions 65 and 66
fn=../../seissol_output/max_dyn_dCFS.xdmf
seissol_output_extractor $fn --regionF "65,66" --add "extra"

light_quake_visualizer max_dyn_dCFSextra.xdmf --variable dyn_dCFS --cmap bilbao_r --color_range "0 1.5e6" --zoom 1.0 --window 1300 1200 --time "i-1" --vtk "../pvcc_vtk/CoastLine.vtk darkblue 2; ../pvcc_vtk/grid_larger.vtk k 1; ../pvcc_vtk/edges.vtk k 1" --view ../pvcc_vtk/forCFS.pvcc --output dyn_dCFS --zoom 1.8  #--scalar_bar "0.15 0.3 300"

maxc=1e5
light_quake_visualizer max_dyn_dCFSextra.xdmf --variable dCFS --cmap vik --color_range "-$maxc $maxc" --zoom 1.0 --window 1300 1200 --time "i-1" --vtk "../pvcc_vtk/CoastLine.vtk darkblue 2; ../pvcc_vtk/grid_larger.vtk k 1; ../pvcc_vtk/edges.vtk k 1" --view ../pvcc_vtk/forCFS.pvcc --output dCFS --zoom 1.8  #--scalar_bar "0.15 0.3 300"

rm max_dyn_dCFSextra.*
