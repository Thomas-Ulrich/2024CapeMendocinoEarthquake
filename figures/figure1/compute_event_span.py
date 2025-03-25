import h5py
import numpy as np
import argparse
from seissolxdmf import seissolxdmf
from pyproj import Transformer


class seissolxdmfExtended(seissolxdmf):
    def compute_centers(self):
        xyz = self.ReadGeometry()
        connect = self.ReadConnect()
        return (xyz[connect[:, 0]] + xyz[connect[:, 1]] + xyz[connect[:, 2]]) / 3.0


parser = argparse.ArgumentParser(description="find range of rupture in lon, lat")
parser.add_argument("filename", help="seissol output file name")
args = parser.parse_args()

sx = seissolxdmfExtended(args.filename)
xyz, connect = sx.ReadGeometry(), sx.ReadConnect()
centers = sx.compute_centers()
transformer = Transformer.from_crs(
    "+proj=tmerc +datum=WGS84 +k=0.9996 +lon_0=-125.02 +lat_0=40.37",
    "epsg:4326",
    always_xy=True,
)
lon, lat = transformer.transform(centers[:, 0], centers[:, 1])

slip = sx.ReadData("ASl", sx.ndt - 1)
ids = np.where(slip > 0.5)[0]

ar = lon[ids]
lon_min, lon_max = np.amin(ar), np.amax(ar)
ar = lat[ids]
lat_min, lat_max = np.amin(ar), np.amax(ar)

output = (
    "span_2024={"
    + f"'lon':[{lon_min:.3f}, {lon_max:.3f}], 'lat':[{lat_max:.3f}, {lat_min:.3f}]"
    + "}"
)
print(output)
