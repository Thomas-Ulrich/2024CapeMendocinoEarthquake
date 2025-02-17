projection="+proj=tmerc +datum=WGS84 +k=0.9996 +lon_0=-125.02 +lat_0=40.37"

python ~/TuSeisSolScripts/displayh5vtk/generate_vtk_grid.py --lon " -125" " -122" --lat 39 44 --dx 1 --proj "$projection"
mv grid.vtk grid_larger.vtk
python ~/TuSeisSolScripts/displayh5vtk/generate_vtk_grid.py --lon " -125" " -123" --lat 39 44 --dx 1 --proj "$projection"
~/SeisSol/SeisSol/postprocessing/visualization/tools/CreateVtkCoastLineFromGmt.py --lon " -128" " -122" --lat 39 44 --proj "$projection" --resolution f --filter 1000
