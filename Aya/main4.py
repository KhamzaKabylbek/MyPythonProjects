import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import csv
from datetime import datetime

# Параметры сетки и начальные условия
nx, ny = 40, 40  # Уменьшенный размер сетки для лучшей производительности
temperature = np.zeros((nx, ny))
source_temp = 100  # Начальная температура источника
temperature[nx//2, ny//2] = source_temp

# Создание фигуры и областей
fig = plt.figure(figsize=(18, 10))
gs = fig.add_gridspec(3, 3, height_ratios=[5, 0.5, 2])
fig.subplots_adjust(bottom=0.25)

# Создание осей для графиков
ax_sim = fig.add_subplot(gs[0, 0])    # Симуляция температуры
ax_graph_temp = fig.add_subplot(gs[0, 2])  # График температуры
ax_graph_optical = fig.add_subplot(gs[2, :])  # График оптических свойств
ax_3d = fig.add_subplot(gs[0, 1], projection='3d')  # 3D визуализация температуры

# Создание слайдеров
ax_slider_temp = fig.add_axes([0.25, 0.15, 0.65, 0.03])
ax_slider_coef = fig.add_axes([0.25, 0.1, 0.65, 0.03])

# Данные для графиков
x = np.arange(nx)
y = np.arange(ny)
x, y = np.meshgrid(x, y)

# Динамические данные
time_data = []
temp_data = []
absorption_data = []
reflection_data = []

# Настройка слайдеров
slider_temp = Slider(
    ax=ax_slider_temp,
    label='Температура источника (K)',
    valmin=0,
    valmax=500,
    valinit=source_temp,
    color='lightblue'
)

slider_coef = Slider(
    ax=ax_slider_coef,
    label='Коэффициент теплопередачи',
    valmin=0.01,
    valmax=0.5,
    valinit=0.1,
    color='lightgreen'
)

# Настройка графиков
im = ax_sim.imshow(temperature, cmap='hot', interpolation='nearest')
plt.colorbar(im, ax=ax_sim, label='Температура (K)')
ax_sim.set_title('2D Распределение температуры')

# Инициализация 3D поверхности
surf = ax_3d.plot_surface(x, y, temperature, cmap='hot', rstride=1, cstride=1)
ax_3d.set_title("3D визуализация температуры")
ax_3d.set_xlabel("X")
ax_3d.set_ylabel("Y")
ax_3d.set_zlabel("Температура (K)")

# Настройка графиков
line_temp, = ax_graph_temp.plot([], [], 'r-', lw=2, label='Температура (K)')
line_abs, = ax_graph_optical.plot([], [], 'b-', lw=2, label='Поглощение')
line_ref, = ax_graph_optical.plot([], [], 'g-', lw=2, label='Отражение')

ax_graph_temp.set_xlim(0, 200)
ax_graph_temp.set_ylim(0, 500)
ax_graph_temp.set_xlabel('Время (с)')
ax_graph_temp.set_ylabel('Температура (K)')
ax_graph_temp.grid(True)
ax_graph_temp.legend(loc='upper left')

ax_graph_optical.set_xlim(0, 200)
ax_graph_optical.set_ylim(0, 1)
ax_graph_optical.set_xlabel('Время (с)')
ax_graph_optical.set_ylabel('Оптические свойства')
ax_graph_optical.grid(True)
ax_graph_optical.legend(loc='upper right')

# Создание файла для логирования
log_filename = f'temperature_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
with open(log_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Time', 'Temperature', 'Absorption', 'Reflection'])

def calculate_absorption(temp):
    return np.clip(0.8 * np.exp(-temp / 300), 0, 1)

def calculate_reflection(temp):
    return np.clip(0.2 + 0.1 * np.sin(temp / 100), 0, 1)

def update_temperature(frame):
    global temperature, surf
    laplacian = (np.roll(temperature, +1, 0) + np.roll(temperature, -1, 0) +
                 np.roll(temperature, +1, 1) + np.roll(temperature, -1, 1) - 4*temperature)
    temperature += slider_coef.val * laplacian
    temperature[nx//2, ny//2] = slider_temp.val
    return temperature

def update(frame):
    global surf
    temp = update_temperature(frame)
    
    # Обновление 2D визуализации
    im.set_array(temp)
    
    # Обновление 3D визуализации
    ax_3d.clear()
    surf = ax_3d.plot_surface(x, y, temp, cmap='hot', rstride=1, cstride=1)
    ax_3d.set_title("3D визуализация температуры")
    ax_3d.set_xlabel("X")
    ax_3d.set_ylabel("Y")
    ax_3d.set_zlabel("Температура (K)")
    ax_3d.view_init(elev=20, azim=frame % 360)  # Вращение графика
    
    # Обновление данных графиков
    time_data.append(frame)
    current_temp = slider_temp.val
    temp_data.append(current_temp)
    
    current_absorption = calculate_absorption(current_temp)
    current_reflection = calculate_reflection(current_temp)
    
    absorption_data.append(current_absorption)
    reflection_data.append(current_reflection)
    
    line_temp.set_data(time_data, temp_data)
    line_abs.set_data(time_data, absorption_data)
    line_ref.set_data(time_data, reflection_data)
    
    # Добавление текстовой информации
    ax_sim.set_title(f'Время: {frame}с\nТемпература источника: {current_temp:.1f}K')
    
    # Логирование данных
    with open(log_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([frame, current_temp, current_absorption, current_reflection])
    
    return [im, line_temp, line_abs, line_ref]

# Добавление общего заголовка
fig.suptitle('Симуляция нагрева бериллия и оптических свойств', fontsize=14)

# Создание анимации
ani = animation.FuncAnimation(fig, update, frames=200, interval=100, blit=True)

plt.show()