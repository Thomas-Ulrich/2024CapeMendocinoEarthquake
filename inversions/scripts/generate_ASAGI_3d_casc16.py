import numpy as np
from netCDF4 import Dataset
from scipy.interpolate import RegularGridInterpolator
from pyproj import Transformer
from asagiwriter import writeNetcdf


def extend_z_vp(z, vp, n_added=3):
    """extend z array towards positive depth, as well as data array"""
    vp_new = np.zeros((vp.shape[0] + n_added, vp.shape[1], vp.shape[2]))
    vp_new[n_added:, :, :] = vp[:, :, :]
    for i in range(n_added):
        vp_new[i:, :, :] = vp[n_added, :, :]
    z_new = np.concatenate((-z[n_added:0:-1], z))
    return z_new, vp_new


def fill(data, invalid=None):
    from scipy import ndimage as nd

    """
    Replace the value of invalid 'data' cells (indicated by 'invalid')
    by the value of the nearest valid data cell

    Input:
        data:    numpy array of any dimension
        invalid: a binary array of same shape as 'data'.
                 data value are replaced where invalid is True
                 If None (default), use: invalid  = np.isnan(data)

    Output:
        Return a filled array.
    https://stackoverflow.com/questions/5551286/filling-gaps-in-a-numpy-array/9262129#9262129
    """
    if invalid is None:
        invalid = np.isnan(data)
    ind = nd.distance_transform_edt(
        invalid, return_distances=False, return_indices=True
    )
    return data[tuple(ind)]


def ProjectData2utm(x, y, z, vp, myproj):
    # reproject grid
    nz, ny, nx = vp.shape
    utm_zone10N = "EPSG:32610"
    transformer = Transformer.from_crs(utm_zone10N, myproj, always_xy=True)
    transformer_inv = Transformer.from_crs(myproj, utm_zone10N, always_xy=True)
    Xlim, Ylim = transformer.transform([x[0], x[-1]], [y[0], y[-1]])
    X_utm = np.linspace(Xlim[0], Xlim[1], nx)
    Y_utm = np.linspace(Ylim[0], Ylim[1], ny)
    Xg, Yg = np.meshgrid(X_utm, Y_utm)
    glon_grid, glat_grid = transformer_inv.transform(Xg.flatten(), Yg.flatten())
    coords_grid = np.column_stack((glon_grid, glat_grid))

    vp_utm = np.zeros((nz, ny, nx))

    for k in range(0, nz):
        mydata = fill(vp[k, :, :].T)
        fVp = RegularGridInterpolator(
            (x, y), mydata, fill_value=np.nanmean(mydata), bounds_error=False
        )
        VPg = fVp(coords_grid)
        VPg = VPg.reshape(np.shape(Xg))
        vp_utm[k, :, :] = VPg
    return X_utm, Y_utm, z, vp_utm


file_path = "data/casc1.6-velmdl.r1.1-n4.nc"
with Dataset(file_path, mode="r") as nc_file:
    # Read variables
    x = nc_file.variables["x"][:]
    y = nc_file.variables["y"][:]
    z = -nc_file.variables["depth"][:].astype(float)
    vp = nc_file.variables["Vp"][:] / 1000.0  # P-wave velocity
    vs = nc_file.variables["Vs"][:] / 1000.0  # S-wave velocity
    nz, ny, nx = vp.shape

    newny = int(ny * 0.2)
    vs = vs[:, 0:newny, :]
    vp = vp[:, 0:newny, :]
    y = y[0:newny]

    # Remove water layer
    nz, ny, nx = vp.shape
    for j in range(ny):
        for i in range(nx):
            first_non_zero = np.where(vs[:, j, i] > 0)[0]
            if first_non_zero.size > 0:
                first_index = first_non_zero[0]
                # Set water layer to first non-zero value
                vs[0:first_index, j, i] = vs[first_index, j, i]
                vp[0:first_index, j, i] = vp[first_index, j, i]

    # Extend the model towards y min
    num_layers_to_add = newny
    idxmin = 0  # Assuming idxmin corresponds to the minimum index along the y-axis
    vs_extension = np.repeat(vs[:, idxmin : idxmin + 1, :], num_layers_to_add, axis=1)
    vp_extension = np.repeat(vp[:, idxmin : idxmin + 1, :], num_layers_to_add, axis=1)
    y_extension = np.linspace(
        y[0] - num_layers_to_add * (y[1] - y[0]),
        y[0] - (y[1] - y[0]),
        num_layers_to_add,
    )

    print(vs.shape)
    # Concatenate the extensions to the original arrays
    vs = np.concatenate((vs_extension, vs), axis=1)
    vp = np.concatenate((vp_extension, vp), axis=1)
    y = np.concatenate((y_extension, y))
    print(vs.shape)


myproj = "+proj=tmerc +datum=WGS84 +k=0.9996 +lon_0=-125.02 +lat_0=40.37"
X_utm, Y_utm, Z_utm, vp_utm = ProjectData2utm(x, y, z, vp, myproj)
X_utm, Y_utm, Z_utm, vs_utm = ProjectData2utm(x, y, z, vs, myproj)

# Compute rho from vp
rho = (
    1.6612 * vp_utm
    - 0.4721 * vp_utm**2
    + 0.0671 * vp_utm**3
    - 0.0043 * vp_utm**4
    + 0.000106 * vp_utm**5
)
VP, VS, rho = 1000 * vp_utm, 1000 * vs_utm, 1000 * rho


# Comupute Lame parameter
mu = rho * VS * VS
lambdax = rho * (VP**2 - 2.0 * VS**2)

prefix = "casc16"

for i, var in enumerate(["Vp", "Vs", "rho"]):
    writeNetcdf(
        f"{prefix}_{var}",
        [X_utm, Y_utm, Z_utm],
        [var],
        [[VP, VS, rho][i]],
        paraview_readable=True,
    )

writeNetcdf(
    f"{prefix}_ASAGI",
    [X_utm, Y_utm, Z_utm],
    ["rho", "mu", "lambda"],
    [rho, mu, lambdax],
    paraview_readable=False,
)
