#!/bin/bash
#f1=/export/dump/ulrich/trash_Mendocino/2024CapeMendocinoEarthquake/inversions/newdip90_strike100_21/gnss_tl_sm2/
f1=/export/dump/ulrich/trash_Mendocino/2024CapeMendocinoEarthquake/inversions/splaydip70_2striket_ref/gnss_tl_sm2/
f2=/export/dump/ulrich/trash_Mendocino/2024CapeMendocinoEarthquake/inversions/segments_data_with_cascadia/gnss_tl_sm2/

cp $f1/../plots_gnss_tele_sm_shorter_shma/Solution.param $f1/Solution.txt
cp $f2/../plots_gnss_tele_sm_shorter_shma/Solution.param $f2/Solution.txt

echo ffm plot neic -t gnss $f2 --ffm-solution --map-limits " -125.5" " -123.0" 39.8 41.3

#change to the following for the figure checking the effect of the velocity model
#f2=/export/dump/ulrich/2024CapeMendocinoEarthquake/inversions/all_usgs_vel/usgs_vel_gps_tl_sm2/
ln -s $(realpath plot_graphic_NEIC_multiple.py) /import/cachemiss-dump/ulrich/neic-finitefault/src/ffm/plot_graphic_NEIC_multiple.py
python /import/cachemiss-dump/ulrich/neic-finitefault/src/ffm/plot_graphic_NEIC_multiple.py "$f1,$f2" "body" --stations_body "HNR,MA2,LVZ,MACI,HRV,FDFM,MPG,SAML,PAYG"
mv $f1/P_body_waves.png tmp.png
python /import/cachemiss-dump/ulrich/neic-finitefault/src/ffm/plot_graphic_NEIC_multiple.py "$f1,$f2" "body" --stations_body "GUMO,HNR,KURK,HRV,MACI,PAYG"
mv tmp.png $f1/P_body_waves.png
python /import/cachemiss-dump/ulrich/neic-finitefault/src/ffm/plot_graphic_NEIC_multiple.py "$f1,$f2" "strong" --stations_strong "KRP,THOM,KMPB,PETL,MNDO"
#python /import/cachemiss-dump/ulrich/neic-finitefault/src/ffm/plot_graphic_NEIC_multiple.py "$f1,$f2" "surf" --stations_surf "BORG,PAB,PAYG"
python /import/cachemiss-dump/ulrich/neic-finitefault/src/ffm/plot_graphic_NEIC_multiple.py "$f1,$f2" "surf" --stations_surf "RAR,SSPA,PAYG"
#ffm plot neic -t gnss $f2 --ffm-solution --map-limits " -125.5" " -123.0" 39.8 41.3
ffm plot map -t gnss $f2 ../data/cmtsolution --map-limits " -125.5" " -123.0" 39.8 41.3
mv $f1/*.png .
cp $f2/plots/SlipDist_plane0.png .
#cp $f2/Map.png .
#cp $f2/plots/Cumulative_Moment_Tensor.png .
#cp $f2/plots/MomentRate.png .
