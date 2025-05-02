import numpy as np
import matplotlib.pyplot as plt

# Matplotlib settings
plt.rcParams["font.size"] = 13
plt.rcParams["savefig.dpi"] = 500

# Constants
rho = 2700       # density in kg/m^3
g = 9.81         # gravity in m/s^2
z_max = 20_000   # max depth in meters
z = np.linspace(0, z_max, 1000)  # depth in meters
z_km = z / 1000  # convert depth to kilometers

# Effective normal stress σ_n (in MPa)
sigma_n = np.minimum(-1e6, np.maximum(-40e6, -0.4 * rho * g * z)) / 1e6  # in MPa

# Frictional cohesion κ(z)
z_coh = 6000     # in meters
kappa_0 = -0.25   # MPa
kappa_1 = -1.0    # MPa
kappa = kappa_0 + kappa_1 * np.maximum(0, (z_coh - z) / z_coh)

# Plotting
fig, ax1 = plt.subplots(figsize=(6, 6))

# Plot σ_n on primary x-axis
color1 = 'tab:blue'
ax1.plot(sigma_n, z_km, color=color1, label=r'$\sigma_n$ (MPa)')
ax1.set_xlabel('Effective Normal Stress σₙ (MPa)', color=color1)
ax1.set_ylabel('Depth (km)')
ax1.tick_params(axis='x', labelcolor=color1)
ax1.invert_yaxis()  # Depth increases downward
#ax1.grid(True)

# Plot κ on secondary x-axis
ax2 = ax1.twiny()
color2 = 'tab:red'
ax2.plot(kappa, z_km, color=color2, label=r'$\kappa$ (MPa)')
ax2.set_xlabel('Frictional Cohesion κ (MPa)', color=color2)
ax2.tick_params(axis='x', labelcolor=color2)
ax1.set_xlim(-45, 5)

# Title
#plt.title('Depth Dependence of σₙ and κ')
fig.tight_layout()
fn = "depth_vs_sigma_n_cohesion.pdf"
plt.savefig(fn)
print(f"done writing {fn}")
plt.show()

