#!/bin/bash
set -euo pipefail

#lon=124.5
lon=124.75
#myfolder=LL19${lon}
myfolder=re98_20s_lon${lon}_m125.022_dip_90_270
#myfolder=dipm70_20s_lon${lon}

# Prompt for user input
echo "Do you want to rerun the gnss (y/n)"
read -r rerun_gnss

echo "Do you want to rerun the gnss-teleseismic inversion (y/n)"
read -r rerun_gnss_tele

echo "Do you want to rerun the gnss-teleseismic-strong motion inversion (y/n)"
read -r rerun_gnss_tele_strong

copy_results_to_plots_and_rename() {
  # $1 = name of the destination folder (e.g., plots_gnss_tele_shift_match)
  if [ -z "$1" ]; then
    echo "Usage: copy_and_move <destination_folder>"
    return 1
  fi
  dest="$1"
  mv Solution.txt plots
  mv modelling_summary.txt plots
  # move misfit_details.txt only if it exists
  if [ -f misfit_details.txt ]; then
    mv misfit_details.txt plots
  fi
  # Step 2: rename/move 'plots' to the destination folder name
  mv plots ../$dest
}

mkdir -p $myfolder && cd $myfolder

suffix=gnss
if [[ "$rerun_gnss" == "y" ]]; then
  #we first run a auto inversion
  ln -sfn ../data data
  ln -sfn ../scripts scripts
  ln -sfn ../input_data input_data
  ffm model run $(pwd) auto_model -g data/cmtsolution -t gnss -d data/Static_Data/

  auto_folder=$(../scripts/compile_folder_name_auto_inversion.py)
  cp $auto_folder/ffm.0/NP1/ $suffix -r
  rm -r $auto_folder

  cp input_data/annealing_prop.json $suffix

  if [[ $myfolder == LL* ]]; then
    echo "using Li and Lay 2 segment model"
    # your commands here
    cp input_data/segments_data_2segments.json $suffix/segments_data.json
    cp input_data/model_space_2segments.json $suffix/model_space.json
    cp input_data/tensor_info_LL.json $suffix/tensor_info.json
  elif [[ $myfolder == dip* ]]; then
    dip_value="${myfolder#dip}"  # remove leading 'dip'
    dip_value="${dip_value%%_*}" # keep only characters before first '_'
    echo "using dip $dip_value fault"
    cp "input_data/segments_data_dip${dip_value}.json" "$suffix/segments_data.json"
    cp "input_data/model_space_vardip.json" "$suffix/model_space.json"
  elif [[ $myfolder == re98* ]]; then
    echo "using strike 98 base fault model"
    cp input_data/segments_data.json ${myfolder}_$suffix
    cp input_data/model_space_vardip.json $suffix/model_space.json
  elif [[ $myfolder == with_cascadia* ]]; then
    cp input_data/segments_data_with_cascadia.json ${myfolder}_$suffix/segments_data.json
    cp input_data/model_space_with_cascadia.json ${myfolder}_$suffix/model_space.json
  else
    echo "$myfolder structure not understood"
    exit -1
  fi

  if [[ "$myfolder" == *usgs* ]]; then
    #only if usgs in the myfolder name will the usgs default velocity model be used
    cd ${suffix}
  else
    python scripts/prepare_velocity_model.py $lon
    cp data/vel_model.txt $suffix
    cd ${suffix}
    ffm manage velmodel-to-json $(pwd) vel_model.txt
  fi

  ffm manage update-inputs $(pwd) -p -m -a
  ffm model run $(pwd) manual_model_add_data
  copy_results_to_plots_and_rename plots_gnss
  cd ..
fi

if [[ "$rerun_gnss_tele" == "y" ]]; then
  cp -r ${suffix} gnss_tele
  suffix=gnss_tele
  cd ${suffix}

  echo "starting inv with teleseismics"
  ffm model run $(pwd) manual_model_add_data -t body -t surf -d ../data/Teleseismic_Data/
  ffm manage modify-dicts $(pwd) downweight surf -sc "KBS:BHZ"
  ffm manage modify-dicts $(pwd) downweight surf -sc "KEV:BHZ"
  ffm manage modify-dicts $(pwd) downweight surf -sc "MIDW:BHT"
  ffm manage modify-dicts $(pwd) downweight surf -sc "MSVF:BHT"
  ffm manage modify-dicts $(pwd) downweight surf -sc "MA2:BHT"
  ffm manage update-inputs $(pwd) -t surf

  copy_results_to_plots_and_rename plots_gnss_tele

  ffm process shift-match $(pwd) body -o auto
  ffm process shift-match $(pwd) surf -o auto
  ffm process remove-baseline $(pwd)
  ffm manage update-inputs $(pwd) -t body -t surf
  echo "starting inv with teleseismics after shift-match"
  ffm model run $(pwd) manual_model_add_data
  copy_results_to_plots_and_rename plots_gnss_tele_shift_match
  cd ..
fi

if [[ "$rerun_gnss_tele_strong" == "y" ]]; then
  suffix=gnss_tele
  cp -r $suffix gnss_tele_sm
  suffix=gnss_tele_sm
  cd ${suffix}
  ffm model run $(pwd) manual_model_add_data -t strong -d ../data/StrongMotion_Data/
  copy_results_to_plots_and_rename plots_gnss_tele_sm
  echo "done running inversion with trong motion"
  ../scripts/modify_wasp_strong_motion_waves.py 10
  ffm model run $(pwd) manual_model_add_data
  copy_results_to_plots_and_rename plots_gnss_tele_sm_shorter
  cd ..
  echo "done running inversion with strong motion (shorter)"

  cp -r ${suffix} gnss_tl_sm2
  suffix=gnss_tl_sm2
  cd ${suffix}
  ffm process shift-match $(pwd) strong -o auto
  ffm model run $(pwd) manual_model_add_data
  copy_results_to_plots_and_rename plots_gnss_tele_sm_shorter_shma
  cd ..
  echo "done running inversion with strong motion (shorter + shift-match)"
fi
cd ..
