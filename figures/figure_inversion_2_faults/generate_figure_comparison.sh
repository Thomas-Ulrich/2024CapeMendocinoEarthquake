#!/bin/bash
f1=/export/dump/ulrich/trash_Mendocino/2024CapeMendocinoEarthquake/inversions/newdip90_strike100_21/gnss_tl_sm2/
f2=/export/dump/ulrich/trash_Mendocino/2024CapeMendocinoEarthquake/inversions/splaydip70_2striket/gnss_tl_sm2/

cp $f1/../plots_gnss_tele_sm_shorter_shma/Solution.param $f1/Solution.txt
cp $f2/../plots_gnss_tele_sm_shorter_shma/Solution.param $f2/Solution.txt

#change to the following for the figure checking the effect of the velocity model
#f2=/export/dump/ulrich/2024CapeMendocinoEarthquake/inversions/all_usgs_vel/usgs_vel_gps_tl_sm2/
ln -s $(realpath plot_graphic_NEIC_multiple.py) /import/cachemiss-dump/ulrich/neic-finitefault/src/ffm/plot_graphic_NEIC_multiple.py
python /import/cachemiss-dump/ulrich/neic-finitefault/src/ffm/plot_graphic_NEIC_multiple.py "$f1,$f2" "body" --stations_body "LVZ,GRFO,PAB,MACI,SSPA,FDFM,MPG,SAML,PAYG"
python /import/cachemiss-dump/ulrich/neic-finitefault/src/ffm/plot_graphic_NEIC_multiple.py "$f1,$f2" "strong" --stations_strong "KRP,THOM,KMPB,PETL,MNDO"
python /import/cachemiss-dump/ulrich/neic-finitefault/src/ffm/plot_graphic_NEIC_multiple.py "$f1,$f2" "surf" --stations_surf "BORG,PAB,PAYG"
ffm plot neic -t gnss $f2 --ffm-solution --map-limits " -125.5" " -123.0" 39.8 41.3
ffm plot neic -t gnss $f2 --tensor
mv $f1/*.png .
cp $f2/plots/SlipDist_plane0.png .
cp $f2/../plots_gnss_tele_sm_shorter_shma/Map.png .
cp $f2/plots/Cumulative_Moment_Tensor.png .
cp $f2/plots/MomentRate.png .
