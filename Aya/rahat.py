import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import jv

# Улучшенные параметры волновода
radius1 = 10  # Радиус внутренней части
radius2 = 20  # Радиус внешней части
m = 1  # Порядок функции Бесселя
k = 2 * np.pi / 5  # Волновое число
beta = 1  # Константа для магнитной волны

# Улучшенная сетка с большим разрешением
nx, ny = 200, 200  # Увеличено разрешение сетки
x = np.linspace(-radius2, radius2, nx)
y = np.linspace(-radius2, radius2, ny)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)
PHI = np.arctan2(Y, X)

def magnetic_field(r, phi, z):
    """
    Вычисляет магнитное поле в волноводе с плавным переходом между областями
    """
    result = np.zeros_like(r, dtype=complex)
    
    # Добавляем плавный переход между областями
    transition_width = 0.5
    inner_mask = r <= (radius1 - transition_width)
    outer_mask = r >= (radius1 + transition_width)
    transition_mask = ~(inner_mask | outer_mask)
    
    # Внутренняя часть
    result[inner_mask] = jv(m, beta * r[inner_mask]) * np.cos(m * phi[inner_mask])
    
    # Внешняя часть
    beta2 = beta * radius1 / radius2
    outer_field = jv(m, beta2 * r[outer_mask]) * np.cos(m * phi[outer_mask])
    result[outer_mask] = outer_field
    
    # Плавный переход
    if np.any(transition_mask):
        t = (r[transition_mask] - (radius1 - transition_width)) / (2 * transition_width)
        inner_val = jv(m, beta * r[transition_mask]) * np.cos(m * phi[transition_mask])
        outer_val = jv(m, beta2 * r[transition_mask]) * np.cos(m * phi[transition_mask])
        result[transition_mask] = inner_val * (1 - t) + outer_val * t
    
    return result * np.exp(-1j * k * z)

# Создание фигуры с улучшенным layout
plt.style.use('dark_background')
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(2, 2, height_ratios=[5, 1], width_ratios=[1, 1], hspace=0.3, wspace=0.2)

# Настройка осей
ax_field = fig.add_subplot(gs[0, 0], projection='3d')
ax_2d = fig.add_subplot(gs[0, 1])
ax_slider_z = fig.add_subplot(gs[1, :])

# Улучшенный слайдер
slider_z = Slider(
    ax=ax_slider_z,
    label='Z (сечение волновода)',
    valmin=0,
    valmax=10,
    valinit=0,
    valstep=0.05,  # Уменьшен шаг для более плавной анимации
    color='lightblue'
)

def update_field(z):
    """Обновление визуализации поля с улучшенным качеством"""
    field = np.abs(magnetic_field(R, PHI, z))
    
    ax_field.clear()
    ax_2d.clear()
    
    # Улучшенная 3D визуализация
    norm = plt.Normalize(field.min(), field.max())
    surf = ax_field.plot_surface(X, Y, field, cmap='plasma',
                               norm=norm,
                               edgecolor='none',
                               alpha=0.9,
                               antialiased=True,
                               rcount=100,  # Увеличено количество точек рендеринга
                               ccount=100)
    
    ax_field.set_title('3D визуализация магнитного поля', fontsize=12, pad=20)
    ax_field.set_xlabel('X', labelpad=10)
    ax_field.set_ylabel('Y', labelpad=10)
    ax_field.set_zlabel('Магнитное поле', labelpad=10)
    
    # Настройка угла обзора для лучшего восприятия
    ax_field.view_init(elev=30, azim=45)
    
    # Улучшенная 2D визуализация
    im = ax_2d.imshow(field, extent=(-radius2, radius2, -radius2, radius2),
                     cmap='plasma',
                     interpolation='gaussian',  # Улучшенная интерполяция
                     aspect='equal')
    
    # Добавление контурных линий с оптимизированными параметрами
    levels = np.linspace(field.min(), field.max(), 15)
    contours = ax_2d.contour(X, Y, field, levels=levels,
                            colors='white', alpha=0.2, linewidths=0.5)
    
    # Настройка цветовых шкал
    plt.colorbar(im, ax=ax_2d, label='Амплитуда поля')
    fig.colorbar(surf, ax=ax_field, shrink=0.5, aspect=5, label='Амплитуда поля')
    
    ax_2d.set_title('2D срез магнитного поля')
    ax_2d.set_xlabel('X')
    ax_2d.set_ylabel('Y')

def update(frame):
    """Функция обновления для более плавной анимации"""
    z = frame  # Напрямую используем frame как значение z
    update_field(z)
    fig.suptitle(f'Срез магнитного поля на Z={z:.2f}', fontsize=16)
    return fig,

# Создание более плавной анимации
frames = np.linspace(0, 10, 200)  # Увеличено количество кадров
ani = animation.FuncAnimation(fig, update, frames=frames,
                            interval=50,  # Уменьшен интервал
                            blit=True,
                            repeat=True)

# Добавление информации о параметрах
info_text = f'''Параметры:
Радиус внутр.: {radius1}
Радиус внеш.: {radius2}
Порядок m: {m}
Волновое число k: {k:.2f}'''
plt.figtext(0.02, 0.02, info_text, fontsize=10, 
           bbox=dict(facecolor='black', alpha=0.5))

# Начальная визуализация
update_field(0)

plt.show()