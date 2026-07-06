import argparse
import json
import math
import os

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cmcrameri.cm as cmc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from geographiclib.geodesic import Geodesic
from matplotlib.transforms import offset_copy


def add_great_circle_radius(ax, event, radius_deg=30):
    geod = Geodesic.WGS84
    lons_circle = []
    lats_circle = []
    for az in np.linspace(0, 360, 361):
        g = geod.ArcDirect(event["lat"], event["lon"], az, radius_deg)
        lons_circle.append(g["lon2"])
        lats_circle.append(g["lat2"])
    ax.plot(
        lons_circle,
        lats_circle,
        transform=ccrs.Geodetic(),
        color="grey",
        linestyle="--",
        linewidth=0.5,
        zorder=2,
    )
    # --- Annotate the radius at the bottom of the circle (azimuth 180°) ---
    g_bottom = geod.ArcDirect(event["lat"], event["lon"], 180, radius_deg)
    lon_text, lat_text = g_bottom["lon2"], g_bottom["lat2"]

    ax.text(
        lon_text,
        lat_text - 0.5,  # small offset southward for readability
        f"{radius_deg}°",
        color="k",
        ha="center",
        va="top",
        transform=ccrs.Geodetic(),
        bbox=dict(facecolor="white", alpha=0.6, edgecolor="none", pad=1.5),
    )

    return ax


parser = argparse.ArgumentParser(description="plot misfit map")
parser.add_argument("misfit_file", help="path to misfit_details.txt")
parser.add_argument(
    "--skip_station_name", help="skip station names", action="store_true"
)
parser.add_argument(
    "--extension", help="output file extension (e.g. png, pdf)", default="png"
)
args = parser.parse_args()


# -----------------------------
# Step 1: Read misfit details
# -----------------------------
misfit_file = args.misfit_file
df_misfit = pd.read_csv(
    misfit_file,
    sep=r"\s+",
    skiprows=1,
    names=["id", "sta_name", "component", "weight", "misfit"],
)
print(df_misfit)

# -----------------------------
# Step 2: Load station coordinates
# -----------------------------
possible_files = ["tele_waves.json", "surf_waves.json", "strong_motion_waves.json"]

stations = []

for json_file in possible_files:
    if os.path.exists(json_file):
        with open(json_file) as f:
            data = json.load(f)

        for entry in data:
            stations.append(
                {
                    "sta_name": entry["name"],
                    "longitude": entry["location"][1],
                    "latitude": entry["location"][0],
                }
            )

# Optional: remove duplicate station names (keep first)
unique_stations = {s["sta_name"]: s for s in stations}
stations = list(unique_stations.values())

df_stations = pd.DataFrame(stations)
# -----------------------------
# Step 3: Merge misfit with coordinates
# -----------------------------
df = pd.merge(df_misfit, df_stations, on="sta_name", how="inner")
print(df)

# -----------------------------
# Load event info
# -----------------------------
with open("tensor_info.json") as f:
    event = json.load(f)

event_lon = event["lon"]
event_lat = event["lat"]

# -----------------------------
# Plot global map centered on event
# -----------------------------
# plt.figure(figsize=(10, 10))
components = ["HNE", "HNN", "HNZ", "P", "SH", "skip", "L", "R"]
nc = len(components)
ny = math.ceil(math.sqrt(nc))  # number of columns
nx = math.ceil(nc / ny)  # number of rows

proj_global = ccrs.Orthographic(
    central_longitude=event["lon"], central_latitude=event["lat"]
)
proj_regional = ccrs.PlateCarree()

geo = ccrs.Geodetic()

ny = 2 if nc > 2 else 1
ny = 3
nx = int(np.ceil(nc / ny))

projections = [
    proj_regional if comp.startswith("HN") else proj_global for comp in components
]
fig = plt.figure(figsize=(6 * nx, 5 * ny))
axes = []

for i, proj in enumerate(projections):
    if components[i] == "skip":
        ax = []
    else:
        ax = fig.add_subplot(ny, nx, i + 1, projection=proj)
    axes.append(ax)


# Flatten for easy looping

for i, ax in enumerate(axes):
    comp = components[i]
    if comp == "skip":
        continue
    df_plot = df[df["component"] == comp]

    if not comp.startswith("HN"):
        ax = add_great_circle_radius(ax, event, radius_deg=30)
        ax = add_great_circle_radius(ax, event, radius_deg=60)
        ax.set_global()
    else:
        gl = ax.gridlines(
            draw_labels=True, linewidth=0.6, color="gray", alpha=0.6, linestyle="--"
        )

        gl.top_labels = False
        gl.right_labels = False

        # Set tick spacing (every 1°)
        gl.xlocator = plt.MultipleLocator(1)
        gl.ylocator = plt.MultipleLocator(1)

    ax.coastlines(zorder=0)

    # Scatter stations colored by misfit
    if comp in ["L", "R"]:
        vmax = 0.1
    elif comp == "SH":
        vmax = 0.35
    else:
        vmax = 0.25

    sc = ax.scatter(
        df_plot["longitude"],
        df_plot["latitude"],
        c=df_plot["misfit"],
        cmap=cmc.roma_r,
        s=100,
        edgecolor="k",
        transform=ccrs.PlateCarree(),
        vmin=0.0,
        vmax=vmax,
        zorder=1,
    )

    for idx, row in df_plot.iterrows():
        text_transform = offset_copy(
            ccrs.PlateCarree()._as_mpl_transform(ax),
            units="dots",
            x=10,
            y=0,  # 10 px right & up
        )
        if not args.skip_station_name:
            ax.text(
                row["longitude"],
                row["latitude"],
                row["sta_name"],
                fontsize=8,
                transform=text_transform,
                zorder=2,
            )

    # Plot the event as a red star
    ax.plot(
        event_lon,
        event_lat,
        marker="*",
        color="red",
        markersize=15,
        transform=ccrs.PlateCarree(),
        label="Event",
        zorder=2,
    )

    # Add colorbar
    cbar = plt.colorbar(sc, ax=ax, orientation="vertical", fraction=0.03, pad=0.04)
    cbar.set_label(f"Misfit ({comp})")
ext = args.extension
fn = f"misfit_map.{ext}"
plt.savefig(fn, dpi=200, bbox_inches="tight")
print(f"done writing {fn}")
plt.show()
