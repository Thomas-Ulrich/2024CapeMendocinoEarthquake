import numpy as np
import netCDF4 as nc


def read_casc_txt_file():
    # Load the text file
    data = np.loadtxt("data/casc1.6_velmdl.txt")

    # Extract columns
    x, y, depth, vp, vs = data.T

    # Get unique values for dimensions
    x_unique = np.unique(x)
    y_unique = np.unique(y)
    depth_unique = np.unique(depth)
    nz = depth_unique.shape[0]
    ny = y_unique.shape[0]
    nx = x_unique.shape[0]
    print((nz, ny, nx))
    del x, y, depth

    vp = vp.reshape((nz, ny, nx))
    vs = vs.reshape((nz, ny, nx))
    return x_unique, y_unique, depth_unique, vp, vs


x_unique, y_unique, depth_unique, vp, vs = read_casc_txt_file()

# Create NetCDF file
with nc.Dataset("data/casc1.6_full.nc", "w", format="NETCDF4") as ds:
    ds.createDimension("x", len(x_unique))
    ds.createDimension("y", len(y_unique))
    ds.createDimension("depth", len(depth_unique))

    x_var = ds.createVariable("x", "f4", ("x",))
    y_var = ds.createVariable("y", "f4", ("y",))
    depth_var = ds.createVariable("depth", "f4", ("depth",))
    vp_var = ds.createVariable("vp", "f4", ("depth", "y", "x"))
    vs_var = ds.createVariable("vs", "f4", ("depth", "y", "x"))

    x_var[:] = x_unique
    y_var[:] = y_unique
    depth_var[:] = depth_unique
    vp_var[:, :, :] = vp
    vs_var[:, :, :] = vs
