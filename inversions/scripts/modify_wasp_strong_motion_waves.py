#!/usr/bin/env python3
import argparse
import json
from obspy.taup import TauPyModel

def estimate_travel_time(source_depth_in_km, distance_in_degree, station, phase="P"):
    taupModel = "ak135"
    model = TauPyModel(model=taupModel)
    tP = model.get_travel_times(
        source_depth_in_km=source_depth_in_km,
        distance_in_degree=distance_in_degree,
        phase_list=[phase],
    )
    if not tP:
        print(f"no P wave at station {station}")
        tP = 0.0
    else:
        tP = tP[0].time
    return tP


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="update strong_motion_waves.json if available"
    )
    parser.add_argument("hypo_depth_in_km", help="hypocenter depth", type=float)
    args = parser.parse_args()

    fn = "strong_motion_waves.json"
    hypo_depth_in_km = args.hypo_depth_in_km

    with open(fn, "r") as f:
        data = json.load(f)
    # Update the duration for each entry
    for entry in data:
        station_name = entry["name"]
        dist = entry["distance"]
        tP = estimate_travel_time(hypo_depth_in_km, dist, station_name, "P")
        print(station_name, dist, tP)
        if tP == 0.0:
            # station too close
            tP = 5.0
        # 1.2 because our model is much slower than tauP
        entry["duration"] = int((1.2*tP + 50.0) / 2.0) * 10
        # used in first submission model
        # entry["duration"] = int((tP + 50.0) / 2.0) * 10

    with open(fn, "w") as f:
        json.dump(data, f, indent=4)
    print(f"done updating {fn}")
