import pyvista as pv

fn = "../seissol_outputs/dip80/dyn_0007_coh0.25_1.0_B0.9_C0.2_R0.6_3d_24mdip80_SR-fault.xdmf"
mesh = pv.read(fn)

# Extract ONLY boundary edges (edges used by exactly one cell)
boundary = mesh.extract_feature_edges(
    boundary_edges=True,      # ✔ only edges used by one triangle
    feature_edges=False,
    non_manifold_edges=False,
    manifold_edges=False
)

outfn = "edges.vtk"
boundary.save(outfn)
print(f"Saved: {outfn}")
