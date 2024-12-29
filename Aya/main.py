import numpy as np
import matplotlib.pyplot as plt

# Константы
plasma_frequency = 1.6e16  # Плазменная частота бериллия (рад/с)
relaxation_time = 1e-15    # Время релаксации (с)
epsilon_inf = 1.0          # Диэлектрическая проницаемость на высоких частотах

# Функция для расчета диэлектрической функции
def dielectric_function(omega, plasma_frequency, relaxation_time, epsilon_inf=1.0):
    gamma = 1 / relaxation_time
    epsilon = epsilon_inf - (plasma_frequency**2) / (omega**2 + 1j * gamma * omega)
    return epsilon

# Частотный диапазон (рад/с)
omega = np.logspace(13, 16, 500)  # Частоты от 10^13 до 10^16 рад/с

# Расчет диэлектрической функции
epsilon = dielectric_function(omega, plasma_frequency, relaxation_time, epsilon_inf)

# Разделение на действительную и мнимую части
epsilon_real = np.real(epsilon)
epsilon_imag = np.imag(epsilon)

# Расчет коэффициента отражения и поглощения
def refractive_index(epsilon):
    n = np.sqrt((np.abs(epsilon) + epsilon_real) / 2)
    k = np.sqrt((np.abs(epsilon) - epsilon_real) / 2)
    return n, k

n, k = refractive_index(epsilon)

# Коэффициент отражения
R = ((n - 1)**2 + k**2) / ((n + 1)**2 + k**2)

# Коэффициент пропускания
T = 1 - R

# Построение графиков
plt.figure(figsize=(10, 8))

# Диэлектрическая функция
plt.subplot(2, 2, 1)
plt.plot(omega, epsilon_real, label='Re(ε)', color='blue')
plt.plot(omega, epsilon_imag, label='Im(ε)', color='red')
plt.xscale('log')
plt.title('Диэлектрическая функция')
plt.xlabel('Частота ω (рад/с)')
plt.ylabel('ε')
plt.legend()
plt.grid()

# Показатель преломления и коэффициент поглощения
plt.subplot(2, 2, 2)
plt.plot(omega, n, label='n (Refractive Index)', color='green')
plt.plot(omega, k, label='k (Extinction Coefficient)', color='purple')
plt.xscale('log')
plt.title('Оптические параметры')
plt.xlabel('Частота ω (рад/с)')
plt.ylabel('n, k')
plt.legend()
plt.grid()

# Коэффициент отражения
plt.subplot(2, 2, 3)
plt.plot(omega, R, label='Reflection Coefficient', color='orange')
plt.xscale('log')
plt.title('Коэффициент отражения')
plt.xlabel('Частота ω (рад/с)')
plt.ylabel('R')
plt.grid()

# Коэффициент поглощения
alpha = 2 * omega * k / 3e8  # α = 2ωk/c
plt.subplot(2, 2, 4)
plt.plot(omega, alpha, label='Absorption Coefficient', color='brown')
plt.xscale('log')
plt.title('Коэффициент поглощения')
plt.xlabel('Частота ω (рад/с)')
plt.ylabel('α (1/м)')
plt.grid()

# Коэффициент пропускания
plt.subplot(3, 2, 5)
plt.plot(omega, T, label='Transmission Coefficient', color='cyan')
plt.xscale('log')
plt.title('Коэффициент пропускания')
plt.xlabel('Частота ω (рад/с)')
plt.ylabel('T')
plt.grid()

plt.tight_layout()
plt.show()

