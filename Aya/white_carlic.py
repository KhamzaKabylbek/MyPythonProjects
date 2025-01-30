<<<<<<< HEAD

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap

def create_white_dwarf_visualization():
    # Реалистичные параметры белого карлика
    radius = 0.01  # Радиус в солнечных радиусах
    temperature = 25000  # Температура поверхности в Кельвинах
    
    # Создание сетки для 3D визуализации
    phi = np.linspace(0, np.pi, 200)
    theta = np.linspace(0, 2 * np.pi, 200)
    phi, theta = np.meshgrid(phi, theta)

    # Расчет координат
    x = radius * np.sin(phi) * np.cos(theta)
    y = radius * np.sin(phi) * np.sin(theta)
    z = radius * np.cos(phi)

    # Создание градиента температуры
    temperature_gradient = np.sin(phi) # Градиент от центра к краям
    
    # Создание пользовательской цветовой карты
    colors = [(1, 1, 1), (0.95, 0.95, 1), (0.85, 0.85, 1), (0.7, 0.7, 1)]
    custom_cmap = LinearSegmentedColormap.from_list('white_dwarf', colors)

    # Создание 3D визуализации
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Отрисовка поверхности с градиентом
    surf = ax.plot_surface(x, y, z, 
                          facecolors=custom_cmap(temperature_gradient),
                          alpha=0.9,
                          antialiased=True,
                          rstride=1,
                          cstride=1)

    # Добавление свечения
    ax.plot_surface(x*1.01, y*1.01, z*1.01,
                    color='white',
                    alpha=0.1,
                    antialiased=True)

    # Настройка освещения и перспективы
    ax.view_init(elev=20, azim=45)
    
    # Настройка осей
    ax.set_title(f'Realistic White Dwarf Star\nSurface Temperature: {temperature}K')
    ax.set_xlabel('X (Solar Radii)')
    ax.set_ylabel('Y (Solar Radii)')
    ax.set_zlabel('Z (Solar Radii)')
    
    # Удаление сетки и настройка фона
    ax.grid(False)
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    
    # Установка равных масштабов осей
    ax.set_box_aspect([1,1,1])
    
    plt.show()

if __name__ == "__main__":
    create_white_dwarf_visualization()
=======
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
>>>>>>> origin/main
