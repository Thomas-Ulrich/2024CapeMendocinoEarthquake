import numpy as np
import re
from pyproj import Proj
import numpy as np
from scipy.spatial import KDTree
import argparse


def parse_param(filename):
    segments = []
    with open(filename) as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(
            r"#Fault_segment\s*=\s*(\d+)\s+nx\(Along-strike\)=\s*(\d+)\s+Dx\s*=\s*([\d.]+)km\s+ny\(downdip\)=\s*(\d+)\s+Dy\s*=\s*([\d.]+)km",
            line,
        )
        if m:
            seg_id = int(m.group(1))
            nx = int(m.group(2))
            dx = float(m.group(3)) * 1e3  # km -> m
            ny = int(m.group(4))
            dy = float(m.group(5)) * 1e3

            i += 1
            while i < len(lines) and not lines[i].strip().startswith("#Lat"):
                i += 1
            i += 1  # skip #Lat. Lon. ... header

            patches = []
            for _ in range(nx * ny):
                vals = lines[i].split()
                patches.append(
                    {
                        "lat": float(vals[0]),
                        "lon": float(vals[1]),
                        "depth": float(vals[2]) * 1e3,  # km -> m
                        "slip": float(vals[3]) * 1e-2,  # cm -> m
                        "rake": float(vals[4]),
                        "strike": float(vals[5]),
                        "dip": float(vals[6]),
                        "t_rup": float(vals[7]),
                        "t_ris": float(vals[8]),
                        "t_fal": float(vals[9]),
                        "mo": float(vals[10]),
                    }
                )
                i += 1
            segments.append(
                {
                    "id": seg_id,
                    "nx": nx,
                    "ny": ny,
                    "dx": dx,
                    "dy": dy,
                    "patches": patches,
                }
            )
        else:
            i += 1
    return segments


def patch_corners(cx, cy, cz, strike_deg, dip_deg, dx, dy):
    s = np.radians(strike_deg)
    d = np.radians(dip_deg)

    along_stk = np.array([np.sin(s), np.cos(s), 0.0])
    down_dip = np.array(
        [
            np.cos(d) * np.sin(s + np.pi / 2),
            np.cos(d) * np.cos(s + np.pi / 2),
            -np.sin(d),
        ]
    )

    hs = dx / 2.0
    hd = dy / 2.0

    centre = np.array([cx, cy, -cz])

    c0 = centre - hs * along_stk - hd * down_dip  # top-left
    c1 = centre + hs * along_stk - hd * down_dip  # top-right
    c2 = centre + hs * along_stk + hd * down_dip  # bottom-right
    c3 = centre - hs * along_stk + hd * down_dip  # bottom-left

    return [c0, c1, c2, c3]


def write_vtk(segments, outfile, projection, tolerance=1.0):
    """
    Writes out the VTK grid, merging points with an actual physical
    Euclidean distance less than `tolerance` meters using a KDTree.
    """
    proj = Proj(projection)
    unique_points = []
    all_cells = []
    all_slip = []
    all_rake = []
    all_t_rup = []
    all_mo = []

    for seg in segments:
        dx, dy = seg["dx"], seg["dy"]
        for patch in seg["patches"]:
            cx, cy = proj(patch["lon"], patch["lat"])
            cz = patch["depth"]
            corners = patch_corners(cx, cy, cz, patch["strike"], patch["dip"], dx, dy)

            cell_indices = []
            for p in corners:
                if len(unique_points) == 0:
                    # First point ever
                    idx = 0
                    unique_points.append(p)
                else:
                    # Build a temporary spatial tree of current unique points
                    # (Still incredibly fast in Python due to C-optimized KDTree)
                    tree = KDTree(unique_points)

                    # Query if any existing point is within our tolerance distance
                    distance, closest_idx = tree.query(p)

                    if distance < tolerance:
                        # Nearby point found! Reuse its index
                        idx = closest_idx
                    else:
                        # Truly a new point
                        idx = len(unique_points)
                        unique_points.append(p)

                cell_indices.append(idx)

            all_cells.append(cell_indices)
            all_slip.append(patch["slip"])
            all_rake.append(patch["rake"])
            all_t_rup.append(patch["t_rup"])
            all_mo.append(patch["mo"])

    npts = len(unique_points)
    ncells = len(all_cells)

    with open(outfile, "w") as f:
        f.write("# vtk DataFile Version 3.0\n")
        f.write("Kinematic fault model (KDTree Merged Points)\n")
        f.write("ASCII\n")
        f.write("DATASET UNSTRUCTURED_GRID\n\n")

        f.write(f"POINTS {npts} float\n")
        for p in unique_points:
            f.write(f"{p[0]:.3f} {p[1]:.3f} {p[2]:.3f}\n")

        f.write(f"\nCELLS {ncells} {ncells * 5}\n")
        for cell in all_cells:
            f.write(f"4 {cell[0]} {cell[1]} {cell[2]} {cell[3]}\n")

        f.write(f"\nCELL_TYPES {ncells}\n")
        for _ in all_cells:
            f.write("9\n")  # VTK_QUAD

        f.write(f"\nCELL_DATA {ncells}\n")

        for name, data in [
            ("slip_m", all_slip),
            ("rake_deg", all_rake),
            ("t_rup_s", all_t_rup),
            ("moment_Nm", all_mo),
        ]:
            f.write(f"SCALARS {name} float 1\n")
            f.write("LOOKUP_TABLE default\n")
            for v in data:
                f.write(f"{v:.6e}\n")

    print(f"Distance merge complete! Reduced vertex pool down to {npts} unique points.")
    print(f"Written {ncells} patches to {outfile}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse a USGS Solution.param file and output a merged VTK grid."
    )

    # Positional or optional flags
    parser.add_argument(
        "input_file", type=str, help="Path to the input Solution.param file"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="Solution.vtk",
        help="Path for the output VTK file (default: Solution.vtk)",
    )
    parser.add_argument(
        "-t",
        "--tolerance",
        type=float,
        default=1.0,
        help="Distance tolerance in meters for merging nearby vertices (default: 1.0)",
    )
    parser.add_argument(
        "-p",
        "--proj",
        type=str,
        required=True,
        help=f"PROJ projection string or EPSG code)",
    )

    args = parser.parse_args()

    segments = parse_param(args.input_file)
    for s in segments:
        print(
            f"Segment {s['id']}: nx={s['nx']} ny={s['ny']} -> {len(s['patches'])} patches"
        )

    write_vtk(segments, args.output, projection=args.proj, tolerance=args.tolerance)
