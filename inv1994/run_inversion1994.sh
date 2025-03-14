#!/bin/bash
set -euo pipefail

myfolder=res1994
suffix=auto


echo "Do you want to download the data(y/n)"
read -r download


# Prompt for user input
echo "Do you want to rerun the auto model (y/n)"
read -r rerun_auto

if [[ "$download" == "y" ]]; then
   mkdir -p data/Teleseismic_Data
   curl https://ds.iris.edu/spudservice/momenttensor/885430/cmtsolution -o data/cmtsolution
   wasp manage acquire data/Teleseismic_Data data/cmtsolution -t body
   cd ..
fi

if [[ "$rerun_auto" == "y" ]]; then
   wasp model run $(pwd) auto_model -g data/cmtsolution -t body -t surf -d data/Teleseismic_Data/
   cp 19940901151553/ffm.0/NP2 ${myfolder}_$suffix -r
   rm -r 19940901151553/ffm.0/NP2
fi


cp -r ${myfolder}_${suffix} ${myfolder}_up
suffix=up

cp input_data/vel_model.txt ${myfolder}_$suffix
cp input_data/segments_data.json ${myfolder}_$suffix
cd ${myfolder}_${suffix}
# obtaind with
# python scripts/prepare_velocity_model.py 125.7
wasp manage velmodel-to-json $(pwd) vel_model.txt
wasp manage update-inputs $(pwd) -p -m -a
wasp model run $(pwd) manual_model_add_data 
cp Solucion.txt plots
cp modelling_summary.txt plots
mv plots plots_no_shift


wasp process shift-match $(pwd) body -o auto
wasp process shift-match $(pwd) surf -o auto
wasp process remove-baseline $(pwd)
wasp manage update-inputs $(pwd) -t body -t surf
echo "starting inv with teleseismics after shift-match"
wasp model run $(pwd) manual_model_add_data 

cp Solucion.txt plots
cp modelling_summary.txt plots
mv plots plots_shift



