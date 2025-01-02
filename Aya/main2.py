import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.animation as animation

nx, ny = 50, 50
temperature = np.zeros((nx, ny))
source_temp = 100  # Начальная температура источника
temperature[nx//2, ny//2] = source_temp

fig = plt.figure(figsize=(12, 8))
gs = fig.add_gridspec(2, 2, height_ratios=[5, 0.5])
fig.subplots_adjust(bottom=0.2)

ax_sim = fig.add_subplot(gs[0, 0])    # Симуляция
ax_graph = fig.add_subplot(gs[0, 1])  # График

ax_slider = fig.add_axes([0.25, 0.08, 0.65, 0.03])  # [left, bottom, width, height]

time_data = []
temp_data = []

#слайдер
slider = Slider(
    ax=ax_slider,
    label='Температура источника (K)',
    valmin=0,
    valmax=500,
    valinit=source_temp,
    color='lightblue'
)

# Настройка графиков
im = ax_sim.imshow(temperature, cmap='hot', interpolation='nearest')
line, = ax_graph.plot([], [], 'r-', lw=2)
ax_graph.set_xlim(0, 200)
ax_graph.set_ylim(0, 500)
ax_graph.set_xlabel('Время')
ax_graph.set_ylabel('Температура (K)')
ax_graph.grid(True)

def update_temperature(frame):
    global temperature
    # Диффузия тепла
    laplacian = (np.roll(temperature, +1, 0) + np.roll(temperature, -1, 0) +
                np.roll(temperature, +1, 1) + np.roll(temperature, -1, 1) - 4*temperature)
    temperature += 0.1 * laplacian
    
    temperature[nx//2, ny//2] = slider.val
    return temperature

def update(frame):
    temp = update_temperature(frame)
    im.set_array(temp)
    
    time_data.append(frame)
    temp_data.append(slider.val)
    line.set_data(time_data, temp_data)
    
    return [im, line]

ax_slider.text(0.5, -0.5, 'Симуляция нагрева Берилия',
              horizontalalignment='center',
              transform=ax_slider.transAxes,
              fontsize=10)

ani = animation.FuncAnimation(fig, update, frames=200, interval=50, blit=True)
plt.show()
