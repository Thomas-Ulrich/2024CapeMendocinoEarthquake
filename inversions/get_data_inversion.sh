#!/bin/bash
set -euo pipefail

mkdir -p data
# Download GCMT
wget https://ds.iris.edu/spudservice/momenttensor/22929936/cmtsolution --directory-prefix data

# Download gps
wget http://geodesy.unr.edu/news_items/20241211/nc75095651_web.txt --directory-prefix data

mkdir -p data/Static_Data
scripts/filter_gps.py
