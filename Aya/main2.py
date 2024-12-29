import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.animation as animation

# Создаем сетку для симуляции
nx, ny = 50, 50
temperature = np.zeros((nx, ny))
source_temp = 100  # Начальная температура источника
temperature[nx//2, ny//2] = source_temp

# Настройка отображения с новым layout
fig = plt.figure(figsize=(12, 8))
gs = fig.add_gridspec(2, 2, height_ratios=[4, 1])
ax_sim = fig.add_subplot(gs[0, 0])  # Симуляция
ax_graph = fig.add_subplot(gs[0, 1])  # График
ax_slider = fig.add_subplot(gs[1, :])  # Слайдер на всю ширину

# История температуры для графика
time_data = []
temp_data = []

# Создаем слайдер
slider = Slider(
    ax=ax_slider,
    label='Температура источника (K)',
    valmin=0,
    valmax=500,
    valinit=source_temp,
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
    
    # Обновляем источник тепла используя значение слайдера
    temperature[nx//2, ny//2] = slider.val
    return temperature

def update(frame):
    # Обновление симуляции
    temp = update_temperature(frame)
    im.set_array(temp)
    
    # Обновление графика
    time_data.append(frame)
    temp_data.append(slider.val)
    line.set_data(time_data, temp_data)
    
    return [im, line]

# Добавляем заголовок под слайдером
ax_slider.text(0.5, -0.5, 'Симуляция нагрева берилия', 
              horizontalalignment='center',
              transform=ax_slider.transAxes,
              fontsize=10)

ani = animation.FuncAnimation(fig, update, frames=200, interval=50, blit=True)
plt.show()
