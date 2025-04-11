generated with:
```
../rapid-earthquake-dynamics/step1_model_setup.py --event_id nc75095651 --finite_fault /import/exception-dump/ulrich/2024CapeMendocinoEarthquake/inversions/all_re98/re98124.75_gps_tl_sm2/Solucion_strike_98.param  --vel /import/exception-dump/ulrich/2024CapeMendocinoEarthquake/inversions/data/vel_model_axitra_fmt.txt --reference_moment_rate_function /import/exception-dump/ulrich/2024CapeMendocinoEarthquake/inversions/all_re98/re98124.75_gps_tl_sm2/STF.txt  --mesh /import/memoryleak-dump/ulrich/Mendocino/mend_topo --custom_setup_files "material.yaml;casc16_ASAGI.nc;fault_tags.yaml;observations" --regional_seismic_stations "NC.KRP,BK.SBAR,BK.THOM,BK.DMOR,NC.KMPB,BK.HUNT,BK.ETSL,BK.HALS,BK.MNDO" --mu_delta_min 0.02 --CFS_code CFS_code_block.lua 
```
