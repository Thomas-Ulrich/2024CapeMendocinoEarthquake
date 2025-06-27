## Dynamic Rupture Workflow for the Mw7 2024 Mendocino Earthquake

This guide outlines the steps for running the dynamic rupture workflow to characterize the rupture dynamics of the Mw7 2024 Mendocino earthquake.

---

### 1. Clone the Workflow Repository

Clone the `rapid-earthquake-dynamics` repository at version `v0.1.1`:

```bash
git clone --recursive --branch v0.1.1 https://github.com/Thomas-Ulrich/rapid-earthquake-dynamics
```

### 2. Prepare the Earthquake Scenario

Run the setup script to retrieve earthquake information and generate the files needed to construct an ensemble of dynamic rupture models from a kinematic finite fault model:

```bash
../rapid-earthquake-dynamics/step1_model_setup.py --config input_config.yaml
```

This will create a directory containing all necessary input files.

### 3. Run the Workflow on HPC (e.g., superNG)

Copy the generated folder to your HPC system (e.g., superNG) and execute the workflow using:

```bash
../rapid-earthquake-dynamics/step2_NG.sh
```

This script will launch a sequence of srun jobs to:

1. Compute the stress change from the finite fault model

2. Generate input files for the ensemble of dynamic rupture models

3. Run all dynamic rupture simulations

4. Validate the models against available observations


