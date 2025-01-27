# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.widgets import Slider
# from matplotlib.colors import LightSource

# # Генерация данных для модели белого карлика
# def generate_white_dwarf(radius=1, resolution=100):
#     phi = np.linspace(0, 2 * np.pi, resolution)
#     theta = np.linspace(0, np.pi, resolution)
#     phi, theta = np.meshgrid(phi, theta)
#     x = radius * np.sin(theta) * np.cos(phi)
#     y = radius * np.sin(theta) * np.sin(phi)
#     z = radius * np.cos(theta)
#     return x, y, z

# # Модель распределения пылевых частиц
# def generate_dust_particles(num_particles=500, radius=1.5):
#     np.random.seed(42)
#     phi = np.random.uniform(0, 2 * np.pi, num_particles)
#     theta = np.random.uniform(0, np.pi, num_particles)
#     r = np.random.uniform(radius, radius + 0.5, num_particles)
#     x = r * np.sin(theta) * np.cos(phi)
#     y = r * np.sin(theta) * np.sin(phi)
#     z = r * np.cos(theta)
#     return x, y, z

# # Функция для обновления графика
# def update(val):
#     temp_dust = slider.val  # Текущее значение слайдера
#     ax.clear()  # Очистить предыдущий график
    
#     # Рисуем белый карлик с текстурой
#     x, y, z = generate_white_dwarf()
#     ls = LightSource(azdeg=45, altdeg=45)
#     color_map = plt.cm.hot  # Используем карту горячего цвета
#     rgb = ls.shade(z, cmap=color_map, vert_exag=0.8, blend_mode='soft')
#     ax.plot_surface(x, y, z, facecolors=rgb, rstride=1, cstride=1, alpha=0.9, edgecolor='none')
    
#     # Рисуем пылевые частицы
#     dust_x, dust_y, dust_z = generate_dust_particles()
#     temp_norm = (temp_dust - 300) / (2000 - 300)  # Нормализация температуры
#     colors = plt.cm.plasma(temp_norm)
#     ax.scatter(dust_x, dust_y, dust_z, c=colors, s=10, label=f"Temp: {int(temp_dust)} K")
    
#     # Настройка фона
#     ax.set_facecolor('black')  # Черный фон для космоса
    
#     # Обновляем параметры графика
#     ax.set_title("Белый карлик G29-38 и пылевые частицы", fontsize=16, color='white')
#     ax.set_xlabel("X", fontsize=12, color='white')
#     ax.set_ylabel("Y", fontsize=12, color='white')
#     ax.set_zlabel("Z", fontsize=12, color='white')
#     ax.tick_params(colors='white')  # Белые метки на осях 
#     ax.legend(loc='upper right', fontsize=10, facecolor='black', edgecolor='white', labelcolor='white') 
#     fig.canvas.draw_idle()  # Обновить график 

# # Настройка окна и слайдера
# fig = plt.figure(figsize=(10, 8), facecolor='black')
# ax = fig.add_subplot(111, projection='3d')
# plt.subplots_adjust(bottom=0.2)  # Оставляем место для слайдера

# # Создаём слайдер
# ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03], facecolor='lightgrey')  # Позиция слайдера
# slider = Slider(ax_slider, 'Температура (K)', 300, 2000, valinit=500, valstep=50)

# # Привязываем обновление графика к слайдеру
# slider.on_changed(update)

# # Рисуем начальный график
# update(500)

# plt.show()
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog
from PyQt6.QtCore import Qt
from docx import Document
import collections

class WordAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Поиск самого повторяющегося слова")
        self.setGeometry(300, 300, 400, 250)

        self.init_ui()

    def init_ui(self):
        self.open_button = QPushButton("Открыть файл")
        self.open_button.clicked.connect(self.open_file)

        self.result_label = QLabel("Результат: ")
        
        self.statistics_label = QLabel("Количество слов: 0")
        
        self.count_button = QPushButton("Подсчитать")
        self.count_button.clicked.connect(self.calculate_most_repeated_word)

        layout = QVBoxLayout()
        layout.addWidget(self.open_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.statistics_label)
        layout.addWidget(self.count_button)

        self.setLayout(layout)
        
        self.file_path = None
        self.text = ""

    def open_file(self):
        try:
            options = QFileDialog.Option()
            file, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Word Files (*.docx)", options=options)
            if file:
                self.file_path = file
                self.text = self.extract_text_from_word(file)
                self.statistics_label.setText(f"Количество слов: {len(self.text.split())}")
        except Exception as e:
            self.result_label.setText(f"Ошибка при открытии файла: {e}")
            print(f"Ошибка при открытии файла: {e}")

    def extract_text_from_word(self, file):
        try:
            document = Document(file)
            full_text = []
            for para in document.paragraphs:
                full_text.append(para.text)
            return " ".join(full_text)
        except Exception as e:
            self.result_label.setText(f"Ошибка при извлечении текста: {e}")
            print(f"Ошибка при извлечении текста: {e}")
            return ""

    def calculate_most_repeated_word(self):
        if not self.text:
            self.result_label.setText("Пожалуйста, откройте файл.")
            return
        
        try:
            words = [word.lower() for word in self.text.split() if word.isalpha()]
            
            word_counts = collections.Counter(words)
            
            most_common_word, count = word_counts.most_common(1)[0]
            
            self.result_label.setText(f"Результат: {most_common_word} (повторяется {count} раз)")
            
            self.setWindowTitle(f"Самое повторяющееся слово: {most_common_word}")
        except Exception as e:
            self.result_label.setText(f"Ошибка при подсчете слов: {e}")
            print(f"Ошибка при подсчете слов: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WordAnalyzer()
    window.show()
    sys.exit(app.exec())
