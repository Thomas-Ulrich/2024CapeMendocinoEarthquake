import numpy as np
import argparse
import seissolxdmf
import seissolxdmfwriter as sxw
from tqdm import tqdm


class seissolxdmfExtended(seissolxdmf.seissolxdmf):
    def OutputTimes(self):
        """returns the list of output times written in the file"""
        root = self.tree.getroot()
        outputTimes = []
        for Property in root.findall("Domain/Grid/Grid/Time"):
            outputTimes.append(float(Property.get("Value")))
        return outputTimes


def compute_time_indices(sx, at_time):
    """retrive list of time index in file"""
    outputTimes = np.array(sx.OutputTimes())
    lidt = []
    for oTime in at_time:
        idsClose = np.where(np.isclose(outputTimes, oTime, atol=0.0001))
        if not len(idsClose[0]):
            print(f"t={oTime} not found in {sx.xdmfFilename}")
        else:
            lidt.append(idsClose[0][0])
    return lidt


parser = argparse.ArgumentParser(description="compute max dynanmic dCFS")
parser.add_argument("xdmf_filename", help="seissol xdmf file")
parser.add_argument(
    "--end_time",
    nargs=1,
    metavar=("end_time"),
    help="end of time range over which is calculated dCGS",
    type=float,
)

args = parser.parse_args()


sx = seissolxdmfExtended(args.xdmf_filename)
# Compute dCFS with shear traction in the rake direction of the final slip
if args.end_time:
    end_idt = compute_time_indices(sx, [args.end_time[0]])[0]
    print(f"computing dCFS over range 0-{args.end_time[0]}s")
else:
    end_idt = sx.ndt
    print("computing dCFS over the full time range")

Ts0 = sx.ReadData("Ts0", 0)
Td0 = sx.ReadData("Td0", 0)
rake = np.arctan2(Td0, Ts0)
max_dCFS = np.zeros_like(Ts0) - np.inf
dt = sx.ReadTimeStep()
tags = sx.Read1dData("fault-tag", sx.nElements, isInt=True).astype(np.int32)

for i in tqdm(range(end_idt)):
    T_s = sx.ReadData("T_s", i)
    T_d = sx.ReadData("T_d", i)
    P_n = sx.ReadData("P_n", i)
    Shear_in_slip_direction = np.cos(rake) * T_s + np.sin(rake) * T_d
    max_dCFS = np.maximum(Shear_in_slip_direction + 0.6 * P_n, max_dCFS)

n_average = 10
print(f"averaging over the last {n_average} time steps for dCFS")
T_s = 0
T_d = 0
P_n = 0

for i in range(n_average):
    k = sx.ndt - n_average + i
    T_s += sx.ReadData("T_s", k)
    T_d += sx.ReadData("T_d", k)
    P_n += sx.ReadData("P_n", k)

T_s /= n_average
T_d /= n_average
P_n /= n_average

Shear_in_slip_direction = np.cos(rake) * T_s + np.sin(rake) * T_d
dCFS = Shear_in_slip_direction + 0.6 * P_n

sxw.write(
    "max_dyn_dCFS",
    sx.ReadGeometry(),
    sx.ReadConnect(),
    {"dyn_dCFS": max_dCFS, "fault-tag": tags, "dCFS": dCFS},
    {0.0: 0},
    reduce_precision=True,
)
