import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

# Константы системы
num_particles = 50
box_size = 10
dt = 0.01
num_steps = 500

# Потенциал Леннард-Джонса
epsilon = 1.0
sigma = 1.0

# Функция для вычисления силы по потенциалу Леннард-Джонса
def lj_force(r):
    r6 = (sigma / r)**6
    r12 = r6**2
    return 24 * epsilon * (2 * r12 - r6) / r**2

# Инициализация частиц
positions = np.random.uniform(0, box_size, (num_particles, 3))
velocities = np.random.normal(0, 0.5, (num_particles, 3))
forces = np.zeros_like(positions)

# Вычисление сил
def compute_forces(positions):
    forces = np.zeros_like(positions)
    for i in range(num_particles):
        for j in range(i + 1, num_particles):
            r_vec = positions[i] - positions[j]
            r_vec -= np.rint(r_vec / box_size) * box_size  # Периодические границы
            r = np.linalg.norm(r_vec)
            if r > 0:
                f = lj_force(r) * r_vec / r
                forces[i] -= f
                forces[j] += f
    return forces

# Интегратор Верле
def velocity_verlet(positions, velocities, forces, dt):
    positions += velocities * dt + 0.5 * forces * dt**2
    positions %= box_size  # Периодические границы
    new_forces = compute_forces(positions)
    velocities += 0.5 * (forces + new_forces) * dt
    return positions, velocities, new_forces

# Настройка визуализации
plt.style.use('dark_background')
fig = plt.figure(figsize=(18, 10))
gs = fig.add_gridspec(3, 2, height_ratios=[5, 1, 3])

ax_sim = fig.add_subplot(gs[0, 0], projection='3d')
ax_temp = fig.add_subplot(gs[2, :])
ax_slider_dt = fig.add_axes([0.2, 0.15, 0.6, 0.03])

ax_sim.set_xlim(0, box_size)
ax_sim.set_ylim(0, box_size)
ax_sim.set_zlim(0, box_size)
ax_sim.set_title("Молекулярная динамика: 3D визуализация", color='white')

slider_dt = Slider(ax_slider_dt, 'Шаг времени', 0.005, 0.05, valinit=dt, color='lightblue')

temp_data = []
time_data = []

# Анимация
scat = ax_sim.scatter(positions[:, 0], positions[:, 1], positions[:, 2], c='cyan', s=50)

def update(frame):
    global positions, velocities, forces, dt
    dt = slider_dt.val
    positions, velocities, forces = velocity_verlet(positions, velocities, forces, dt)

    # Обновление 3D визуализации
    scat._offsets3d = (positions[:, 0], positions[:, 1], positions[:, 2])

    # Вычисление температуры
    kinetic_energy = 0.5 * np.sum(velocities**2)
    temperature = kinetic_energy / num_particles
    temp_data.append(temperature)
    time_data.append(frame * dt)

    ax_temp.clear()
    ax_temp.plot(time_data, temp_data, 'r-', lw=2, label='Температура')
    ax_temp.set_xlim(0, num_steps * dt)
    ax_temp.set_ylim(0, max(temp_data) * 1.2)
    ax_temp.set_title("Температура системы", color='white')
    ax_temp.set_xlabel("Время", color='white')
    ax_temp.set_ylabel("Температура", color='white')
    ax_temp.legend(loc='upper right', framealpha=0.8)
    ax_temp.grid(True, linestyle='--', alpha=0.3)
    return scat,

ani = animation.FuncAnimation(fig, update, frames=num_steps, interval=50, blit=False)

plt.show()
