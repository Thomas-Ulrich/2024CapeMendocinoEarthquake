import numpy as np
import pandas as pd
import argparse
import seissolxdmf
from pyproj import Transformer
import scipy.interpolate as interp


def read_seissol_surface_data(xdmfFilename):
    """read unstructured free surface output and associated data.
    compute cell_barycenter"""
    sx = seissolxdmf.seissolxdmf(xdmfFilename)
    xyz = sx.ReadGeometry()
    connect = sx.ReadConnect()

    U = sx.ReadData("u1", sx.ndt - 1)
    V = sx.ReadData("u2", sx.ndt - 1)
    W = sx.ReadData("u3", sx.ndt - 1)

    # project the data to geocentric (lat, lon)
    myproj = "+proj=tmerc +datum=WGS84 +k=0.9996 +lon_0=-125.02 +lat_0=40.37"
    transformer = Transformer.from_crs(myproj, "epsg:4326", always_xy=True)
    lons, lats = transformer.transform(xyz[:, 0], xyz[:, 1])
    xy = np.vstack((lons, lats)).T

    # compute triangule barycenter
    lonlat_barycenter = (
        xy[connect[:, 0], :] + xy[connect[:, 1], :] + xy[connect[:, 2], :]
    ) / 3.0

    return lons, lats, lonlat_barycenter, connect, U, V, W


def interpolate_seissol_surf_output(lonlat_barycenter, U, df):
    """interpolate SeisSol free surface output to GPS data location"""

    Fvsm = interp.LinearNDInterpolator(lonlat_barycenter, U)
    locGPS = np.vstack((df["lon"].to_numpy(), df["lat"].to_numpy())).T

    Fvsm = interp.LinearNDInterpolator(lonlat_barycenter, U)
    ui = Fvsm.__call__(locGPS)
    Fvsm = interp.LinearNDInterpolator(lonlat_barycenter, V)
    vi = Fvsm.__call__(locGPS)
    Fvsm = interp.LinearNDInterpolator(lonlat_barycenter, W)
    wi = Fvsm.__call__(locGPS)
    df["E_syn"] = ui
    df["N_syn"] = vi
    df["Up_syn"] = wi

    return df

parser = argparse.ArgumentParser(
    description="extract displacement at GNSS station from seissol surface output"
)
parser.add_argument(
    "--gnss_data", help="SeisSol xdmf surface file", default="gnss_data.csv"
)

parser.add_argument("seissol_surface_output", help="SeisSol xdmf surface file")


args = parser.parse_args()

# Read GPS data
df = pd.read_csv(args.gnss_data, skiprows=[1])
print(df)

# Read SeisSol output and interpolate output to GPS data point locations
lons, lats, lonlat_barycenter, connect, U, V, W = read_seissol_surface_data(
    args.seissol_surface_output
)
df = interpolate_seissol_surf_output(lonlat_barycenter, U, df)
print(df)
# Select only the desired columns and rename them
df_out = df[["id", "lon", "lat", "E_syn", "N_syn", "Up_syn"]].copy()
df_out = df_out.rename(columns={"E_syn": "E", "N_syn": "N", "Up_syn": "Up"})
df_out = df_out.dropna()

df_out.to_csv("gnss_data_preferred_DR.csv", index=False)
