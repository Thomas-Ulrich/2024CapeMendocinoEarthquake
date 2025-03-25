#!/bin/bash
f1=/export/dump/ulrich/2024CapeMendocinoEarthquake/inversions/re98124.75_gps_tl_sm2
f2=/export/dump/ulrich/2024CapeMendocinoEarthquake/inversions/rwca124.75_gps_tl_sm2/
ln -s $(realpath plot_graphic_NEIC_multiple.py) /export/dump/ulrich/neic-finitefault/src/wasp/plot_graphic_NEIC_multiple.py
python /export/dump/ulrich/neic-finitefault/src/wasp/plot_graphic_NEIC_multiple.py "$f1,$f2" "body" --stations_body "LVZ,GRFO,PAB,MACI,SSPA,FDFM,MPG,SAML,PAYG"
python /export/dump/ulrich/neic-finitefault/src/wasp/plot_graphic_NEIC_multiple.py "$f1,$f2" "strong" --stations_strong "KRP,THOM,KMPB,PETL,MNDO"
python /export/dump/ulrich/neic-finitefault/src/wasp/plot_graphic_NEIC_multiple.py "$f1,$f2" "surf" --stations_surf "BORG,PAB,PAYG"
wasp plot neic -t gps $2 --ffm-solution --map-limits " -125.5" " -123.0" 39.8 41.3 
wasp plot neic -t gps $2 --tensor
mv $f1/*.png .
cp $f2/plots/SlipDist_plane0.png .
cp $f2/plots/Map.png .
cp $f2/plots/Cumulative_Moment_Tensor.png .
