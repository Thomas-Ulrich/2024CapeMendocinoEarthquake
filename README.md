## Dynamic Rupture Workflow for the Mw7 2024 Mendocino Earthquake


The repository gathers inputs files and scripts used in our study of the 2024 Mw7.0 Cape Mendocino Earthquake (currently under review):

Ulrich, T., Magen, Y., & Gabriel, A. A. (2025). The complex rupture dynamics of an oceanic transform fault: supershear rupture and deep slip during the 2024 Mw7. 0 Cape Mendocino Earthquake.
https://doi.org/10.31223/X5XT7Q


It lists

- the code used for performing the kinematic inversions (`inversions` and `inv1994` folders)
- The code used to generate the 3D velocity model (`inversions/scripts/generate_ASAGI_3d_casc16.py`)
- The code to reproduce the manuscript figures (`figures` folder)
- The code to generate a ensemble of dynamic rupture scenario and identify a preferred dynamic rupture scenario (see `seissol_setup` folder and detailed instructions in the README.md of the `seissol_setup` folder)

## Dynamic Rupture Workflow for the Mw7 2024 Mendocino Earthquake

This repository contains the input files and scripts used in our study of the 2024 Mw7.0 Cape Mendocino Earthquake, currently under review:

> Ulrich, T., Magen, Y., & Gabriel, A. A. (2025). *The complex rupture dynamics of an oceanic transform fault: supershear rupture and deep slip during the 2024 Mw7.0 Cape Mendocino Earthquake*.  
> [https://doi.org/10.31223/X5XT7Q](https://doi.org/10.31223/X5XT7Q)

### Contents

- **Kinematic inversion input files** used to derive finite-fault models  
  *(see the `inversions/` and `inv1994/` folders)*

- **3D velocity model generation script**, used to create an ASAGI-formatted model based on the 3D Cascadia community velocity model (Stephenson et al., 2017)
  *(see `inversions/scripts/generate_ASAGI_3d_casc16.py`)*

- **Figure reproduction scripts** for all figures shown in the manuscript  
  *(see the `figures/` folder)*

- **Dynamic rupture workflow** to generate an ensemble of dynamic rupture scenarios and identify the preferred model  
  *(see the `seissol_setup/` folder and its `README.md` for detailed instructions)*


### Reference

Stephenson, W. J., Reitman, N. G., & Angster, S. J. (2017). *P- and S-wave velocity models incorporating the Cascadia subduction zone for 3D earthquake ground motion simulations, Version 1.6—Update for Open-File Report 2007–1348* (No. 2017-1152). US Geological Survey.  
[https://doi.org/10.3133/ofr20171152](https://doi.org/10.3133/ofr20171152)
