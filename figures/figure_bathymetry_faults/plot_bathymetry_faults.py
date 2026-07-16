import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import matplotlib.ticker as mticker


def extract_segment_coords_from_solution(file_path):
    segments = {}
    current_segment_id = None
    inside_boundary = False

    with open(file_path, "r") as file:
        for line in file:
            line_clean = line.strip()

            # 1. Detect when a new Fault Segment starts and extract its ID
            if "#Fault_segment =" in line_clean:
                parts = line_clean.split()
                try:
                    eq_idx = parts.index("=")
                    current_segment_id = int(parts[eq_idx + 1])
                    segments[current_segment_id] = []
                except (ValueError, IndexError):
                    continue

            # 2. Trigger the start of boundary reading
            elif (
                "Lon." in line_clean and "Lat." in line_clean and "Depth" in line_clean
            ):
                inside_boundary = True
                continue

            # 3. Stop reading boundary coordinates when hitting the next commented header
            elif inside_boundary and line_clean.startswith("#"):
                inside_boundary = False
                continue

            # 4. Append points to the active segment list
            elif inside_boundary and line_clean and current_segment_id is not None:
                coords = [float(val) for val in line_clean.split()]
                if len(coords) == 3:
                    segments[current_segment_id].append(coords)

    # Convert all list values to NumPy arrays before returning
    return {seg_id: np.array(coords_list) for seg_id, coords_list in segments.items()}


file_path = "../../geometry/GEBCO_26_Feb_2025_0a84c2ff5ea2/gebco_2024_n43.0_s38.0_w-128.0_e-121.0.nc"

ds = xr.open_dataset(file_path)
elevation_var = "elevation" if "elevation" in ds else "z"
topo = ds[elevation_var]

topo_subset = ds[elevation_var].sel(lon=slice(-125.5, -123.8), lat=slice(39.8, 40.9))

# Define PlateCarree projection for data mapping, Mercator for the map display
data_crs = ccrs.PlateCarree()
map_crs = ccrs.Mercator()

fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={"projection": map_crs})

# Plot topographic background
im = ax.pcolormesh(
    topo_subset.lon,
    topo_subset.lat,
    topo_subset,
    cmap="terrain",
    transform=data_crs,
    shading="auto",
    vmax=2000,
)

# Add geographical details
ax.add_feature(cfeature.COASTLINE, edgecolor="black", linewidth=1.0)
ax.add_feature(cfeature.BORDERS, linestyle=":")

gl = ax.gridlines(
    draw_labels=True, x_inline=False, y_inline=False, linestyle="--", alpha=0.5
)
gl.top_labels = False
gl.right_labels = False
gl.xformatter = mticker.FormatStrFormatter("%.2f°")
gl.yformatter = mticker.FormatStrFormatter("%.2f°")
gl.xlocator = mticker.MultipleLocator(0.25)
gl.ylocator = mticker.MultipleLocator(0.25)

# Add Colorbar
cbar = plt.colorbar(im, ax=ax, orientation="horizontal", pad=0.08, shrink=0.7)
cbar.set_label("Elevation (m)")

# Extract Longitude (col 0) and Latitude (col 1) separately, and specify the transform
# ax.plot(all_segments[1][:, 0], all_segments[1][:, 1], transform=data_crs, label="Segment 1", color="red", linewidth=2)
# ax.plot(all_segments[2][:, 0], all_segments[2][:, 1], transform=data_crs, label="Segment 2", color="blue", linewidth=2)
file_name = "../figure2/Solution.param"
all_segments = extract_segment_coords_from_solution(file_name)
file_name = "../figure2/Solution_newdipm85_strike100_21.param"
all_segments_2 = extract_segment_coords_from_solution(file_name)
all_segments[0] = all_segments_2[1]


for seg_id, color, label in [
    (0, "black", "Mendocino TF (one fault geometry)"),
    (1, "red", "Mendocino TF (two-fault geometry)"),
    (2, "blue", "cross-cutting splay fault (two-fault geometry)"),
]:
    coords = all_segments[seg_id]

    # 1. Find the surface mask
    min_depth = np.min(coords[:, 2])
    is_surface = coords[:, 2] == min_depth

    # 2. Plot the ENTIRE closed loop as a dashed line (Sides + Bottom)
    # We append the first point to the end to make sure the loop completely closes
    closed_coords = np.vstack([coords, coords[0]])
    ax.plot(
        closed_coords[:, 0],
        closed_coords[:, 1],
        transform=data_crs,
        color=color,
        linestyle="--",
        linewidth=1.5,
        alpha=0.8,
    )

    # 3. Overlay the surface trace as a solid line
    if np.any(is_surface):
        ax.plot(
            coords[is_surface, 0],
            coords[is_surface, 1],
            transform=data_crs,
            color=color,
            linestyle="-",
            linewidth=2.5,  # Slightly thicker so it stands out on top
            label=label,
        )


ax.legend(loc="upper right")

ax.set_aspect("equal", adjustable="box")
plt.show()
