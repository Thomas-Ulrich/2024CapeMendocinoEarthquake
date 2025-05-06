import seissolxdmf as sx
import argparse
import numpy as np

parser = argparse.ArgumentParser(
    description="compute fault area (area that slip more than 1cm"
)

parser.add_argument(
    "fault",
    help="fault output filename (xdmf)",
)
parser.add_argument(
    "energy",
    help="energy output filename (csv)",
)
args = parser.parse_args()

sx = sx.seissolxdmf(args.fault)
xyz = sx.ReadGeometry()
connect = sx.ReadConnect()

cross0 = np.cross(
    xyz[connect[:, 1], :] - xyz[connect[:, 0], :],
    xyz[connect[:, 2], :] - xyz[connect[:, 0], :],
)
face_area = 0.5 * np.apply_along_axis(np.linalg.norm, 1, cross0)

ndt = sx.ReadNdt()
slip = sx.ReadData("ASl", ndt - 1)

slip_thres = 0.01
face_area = face_area[slip > slip_thres]
ruptured_area = np.sum(face_area)


def pivot_if_necessary(df):
    if "variable" in df:
        # the format of the energy output changed following PR #773 (02.2023), allowing
        # to compute volume energies less frequently
        return df.pivot_table(index="time", columns="variable", values="measurement")
    else:
        return df


"""
# for reference but it does not work
relevant_quantities = [
    "total_frictional_work",
    "static_frictional_work",
]
energy = pd.read_csv(args.energy)
energy = pivot_if_necessary(energy)
energy = energy[relevant_quantities]
total_frictional_work = energy["total_frictional_work"].iloc[-1]
static_frictional_work = energy["static_frictional_work"].iloc[-1]
G = (2 * static_frictional_work - total_frictional_work) / ruptured_area
print(f"rupture area: {ruptured_area/1e6} km2, fracture energy Gc={G:e}")
"""

Pn0 = sx.ReadData("T_n", 0)[slip > slip_thres]
mus = sx.ReadData("mu_s", 0)[slip > slip_thres]
mud = sx.ReadData("Mud", 0)[slip > slip_thres]

ASl = slip[slip > slip_thres]
dc = sx.ReadData("d_c", 0)[slip > slip_thres]
dc = np.minimum(dc, ASl)

Gc = np.sum(-(mus - mud) * face_area * dc * Pn0 * 0.5)
Gc /= ruptured_area
average_slip = np.sum(face_area * slip[slip > slip_thres])
average_slip /= ruptured_area
print(f"average slip {average_slip}")
print(f"fracture energy from based on delta_mu * dc * sigma_n: {Gc:e}")
