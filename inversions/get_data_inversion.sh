#!/bin/bash
set -euo pipefail

# Prompt for user input
echo "Do you want to download CMT data? (y/n)"
read -r download_cmt

echo "Do you want to download GPS data? (y/n)"
read -r download_gps

echo "Do you want to download Teleseismic data? (y/n)"
read -r download_teleseismic

echo "Do you want to download Strong Motion data? (y/n)"
read -r download_strongmotion

# Conditional execution based on user input

# Download CMT if needed
if [[ "$download_cmt" == "y" || "$download_cmt" == "Y" ]]; then
    echo "Downloading CMT data..."
    mkdir -p data
    curl https://ds.iris.edu/spudservice/momenttensor/22929936/cmtsolution -o data/cmtsolution
    scripts/modify_depth_in_cmtsolution.py
else
    echo "Skipping CMT download."
fi

# Download GPS if needed
if [[ "$download_gps" == "y" || "$download_gps" == "Y" ]]; then
    echo "Downloading GPS data..."
    wget http://geodesy.unr.edu/news_items/20241211/nc75095651_web.txt --directory-prefix data
    mkdir -p data/Static_Data
    scripts/filter_gps.py
else
    echo "Skipping GPS download."
fi

# Download Teleseismic data if needed
if [[ "$download_teleseismic" == "y" || "$download_teleseismic" == "Y" ]]; then
    echo "Downloading Teleseismic data..."
    mkdir -p data/Teleseismic_Data
    wasp manage acquire data/Teleseismic_Data data/cmtsolution -t body
else
    echo "Skipping Teleseismic download."
fi

# Download Strong Motion data if needed
if [[ "$download_strongmotion" == "y" || "$download_strongmotion" == "Y" ]]; then
    echo "Downloading Strong Motion data..."
    mkdir -p data/StrongMotion_Data
    ../submodules/seismic-waveform-factory/scripts/select_stations.py input_data/waveforms_config.ini 30 10 --channel "HN*"
    ../submodules/seismic-waveform-factory/scripts/copy_selected_sac_data_to_folder.py
    mv selected_sac data/StrongMotion_Data
else
    echo "Skipping Strong Motion download."
fi
