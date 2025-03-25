import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import matplotlib


def computeMw(label, time, moment_rate):
    M0 = np.trapz(moment_rate[:], x=time[:])
    Mw = 2.0 * np.log10(M0) / 3.0 - 6.07
    print(f"{label} moment magnitude: {Mw} (M0 = {M0:.4e})")
    return Mw


def read_usgs_moment_rate(fname):
    mr_ref = np.loadtxt(fname, skiprows=2)
    # Conversion factor from dyne-cm/sec to Nm/sec (for older usgs files)
    scaling_factor = 1.0 if np.amax(mr_ref[:, 1]) < 1e23 else 1e-7
    mr_ref[:, 1] *= scaling_factor
    return mr_ref


fig = plt.figure(figsize=(7.5, 7.5 * 5.0 / 16), dpi=80)
ax = fig.add_subplot(111)
ps = 12
matplotlib.rcParams.update({"font.size": ps})
plt.rcParams["font.family"] = "sans"
matplotlib.rc("xtick", labelsize=ps)
matplotlib.rc("ytick", labelsize=ps)
matplotlib.rcParams["lines.linewidth"] = 0.5


def add_seissol_data(ax, label, fn):
    df = pd.read_csv(fn)
    df = df.pivot_table(index="time", columns="variable", values="measurement")
    df["seismic_moment_rate"] = np.gradient(df["seismic_moment"], df.index[1])
    Mw = computeMw(label, df.index.values, df["seismic_moment_rate"])
    ax.plot(
        df.index.values,
        df["seismic_moment_rate"] / 1e18,
        label=f"{label} (Mw={Mw:.2f})",
    )


supershear_model = False
if not supershear_model:
    add_seissol_data(
        ax,
        "geodetic informed",
        "../seissol_outputs/one_segment_top_0_Yohai/dyn_0001_coh0.25_1_B0.9_C0.1_R0.6-energy.csv",
    )

use_tmax = False
if use_tmax:
    fn = "../seissol_outputs/Solucion_strike_98_tmax23_1D/dyn_0008_coh0.25_1_B0.9_C0.2_R0.65-energy.csv"
else:
    fn = "../seissol_outputs/energy_files/Solucion_strike_98_1D/dyn_0036_coh0.25_1_B1.0_C0.2_R0.55-energy.csv"

add_seissol_data(ax, "kinematic informed", fn)

if supershear_model:
    fn = "../seissol_outputs/energy_files/Solucion_strike_98_1D/dyn_0033_coh0.25_1_B1.0_C0.1_R0.7-energy.csv"
    add_seissol_data(ax, "kinematic informed (40% supershear)", fn)


usgs_mr = read_usgs_moment_rate("../../data/moment_rate.mr")
Mw = computeMw("usgs", usgs_mr[:, 0], usgs_mr[:, 1])

ax.plot(
    usgs_mr[:, 0],
    usgs_mr[:, 1] / 1e18,
    label=f"usgs (Mw={Mw:.2f})",
)

mr = np.loadtxt("../../data/moment_rate_from_finite_source_file.txt")
Mw = computeMw("ff", mr[:, 0], mr[:, 1])
ax.plot(
    mr[:, 0],
    mr[:, 1] / 1e18,
    label=f"kinematic model (Mw={Mw:.2f})",
)

ax.set_ylim(bottom=0)
ax.set_xlim(right=35)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

ax.set_ylabel(r"moment rate (e18 $\times$ Nm/s)")
ax.set_xlabel("time (s)")
plt.legend(frameon=False)
plt.savefig("moment_rate.svg")
plt.show()
