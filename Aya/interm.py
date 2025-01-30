<<<<<<< HEAD
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import csv
from datetime import datetime

# Параметры сетки и начальные условия
nx, ny = 40, 40
temperature = np.zeros((nx, ny))
source_temp = 100
temperature[nx // 2, ny // 2] = source_temp

# Создание фигуры и областей с улучшенным стилем
plt.style.use('dark_background')  # Тёмная тема для лучшего контраста
fig = plt.figure(figsize=(18, 10))
gs = fig.add_gridspec(3, 3, height_ratios=[5, 0.5, 2])
fig.subplots_adjust(bottom=0.25, top=0.9)

# Создание осей для графиков с улучшенным стилем
ax_sim = fig.add_subplot(gs[0, 0])
ax_graph_temp = fig.add_subplot(gs[0, 2])
ax_graph_optical = fig.add_subplot(gs[2, :])
ax_3d = fig.add_subplot(gs[0, 1], projection='3d')

# Настройка 3D оси для лучшей визуализации
ax_3d.grid(True, linestyle='--', alpha=0.5)
ax_3d.xaxis.pane.fill = False
ax_3d.yaxis.pane.fill = False
ax_3d.zaxis.pane.fill = False

# Создание слайдеров с улучшенным стилем
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
max_temp_data = []

# Настройка слайдеров с улучшенным стилем
def create_slider(ax, label, valmin, valmax, valinit, color):
    return Slider(
        ax=ax,
        label=label,
        valmin=valmin,
        valmax=valmax,
        valinit=valinit,
        color=color,
        alpha=0.8
    )

slider_temp = create_slider(ax_slider_temp, 'Температура источника (K)', 0, 500, source_temp, 'lightblue')
slider_coef = create_slider(ax_slider_coef, 'Коэффициент теплопередачи', 0.01, 0.5, 0.1, 'lightgreen')

# Настройка 2D визуализации с улучшенным стилем
im = ax_sim.imshow(temperature, cmap='plasma', interpolation='bilinear')
cbar = plt.colorbar(im, ax=ax_sim, label='Температура (K)', fraction=0.046, pad=0.04)
cbar.ax.yaxis.label.set_color('white')
cbar.ax.tick_params(colors='white')
ax_sim.set_title('2D Распределение температуры', color='white', pad=10)

# Инициализация 3D поверхности с улучшенным стилем
surf = ax_3d.plot_surface(x, y, temperature, cmap='plasma', rstride=1, cstride=1, antialiased=True, alpha=0.8)
ax_3d.set_title("3D визуализация температуры", color='white', pad=10)
ax_3d.set_xlabel("X", color='white')
ax_3d.set_ylabel("Y", color='white')
ax_3d.set_zlabel("Температура (K)", color='white')

# Настройка графиков с улучшенным стилем
def setup_axes(ax):
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_facecolor('black')
    for spine in ax.spines.values():
        spine.set_color('white')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')

line_temp, = ax_graph_temp.plot([], [], 'r-', lw=2, label='Текущая температура')
line_max_temp, = ax_graph_temp.plot([], [], 'y--', lw=1, label='Максимальная температура')
line_abs, = ax_graph_optical.plot([], [], 'b-', lw=2, label='Поглощение')
line_ref, = ax_graph_optical.plot([], [], 'g-', lw=2, label='Отражение')

setup_axes(ax_graph_temp)
setup_axes(ax_graph_optical)

ax_graph_temp.set_xlim(0, 200)
ax_graph_temp.set_ylim(0, 500)
ax_graph_temp.set_xlabel('Время (с)')
ax_graph_temp.set_ylabel('Температура (K)')
ax_graph_temp.legend(loc='upper left', framealpha=0.8)

ax_graph_optical.set_xlim(0, 200)
ax_graph_optical.set_ylim(0, 1)
ax_graph_optical.set_xlabel('Время (с)')
ax_graph_optical.set_ylabel('Оптические свойства')
ax_graph_optical.legend(loc='upper right', framealpha=0.8)

# Создание файла для логирования
log_filename = f'temperature_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
with open(log_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Time', 'Temperature', 'Max_Temperature', 'Absorption', 'Reflection'])

def calculate_absorption(temp):
    return np.clip(0.8 * np.exp(-temp / 300), 0, 1)

def calculate_reflection(temp):
    return np.clip(0.2 + 0.1 * np.sin(temp / 100), 0, 1)

def update_temperature():
    global temperature
    random_fluctuation = np.random.randn(*temperature.shape) * 0.1
    laplacian = (np.roll(temperature, +1, 0) + np.roll(temperature, -1, 0) +
                 np.roll(temperature, +1, 1) + np.roll(temperature, -1, 1) - 4 * temperature)
    temperature += slider_coef.val * laplacian + random_fluctuation
    temperature[nx // 2, ny // 2] = slider_temp.val
    return temperature

def update(frame):
    global surf
    temp = update_temperature()

    im.set_array(temp)

    surf.remove()
    surf = ax_3d.plot_surface(x, y, temp, cmap='plasma', rstride=1, cstride=1, antialiased=True, alpha=0.8)
    ax_3d.view_init(elev=20 + 10 * np.sin(frame / 50), azim=(frame * 0.5) % 360)

    time_data.append(frame)
    current_temp = slider_temp.val
    max_temp = np.max(temp)
    temp_data.append(current_temp)
    max_temp_data.append(max_temp)

    current_absorption = calculate_absorption(current_temp)
    current_reflection = calculate_reflection(current_temp)

    absorption_data.append(current_absorption)
    reflection_data.append(current_reflection)

    line_temp.set_data(time_data, temp_data)
    line_max_temp.set_data(time_data, max_temp_data)
    line_abs.set_data(time_data, absorption_data)
    line_ref.set_data(time_data, reflection_data)

    stats_text = (f'Время: {frame}с\n'
                  f'Температура источника: {current_temp:.1f}K\n'
                  f'Макс. температура: {max_temp:.1f}K\n'
                  f'Поглощение: {current_absorption:.3f}\n'
                  f'Отражение: {current_reflection:.3f}')

    ax_sim.set_title(stats_text, color='white', pad=10)

    with open(log_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([frame, current_temp, max_temp, current_absorption, current_reflection])

    return [im, line_temp, line_max_temp, line_abs, line_ref]

# Добавление общего заголовка
fig.suptitle('Симуляция нагрева бериллия и оптических свойств', fontsize=14, color='white', y=0.98)

# Создание анимации с оптимизированными параметрами
ani = animation.FuncAnimation(fig, update, frames=200, interval=100, blit=True, cache_frame_data=False)
plt.show()
=======
def calculate_pozitivity_rate(P_bolen, P_poz_bolen, P_poz_ne_bolen):
    """
    Вычисление вероятности позитивного результата теста.
    
    Args:
        P_bolen (float): Вероятность того, что человек болен
        P_poz_bolen (float): Вероятность позитивного результата при болезни
        P_poz_ne_bolen (float): Вероятность ложнопозитивного результата
    
    Returns:
        float: Вероятность позитивного результата
    """
    return P_poz_bolen * P_bolen + P_poz_ne_bolen * (1 - P_bolen)



def main():
    # Параметры
    P_bolen = 0.1  # Вероятность того, что человек болен
    P_poz_bolen = 0.9  # Вероятность позитивного результата при болезни
    P_poz_ne_bolen = 0.1  # Вероятность ложнопозитивного результата

    # Вычисление P(позитивный результат)
    P_poz = calculate_pozitivity_rate(P_bolen, P_poz_bolen, P_poz_ne_bolen)

    # Применение теоремы Байеса
    P_bolen_given_poz = bayesian_theorem(P_bolen, P_poz)

    print(f"Вероятность болезни при позитивном результате теста: {P_bolen_given_poz:.4f}")

if __name__ == "__main__":
    main()
>>>>>>> origin/main
