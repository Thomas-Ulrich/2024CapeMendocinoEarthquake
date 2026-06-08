import json
import csv
import os

files_to_process = {
    "SM": "strong_motion_waves.json",
    "GPS": "static_data.json",
    "body": "tele_waves.json",
    "surf": "surf_waves.json",
}

output_file = "kinematic_inv_stations.csv"
seen_stations = set()
csv_rows = []

for station_type, filename in files_to_process.items():
    if not os.path.exists(filename):
        print(f"Warning: {filename} not found, skipping.")
        continue

    with open(filename, "r") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"Error parsing {filename}: {e}")
            continue

        for entry in data:
            name = entry.get("name")
            location = entry.get("location")  # Structure: [lat, lon]
            weight = entry.get("trace_weight")

            # --- Weight Filtering Logic ---
            # For GPS data, trace_weight is a list of strings like ["0.5", "1.0", "1.0"]
            if isinstance(weight, list):
                try:
                    # Keep if at least one component has a non-zero weight
                    is_used = any(float(w) > 0.0 for w in weight)
                except (ValueError, TypeError):
                    is_used = True  # Fallback to true if parsing string fails
            else:
                # For SM, body, surf where trace_weight is a number or string
                try:
                    is_used = float(weight) > 0.0 if weight is not None else True
                except (ValueError, TypeError):
                    is_used = True

            if not is_used:
                continue  # Skip stations with weight 0

            if name and location and len(location) == 2:
                lat, lon = location[0], location[1]

                station_key = (station_type, name)
                if station_key not in seen_stations:
                    seen_stations.add(station_key)
                    csv_rows.append(
                        {"type": station_type, "id": name, "lat": lat, "lon": lon}
                    )

with open(output_file, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["type", "id", "lat", "lon"])
    writer.writeheader()
    for row in csv_rows:
        writer.writerow(row)

from collections import Counter

type_counts = Counter(row["type"] for row in csv_rows)
for t, n in sorted(type_counts.items()):
    print(f"  {t}: {n} stations")

print(
    f"Successfully generated {output_file} with {len(csv_rows)} active stations (weight > 0)."
)
