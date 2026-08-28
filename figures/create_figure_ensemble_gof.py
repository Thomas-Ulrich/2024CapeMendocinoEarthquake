import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from dynworkflow.plot_utils import plot_combined_gof_plot

ps = 14
matplotlib.rcParams.update({"font.size": ps})
plt.rcParams["font.family"] = "sans"
matplotlib.rc("xtick", labelsize=ps)
matplotlib.rc("ytick", labelsize=ps)


df = pd.read_pickle("compiled_results.pkl")
Cname = "C"
print(df)

if not df.empty:
    keys_to_plot = [
        "gof_slip",
        "gof_body_wf",
        "gof_reg",
        "gof_MRF",
        #"gof_surf_wf",
        "combined_gof",
    ]
    nlines = 4
    preferred_model = {
        "B": df["B"].iloc[0],
        Cname: df[Cname].iloc[0],
        "R": df["R"].iloc[0],
    }
    preferred_model = {k: float(v) for k, v in preferred_model.items()}

    plot_combined_gof_plot(
        df,
        keys_to_plot,
        nlines,
        preferred_model,
        share_colorbar=True,
        combine_B_in_one_fig=True,
    )
