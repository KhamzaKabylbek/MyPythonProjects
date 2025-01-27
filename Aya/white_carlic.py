import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def create_white_dwarf_visualization():
    # White dwarf parameters
    radius = 0.01  # Radius in solar radii
    density = 1e9   # Density in kg/m^3

    # Create a grid for the 3D visualization
    phi = np.linspace(0, np.pi, 100)
    theta = np.linspace(0, 2 * np.pi, 100)
    phi, theta = np.meshgrid(phi, theta)

    # Calculate the coordinates
    x = radius * np.sin(phi) * np.cos(theta)
    y = radius * np.sin(phi) * np.sin(theta) 
    z = radius * np.cos(phi)

    # Create the 3D visualization
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Use a single color to represent the white dwarf
    surf = ax.plot_surface(x, y, z, color='#87CEEB', alpha=0.8)
    
    # Customize the axes
    ax.set_title('Realistic 3D Visualization of a White Dwarf Star')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_zlim(-radius, radius)

    plt.tight_layout()
    plt.show()

# Run the visualization
create_white_dwarf_visualization()