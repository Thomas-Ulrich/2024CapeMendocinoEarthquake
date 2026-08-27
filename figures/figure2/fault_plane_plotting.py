import numpy as np


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


def plot_pygmt_fault_planes_background(fig, solution_file):
    segments = extract_segment_coords_from_solution(solution_file)

    # --- PASS 1: Plot all semi-transparent fault plane polygons ---
    for seg_id, coords in segments.items():
        col = "#4A0E17" if seg_id == 1 else "#0D2B1D"

        fig.plot(
            x=coords[:, 0],
            y=coords[:, 1],
            fill="black",
            transparency=60,
            # pen=f"0.5p,{col},--", # Submerged dashed outline
        )


def plot_pygmt_fault_planes_trace(fig, solution_file):
    segments = extract_segment_coords_from_solution(solution_file)
    # --- PASS 2: Overlay all solid surface traces on top ---
    for seg_id, coords in segments.items():
        col = "#4A0E17" if seg_id == 1 else "#0D2B1D"

        min_depth = np.min(coords[:, 2])
        is_surface = coords[:, 2] == min_depth

        if np.any(is_surface):
            fig.plot(
                x=coords[is_surface, 0],
                y=coords[is_surface, 1],
                pen=f"2.5p,{col},solid",  # Strong solid line for top edge
            )


def plot_pygmt_fault_planes(fig, solution_file):
    plot_pygmt_fault_planes_background(fig, solution_file)
    plot_pygmt_fault_planes_trace(fig, solution_file)
