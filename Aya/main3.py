import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

# Параметры сетки и начальные условия
nx, ny = 50, 50
temperature = np.zeros((nx, ny))
source_temp = 100  # Начальная температура источника
temperature[nx//2, ny//2] = source_temp

# Создание фигуры и областей
fig = plt.figure()
fig.set_size_inches(18, 10)
fig_manager = plt.get_current_fig_manager()
fig_manager.full_screen_toggle()
gs = fig.add_gridspec(3, 3, height_ratios=[5, 0.5, 2])
fig.subplots_adjust(bottom=0.2)

ax_sim = fig.add_subplot(gs[0, 0])    # Симуляция температуры
ax_graph_temp = fig.add_subplot(gs[0, 2])  # График температуры
ax_graph_optical = fig.add_subplot(gs[2, :])  # График оптических свойств
ax_3d = fig.add_subplot(gs[0, 1], projection='3d')  # 3D визуализация температуры

ax_slider = fig.add_axes([0.25, 0.08, 0.65, 0.03])  # Слайдер температуры источника

# Данные для графиков
x = np.arange(nx)
y = np.arange(ny)
x, y = np.meshgrid(x, y)

# Динамические данные
time_data = []
temp_data = []
absorption_data = []
reflection_data = []

# Слайдер
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
line_temp, = ax_graph_temp.plot([], [], 'r-', lw=2, label='Температура (K)')
line_abs, = ax_graph_optical.plot([], [], 'b-', lw=2, label='Поглощение')
line_ref, = ax_graph_optical.plot([], [], 'g-', lw=2, label='Отражение')

ax_graph_temp.set_xlim(0, 200)
ax_graph_temp.set_ylim(0, 500)
ax_graph_temp.set_xlabel('Время')
ax_graph_temp.set_ylabel('Температура (K)')
ax_graph_temp.grid(True)

ax_graph_optical.set_xlim(0, 200)
ax_graph_optical.set_ylim(0, 1)
ax_graph_optical.set_xlabel('Время')
ax_graph_optical.set_ylabel('Оптические свойства')
ax_graph_optical.grid(True)
ax_graph_optical.legend()

# Функции расчета оптических свойств
def calculate_absorption(temp):
    # Простая модель зависимости поглощения от температуры
    return np.clip(0.8 * np.exp(-temp / 300), 0, 1)

def calculate_reflection(temp):
    # Простая модель зависимости отражения от температуры
    return np.clip(0.2 + 0.1 * np.sin(temp / 100), 0, 1)

# Функция обновления температуры
def update_temperature(frame):
    global temperature
    laplacian = (np.roll(temperature, +1, 0) + np.roll(temperature, -1, 0) +
                np.roll(temperature, +1, 1) + np.roll(temperature, -1, 1) - 4*temperature)
    temperature += 0.1 * laplacian
    temperature[nx//2, ny//2] = slider.val
    return temperature

# Функция обновления анимации
def update(frame):
    temp = update_temperature(frame)
    im.set_array(temp)

    # Обновление 3D-графика
    ax_3d.clear()
    ax_3d.plot_surface(x, y, temp, cmap='hot')
    ax_3d.set_title("3D визуализация температуры")
    ax_3d.set_xlabel("X")
    ax_3d.set_ylabel("Y")
    ax_3d.set_zlabel("Температура (K)")

    # Обновление данных графиков
    time_data.append(frame)
    current_temp = slider.val
    temp_data.append(current_temp)

    absorption_data.append(calculate_absorption(current_temp))
    reflection_data.append(calculate_reflection(current_temp))

    line_temp.set_data(time_data, temp_data)
    line_abs.set_data(time_data, absorption_data)
    line_ref.set_data(time_data, reflection_data)

    return [im, line_temp, line_abs, line_ref]

ax_slider.text(50, -0.5, 'Симуляция нагрева бериллия и оптических свойств',
               horizontalalignment='center',
               transform=ax_slider.transAxes,
               fontsize=10)

ani = animation.FuncAnimation(fig, update, frames=200, interval=50, blit=True)
plt.show()
