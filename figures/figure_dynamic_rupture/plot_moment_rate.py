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
plotted_lines = []

def add_seissol_data(ax, label, fn, plotted_lines):
    df = pd.read_csv(fn)
    df = df.pivot_table(index="time", columns="variable", values="measurement")
    df["seismic_moment_rate"] = np.gradient(df["seismic_moment"], df.index[1])
    Mw = computeMw(label, df.index.values, df["seismic_moment_rate"])
    line = ax.plot(
        df.index.values,
        df["seismic_moment_rate"] / 1e18,
        label=f"{label} (Mw={Mw:.2f})",
    )
    plotted_lines.append(line[0])
    return plotted_lines

supershear_model = False
if not supershear_model:
    plotted_lines = add_seissol_data(
        ax,
        "geodetic informed",
        "../seissol_outputs/one_segment_top_0_Yohai_200m_o5/dyn_0041_coh0.25_1.0_B1.0_C0.1_R0.6-energy.csv",
        plotted_lines
    )
    back_projection = pd.read_csv('../figure1/back_projection.csv')
    ax2 = ax.twinx()
    line = ax2.plot(back_projection.time,  back_projection.beam_power, "r--", label="back projection beampower")
    plotted_lines.append(line[0])
    ax2.set_ylabel("beam power")

use_tmax = False
if use_tmax:
    fn = "../seissol_outputs/Solucion_strike_98_tmax23_1D/dyn_0008_coh0.25_1_B0.9_C0.2_R0.65-energy.csv"
else:
    fn = "../seissol_outputs/energy_files/Solucion_strike_98_1D/dyn_0036_coh0.25_1_B1.0_C0.2_R0.55-energy.csv"
    fn = "../seissol_outputs/Solucion_strike_98_casc_1km/dyn_0015_coh0.25_1_B0.9_C0.3_R0.7_large_output-energy.csv"
    fn = "../seissol_outputs/Solucion_strike_98_casc_1km_200m_o5/dyn_0019_coh0.25_1.0_B0.9_C0.3_R0.7-large-energy.csv"

plotted_lines = add_seissol_data(ax, "kinematic informed", fn, plotted_lines)

if supershear_model:
    fn = "../seissol_outputs/energy_files/Solucion_strike_98_1D/dyn_0033_coh0.25_1_B1.0_C0.1_R0.7-energy.csv"
    fn = "../seissol_outputs/Solucion_strike_98_casc_1km/dyn_0002_coh0.25_1_B0.9_C0.1_R0.65-energy.csv"
    fn = "../seissol_outputs/Solucion_strike_98_casc_1km_200m_o5_more_supershear/dyn_0002_coh0.25_1.0_B0.9_C0.1_R0.65-energy.csv"
    add_seissol_data(ax, "kinematic informed (37% supershear)", fn)
    fn = "../seissol_outputs/Solucion_strike_98_casc_1km_200m_o5_more_supershear/dyn_0013_coh0.25_1.0_B0.9_C0.2_R0.8-energy.csv"
    add_seissol_data(ax, "kinematic informed (37a% supershear)", fn)


usgs_mr = read_usgs_moment_rate("../../data/moment_rate.mr")
Mw = computeMw("usgs", usgs_mr[:, 0], usgs_mr[:, 1])

line = ax.plot(
    usgs_mr[:, 0],
    usgs_mr[:, 1] / 1e18,
    label=f"usgs (Mw={Mw:.2f})",
    color='k',
    linestyle = '--'
)
plotted_lines.append(line[0])

mr = np.loadtxt("../../data/STF.txt", skiprows=2)
Mw = computeMw("ff", mr[:, 0], mr[:, 1])
line = ax.plot(
    mr[:, 0],
    mr[:, 1] / 1e18,
    label=f"kinematic model (Mw={Mw:.2f})",
    color='k'
)
plotted_lines.append(line[0])

ax.set_ylim(bottom=0)
ax.set_xlim(right=37)
ax.set_xlim(left=0)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax2.spines["top"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

ax.set_ylabel(r"moment rate (e18 $\times$ Nm/s)")
ax.set_xlabel("time (s)")
labels = [l.get_label() for l in plotted_lines]
ax.legend(plotted_lines, labels, frameon=False)

#plt.legend(frameon=False)
fn = "moment_rate.svg"
plt.savefig(fn)
print(f"done writing {fn}")

plt.show()
