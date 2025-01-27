import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Основные параметры
R_star = 0.8  # Радиус белого карлика в солнечных радиусах
L_star = 0.4  # Светимость белого карлика в солнечных единицах
dist = 10  # Расстояние от белого карлика до пылевых частиц (в астрономических единицах)
n_particles = 1000  # Количество пылевых частиц
M_star = 0.6  # Масса белого карлика в солнечных массах
G = 6.67430e-11  # Гравитационная постоянная (м^3⋅кг^−1⋅с^−2)

# Дополнительные параметры
c = 3e8  # Скорость света (м/с)
sigma_sb = 5.67e-8  # Стефан-Больцмановская постоянная (Вт/(м²⋅K⁴))

# Функция для вычисления температуры пылевых частиц
def temperature(distance, luminosity):
    return (luminosity / (16 * np.pi * distance**2 * sigma_sb))**(1/4)

# Моделирование давления радиации
def radiation_pressure(luminosity, distance):
    return (luminosity * (1 - albedo)) / (4 * np.pi * distance**2 * c)

# Моделирование гравитационного воздействия
def gravitational_acceleration(mass, distance):
    return G * M_star * mass / distance**2

# Генерация случайных координат пылевых частиц
x = np.random.uniform(-R_star, R_star, n_particles)
y = np.random.uniform(-R_star, R_star, n_particles)
z = np.random.uniform(-R_star, R_star, n_particles)

# Расчет расстояний до белого карлика
distances = np.sqrt(x**2 + y**2 + z**2)

# Вычисление температуры для каждой частицы
temperatures = temperature(distances, L_star)

# Альбедо пылевых частиц
albedo = 0.3

# Функция для вычисления температуры с учетом альбедо
def temperature_with_albedo(distance, luminosity, albedo):
    return ((luminosity * (1 - albedo)) / (16 * np.pi * distance**2 * sigma_sb))**(1/4)

# Вычисление температуры для каждой частицы с учетом альбедо
temperatures_with_albedo = temperature_with_albedo(distances, L_star, albedo)

# Функция для вычисления температуры с учетом разных спектров излучения
def temperature_with_spectrum(distance, luminosity, albedo, uv_fraction=0.2, visible_fraction=0.5, ir_fraction=0.3):
    luminosity_uv = luminosity * uv_fraction
    luminosity_visible = luminosity * visible_fraction
    luminosity_ir = luminosity * ir_fraction
    temperature_uv = (luminosity_uv / (16 * np.pi * distance**2 * sigma_sb))**(1/4)
    temperature_visible = (luminosity_visible / (16 * np.pi * distance**2 * sigma_sb))**(1/4)
    temperature_ir = (luminosity_ir / (16 * np.pi * distance**2 * sigma_sb))**(1/4)
    total_temperature = (temperature_uv**4 + temperature_visible**4 + temperature_ir**4)**(1/4)
    return total_temperature

# Вычисление температуры для каждой частицы с учетом разных спектров и альбедо
temperatures_with_spectrum = temperature_with_spectrum(distances, L_star, albedo)

# Моделируем давление радиации для частиц
pressure = radiation_pressure(L_star, distances)

# Создаем фигуру и оси для всех трех графиков
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5), subplot_kw={'projection': '3d'})

# Первый график: температура пылевых частиц (2D)
axes[0].scatter(x, y, c=temperatures_with_spectrum, cmap='hot', s=10)
axes[0].set_title('Temperature Distribution of Dust Particles around White Dwarf G29-38 (2D)')
axes[0].set_xlabel('X (AU)')
axes[0].set_ylabel('Y (AU)')

# Второй график: температура пылевых частиц (3D)
scatter = axes[1].scatter(x, y, z, c=temperatures_with_spectrum, cmap='hot', s=10)
axes[1].set_title('Temperature Distribution of Dust Particles around White Dwarf G29-38 (3D)')
axes[1].set_xlabel('X (AU)')
axes[1].set_ylabel('Y (AU)')
axes[1].set_zlabel('Z (AU)')

# Третий график: анимация движения пылевых частиц
def update_orbit(frame):
    global x, y, z
    # Примерное движение частиц по орбитам с учетом давления радиации
    x = np.cos(frame / 10) * distances
    y = np.sin(frame / 10) * distances
    z = np.sin(frame / 20) * distances
    scatter._offsets3d = (x, y, z)
    return scatter,

# Обновление scatter в анимации
scatter = axes[2].scatter(x, y, z, c=temperatures_with_spectrum, cmap='hot', s=10)
axes[2].set_title('Orbiting Dust Particles (Animation)')
axes[2].set_xlabel('X (AU)')
axes[2].set_ylabel('Y (AU)')
axes[2].set_zlabel('Z (AU)')

# Создание анимации
ani = FuncAnimation(fig, update_orbit, frames=np.arange(0, 100), interval=50)

# Отображаем результат
plt.tight_layout()
plt.show()
