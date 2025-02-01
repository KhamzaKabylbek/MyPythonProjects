from vpython import *
import numpy as np

# Параметры модели
size = 10  # Размер куба (количество узлов по каждой оси)
L = 1.0    # Длина куба (физический размер)
T = np.zeros((size, size, size))  # Массив для хранения температуры
T_new = np.zeros((size, size, size))  # Временный массив для новых значений температуры
dx = L / (size - 1)  # Шаг по пространству
dt = 0.001  # Шаг по времени
time = 0.0  # Начальное время
total_time = 10.0  # Общее время моделирования

# Материалы и их коэффициенты теплопроводности
materials = {
    "Медь": {"alpha": 0.01, "color": vector(0.8, 0.5, 0.2)},  # Оранжевый (медь)
    "Алюминий": {"alpha": 0.005, "color": vector(0.75, 0.75, 0.75)},  # Серебристый (алюминий)
    "Дерево": {"alpha": 0.001, "color": vector(0.55, 0.27, 0.07)},  # Коричневый (дерево)
    "Серебро": {"alpha": 0.015, "color": vector(0.75, 0.75, 0.75)},  # Серебристый (серебро)
    "Железо": {"alpha": 0.02, "color": vector(0.5, 0.5, 0.5)},  # Серый (железо)
    "Сталь": {"alpha": 0.018, "color": vector(0.6, 0.6, 0.6)},  # Светло-серый (сталь)
    "Свинец": {"alpha": 0.003, "color": vector(0.3, 0.3, 0.3)}  # Темно-серый (свинец)
}

# Начальные условия (например, нагретый центр)
T[size//2, size//2, size//2] = 5000.0  # Увеличенная начальная температура

# Создание сцены с новыми размерами и стилем
scene = canvas(title="Теплопроводность в 3D", width=800, height=600, align='left', background=vector(0.95, 0.95, 0.95))
scene.camera.pos = vector(2, 2, 2)
scene.camera.axis = vector(-2, -2, -2)

# Создание контейнера для всего интерфейса
container = """<div style='display: flex; width: 100%; max-width: 1200px; margin: 0 auto; padding: 20px;'>
    <div style='flex: 1;'>
        <div style='margin-bottom: 30px;'>
            <h1 style='font-family: Arial, sans-serif; text-align: center; color: #2c3e50; 
                      font-size: 32px; margin-bottom: 10px;'>Визуализация теплопроводности</h1>
            <p style='text-align: center; color: #7f8c8d; margin-bottom: 20px;'>3D модель распространения тепла в материалах</p>
        </div>
    </div>
</div>"""
title = wtext(text=container)

# Создание куба для визуализации
cubes = []
for i in range(size):
    for j in range(size):
        for k in range(size):
            pos = vector(i * dx - L/2, j * dx - L/2, k * dx - L/2)
            cube = box(pos=pos, length=dx, height=dx, width=dx, color=color.blue)
            cubes.append(cube)

# Обновленная панель управления
control_panel = """<div style='position: absolute; right: 20px; top: 20px; width: 300px; 
                   background: white; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
                   border-radius: 15px; padding: 20px;'>
    <div style='background: #2c3e50; margin: -20px -20px 20px -20px; padding: 15px; 
         border-radius: 15px 15px 0 0;'>
        <h2 style='color: white; margin: 0; font-family: Arial, sans-serif; 
            font-size: 20px; text-align: center;'>Панель управления</h2>
    </div>"""
control_panel_widget = wtext(text=control_panel)

# Стилизованное меню выбора материала
material_section = """<div style='background: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
    <h3 style='color: #2c3e50; margin: 0 0 10px 0; font-size: 16px;'>Выбор материала</h3>"""
wtext(text=material_section)
material_menu = menu(choices=list(materials.keys()), bind=lambda m: set_material(m.selected))
alpha = materials["Медь"]["alpha"]  # Начальное значение теплопроводности
material_color = materials["Медь"]["color"]  # Начальный цвет материала

# Функция для установки коэффициента теплопроводности и цвета материала
def set_material(selected_material):
    global alpha, material_color
    alpha = materials[selected_material]["alpha"]
    material_color = materials[selected_material]["color"]
    print(f"Выбран материал: {selected_material}, теплопроводность: {alpha}")

# Стилизованный слайдер времени
time_section = """<div style='background: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
    <h3 style='color: #2c3e50; margin: 0 0 10px 0; font-size: 16px;'>Управление временем</h3>"""
wtext(text=time_section)
time_slider = slider(min=0, max=total_time, value=0, bind=lambda s: set_time(s.value))

# Функция для установки времени
def set_time(value):
    global time
    time = value
    time_label.text = f"<p style='color: #2c3e50; margin: 5px 0;'><b>Текущее время:</b> {time:.2f}</p>"

# Стилизованная информация о температуре
temp_section = """<div style='background: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
    <h3 style='color: #2c3e50; margin: 0 0 10px 0; font-size: 16px;'>Информация</h3>"""
wtext(text=temp_section)
time_label = wtext(text="<p style='color: #2c3e50; margin: 5px 0;'><b>Текущее время:</b> 0.0</p>")
temperature_label = wtext(text="<p style='color: #2c3e50; margin: 5px 0;'><b>Макс. температура:</b> 0.0</p>")

# Шкала температуры
temperature_label = wtext(text="<p style='color: #555;'><b>Макс. температура:</b> 0.0</p>")

# Добавим слайдер температуры после секции управления временем
temp_control_section = """<div style='background: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
    <h3 style='color: #2c3e50; margin: 0 0 10px 0; font-size: 16px;'>Управление температурой</h3>"""
wtext(text=temp_control_section)
temperature_slider = slider(min=0, max=10000, value=5000, bind=lambda s: set_temperature(s.value))

# Функция для нагрева куба
def heat_cube(temperature_value):
    global T
    # Создаем тепловой градиент от центра
    center = size // 2
    for i in range(size):
        for j in range(size):
            for k in range(size):
                # Рассчитываем расстояние от центра
                distance = np.sqrt((i-center)**2 + (j-center)**2 + (k-center)**2)
                # Применяем температуру с учетом расстояния
                T[i,j,k] = temperature_value * np.exp(-distance/2)

# Обновим функцию установки температуры
def set_temperature(value):
    global T
    heat_cube(value)
    print(f"Установлена температура: {value}")

# Обновленная функция обновления температуры для более реалистичного распространения тепла
def update_temperature(T, T_new, alpha, dx, dt):
    # Коэффициент теплопередачи
    k = alpha * dt / (dx * dx)
    # Ограничиваем коэффициент для стабильности
    k = min(k, 0.2)
    
    for i in range(1, size-1):
        for j in range(1, size-1):
            for k in range(1, size-1):
                T_new[i,j,k] = T[i,j,k] + k * (
                    T[i+1,j,k] + T[i-1,j,k] +
                    T[i,j+1,k] + T[i,j-1,k] +
                    T[i,j,k+1] + T[i,j,k-1] - 6*T[i,j,k]
                )
                # Добавляем небольшое затухание
                T_new[i,j,k] *= 0.999
    return T_new

# Основной цикл моделирования
while True:
    rate(100)  # Уменьшение частоты обновления для более плавной анимации
    
    T_new = update_temperature(T, T_new, alpha, dx, dt)
    T, T_new = T_new, T
    
    max_temp = np.max(T)
    temperature_label.text = f"<p style='color: #2c3e50; margin: 5px 0;'><b>Макс. температура:</b> {max_temp:.2f}</p>"
    
    for idx, cube in enumerate(cubes):
        i = idx // (size * size)
        j = (idx // size) % size
        k = idx % size
        temperature = T[i, j, k]
        if temperature > 0:
            # Улучшенная визуализация нагрева
            intensity = min(temperature / 5000, 1)  # Более плавный градиент
            # Создаем градиент от текущего цвета материала к красному при нагреве
            cube.color = vector(
                material_color.x + (1 - material_color.x) * intensity,
                material_color.y * (1 - intensity),
                material_color.z * (1 - intensity)
            )
        else:
            cube.color = material_color

    time += dt
    time_slider.value = time

    if time >= total_time:
        time = 0.0
        current_temp = temperature_slider.value
        heat_cube(current_temp)  # Используем новую функцию нагрева