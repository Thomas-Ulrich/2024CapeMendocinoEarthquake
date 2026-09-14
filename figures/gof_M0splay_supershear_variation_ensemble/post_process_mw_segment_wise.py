import numpy as np
import pandas as pd
import os
from cmcrameri import cm

# 1. Load the pickle file
df = pd.read_pickle("mw_segment_wise_compiled_results.pkl")  # Adjust filename if needed

# 2. Extract m0_65_ref from the reference file row
ref_file = "extracted_output/dyn-kinmod_compacted-fault.xdmf"

# If M0_65 wasn't explicitly saved as a column, compute M0_65 from Mw65:
# Formula: M0 = 10 ** (1.5 * (Mw + 6.07))
if "M065" in df.columns:
    df["M065"] = df["M065"]
else:
    df["M065"] = 10 ** (1.5 * (df["Mw65"] + 6.07))

ref_row = df[df["file"] == ref_file]

if ref_row.empty:
    raise ValueError(f"Reference file '{ref_file}' not found in DataFrame.")

m0_65_ref = ref_row["M065"].values[0]

# 3. Compute the ratio relative to the reference
df["M0_65_ratio"] = df["M065"] / m0_65_ref

df["file"] = df["file"].apply(
    lambda x: os.path.basename(x)
    .split("_extracted-fault.xdmf")[0]
    .split("_compacted-fault.xdmf")[0]
    .split("-fault.xdmf")[0]
)

df.rename(columns={"file": "faultfn"}, inplace=True)
# Keep only 'fault_fn' and 'M0_65_ratio'
df = df[["faultfn", "M0_65_ratio"]]

# Load your compiled results
df_compiled = pd.read_pickle("compiled_results.pkl")
# df_compiled.rename(columns={"R": "R0"}, inplace=True)
print(df_compiled)
# Merge on 'fault_fn'
# how='inner' keeps only matching rows, 'left' keeps all rows from df_compiled
merged_df = pd.merge(df_compiled, df, on="faultfn", how="left")

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)  # Prevents line wrapping

print(merged_df)

from dynworkflow.plot_utils import plot_combined_gof_plot

extra_label_map = {
    "M0_65_ratio": r"Relative $M_0$ (Splay)",
    "supershear": r"Rupture area with $V_r > V_s$ (%)",
}

Cname = "C"
preferred_model = {
    "B": df_compiled["B"].iloc[0],
    Cname: df_compiled[Cname].iloc[0],
    "R": df_compiled["R"].iloc[0],
}
preferred_model = {k: float(v) for k, v in preferred_model.items()}

plot_combined_gof_plot(
    merged_df,
    [
        "gof_surf_wf",
        "gof_body_wf",
        "gof_reg",
        "gof_slip",
        # "combined_gof",
    ],
    nlines=4,
    preferred_model=preferred_model,
    combine_B_in_one_fig=True,
    cmap=cm.cmaps["lipari"],
    extra_label_map=extra_label_map,
    output_prefix="all_gof_panels",
)


plot_combined_gof_plot(
    merged_df,
    [
        "supershear",
        "M0_65_ratio",
        "combined_gof",
    ],
    nlines=4,
    preferred_model=preferred_model,
    combine_B_in_one_fig=True,
    cmap=cm.cmaps["lipari"],
    extra_label_map=extra_label_map,
    output_prefix="supershear_M0_splay_combined_gof",
)
