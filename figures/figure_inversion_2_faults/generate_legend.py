import matplotlib.pyplot as plt

plt.rc("axes", titlesize=14)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("font", size=20)


# Create a figure
fig, ax = plt.subplots()

# Create two Line2D objects just for the legend
from matplotlib.lines import Line2D

legend_elements = [
    Line2D([0], [0], color='red', lw=2, label='CCVMv1.6 velocity model'),
    Line2D([0], [0], color='blue', lw=2, label='default velocity model')
]

# Hide axes
ax.axis('off')

# Add legend
ax.legend(handles=legend_elements, loc='center')

# Adjust layout
plt.tight_layout()

# Show the figure
plt.savefig("legend.svg", bbox_inches='tight')
plt.show()
