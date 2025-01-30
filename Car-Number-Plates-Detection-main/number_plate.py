import cv2
import pytesseract
import re
import os
import time
import numpy as np
import sys
import subprocess
import ssl
from threading import Thread
from queue import Queue
from yolo_detector import VehicleDetector

# Обновляем конфигурацию
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

# Инициализация
harcascade = "model/haarcascade_russian_plate_number.xml"
video_path = '/Users/hamza/PycharmProjects/pythonProject/Car-Number-Plates-Detection-main/model/2025-01-28 18.00.01.mp4'
cap = cv2.VideoCapture(video_path)
min_area = 500
detected_plates = set()  # Для отслеживания уникальных номеров

# Добавляем параметры для оптимизации
SKIP_FRAMES = 2  # Пропускать каждый второй кадр
PROCESS_WIDTH = 640  # Уменьшаем размер обрабатываемого изображения
PROCESS_HEIGHT = 480
QUEUE_SIZE = 32  # Размер очереди для обработки номеров

# Очередь для многопоточной обработки номеров
plate_queue = Queue(maxsize=QUEUE_SIZE)

# Добавляем новые константы
SAVE_DIR = "detected_plates"
MIN_CONFIDENCE = 0.65  # Минимальная уверенность в распознавании
MIN_PLATE_CONFIDENCE = 0.4  # Минимальная уверенность для распознавания текста

# Изменяем путь сохранения
PLATES_FILE = "/Users/hamza/PycharmProjects/pythonProject/Car-Number-Plates-Detection-main/plates.txt"
detected_plates = set()  # Очищаем множество в начале работы

# Добавляем улучшенную конфигурацию Tesseract
TESSERACT_CONFIGS = [
    '--psm 8 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
    '--psm 7 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
    '--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
]

print("[INFO] Инициализация детектора...")
detector = VehicleDetector()
print("[INFO] Детектор успешно инициализирован")

def get_plate_type(text):
    """Определение типа номерного знака"""
    patterns = {
        'civil': r'^\d{3}[A-Z]{3}\d{2}$',      # 058VNA12
        'transit': r'^\д{3}[A-Z]{2}\д{2}$',     # 123AB01
        'government': r'^\д{3}\д{2}KZ$',        # 12301KZ
        'diplomatic': r'^\д{3}(CD|D|UN)\д{2}$', # 123CD01
        'military': r'^\д{3}[A-Z]{2}\д{2}$',    # 123AB01
        'taxi': r'^\д{3}[A-Z]{3}\д{2}$',       # 123ABC01
        'trailer': r'^\д{3}[A-Z]{2}\д{2}$',    # 123AB01
        'motorcycle': r'^\д{2}[A-Z]{2}\д{2}$'   # 12AB01
    }
    text = text.upper()
    for plate_type, pattern in patterns.items():
        if re.match(pattern, text):
            return plate_type
    return None

def is_valid_plate(text):
    """Проверка формата казахстанского номера"""
    if not text:
        return False
    text = text.upper()
    return get_plate_type(text) is not None

def format_plate_number(text):
    """Форматирование номера в правильный вид"""
    if not text:
        return text
    text = text.upper()
    plate_type = get_plate_type(text)
    if plate_type == 'government':
        return f"{text[:3]}|{text[3:5]}|{text[5:]}"
    elif plate_type == 'motorcycle':
        return f"{text[:2]}|{text[2:4]}|{text[4:]}"
    else:
        return f"{text[:-2]}|{text[-2:]}"

def save_plate_number(plate_number, img_roi):
    """Сохранение номера с расширенным логированием"""
    try:
        # Нормализация номера
        plate_number = ''.join(c for c in plate_number if c.isalnum()).upper()
        formatted_number = format_plate_number(plate_number)
        
        if not formatted_number:
            print(f"[-] Некорректный формат номера: {plate_number}")
            return False
            
        if formatted_number in detected_plates:
            print(f"[*] Номер уже обнаружен: {formatted_number}")
            return False
            
        detected_plates.add(formatted_number)
        
        # Создаем директории если не существуют
        os.makedirs(os.path.dirname(PLATES_FILE), exist_ok=True)
        plates_dir = os.path.join(os.path.dirname(PLATES_FILE), "plates_images")
        os.makedirs(plates_dir, exist_ok=True)
        
        # Сохраняем в лог-файл
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        plate_type = get_plate_type(plate_number)
        log_entry = (
            f"{'='*50}\n"
            f"Время обнаружения: {current_time}\n"
            f"Номер: {formatted_number}\n"
            f"Тип номера: {plate_type}\n"
            f"Оригинальный текст: {plate_number}\n"
            f"{'='*50}\n"
        )
        
        # Используем режим 'a' для добавления в конец файла
        with open(PLATES_FILE, "a", encoding='utf-8') as f:
            f.write(log_entry)
            f.flush()
            os.fsync(f.fileno())
        
        # Сохраняем изображения
        timestamp = int(time.time())
        orig_path = os.path.join(plates_dir, f"orig_{formatted_number}_{timestamp}.jpg")
        proc_path = os.path.join(plates_dir, f"proc_{formatted_number}_{timestamp}.jpg")
        
        # Сохраняем оригинальное и обработанное изображения
        cv2.imwrite(orig_path, img_roi)
        processed = preprocess_plate(img_roi)
        cv2.imwrite(proc_path, processed)
        
        print(f"[+] Сохранен номер: {formatted_number}")
        print(f"[+] Изображения сохранены в: {plates_dir}")
        print(f"[+] Лог обновлен: {PLATES_FILE}")
        return True
        
    except Exception as e:
        print(f"[-] Ошибка сохранения номера: {e}")
        import traceback
        traceback.print_exc()
        return False

def preprocess_image(img):
    """Предобработка изображения"""
    try:
        # Контраст
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        enhanced = cv2.merge((cl, a, b))
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

        # Масштабирование
        enhanced = cv2.resize(enhanced, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)

        # Обработка
        gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray)
        binary = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        # Морфология
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        processed = cv2.morphologyEx(processed, cv2.MORPH_OPEN, kernel)

        return processed
    except Exception as e:
        print(f"Ошибка в предобработке изображения: {e}")
        return img

def preprocess_plate(img):
    """Улучшенная предобработка номерного знака"""
    try:
        # Преобразование в оттенки серого
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Применение порогового значения
        _, thresh = cv2.threshold(gray, 64, 255, cv2.THRESH_BINARY_INV)
        
        # Удаление шума
        denoised = cv2.fastNlMeansDenoising(thresh)
        
        # Увеличение контраста
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        contrast = clahe.apply(denoised)
        
        return contrast
        
    except Exception as e:
        print(f"Ошибка в предобработке номера: {e}")
        return img

def process_license_plate(img_roi):
    """
    Пошаговая обработка изображения номерного знака
    """
    try:
        # Step 1: Увеличение изображения
        img_roi = cv2.resize(img_roi, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        
        # Step 2: Преобразование в градации серого и размытие
        gray = cv2.cvtColor(img_roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Step 3: Пороговая обработка методом Оцу
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Step 4: Дилатация для улучшения контуров
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dilated = cv2.dilate(thresh, kernel, iterations=1)
        
        # Step 5: Поиск контуров и сортировка слева направо
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[0])
        
        # Step 6: Фильтрация контуров
        height_img = img_roi.shape[0]
        plate_chars = []
        
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = h/w
            area = cv2.contourArea(cnt)
            
            # Фильтры для контуров
            if (h >= height_img/6 and  # Высота символа
                aspect_ratio >= 1.0 and  # Соотношение сторон
                area > 100):  # Минимальная площадь
                
                # Step 7: Обработка каждого символа
                char_roi = thresh[y:y+h, x:x+w]
                char_roi = cv2.bitwise_not(char_roi)  # Инверсия цветов
                char_roi = cv2.medianBlur(char_roi, 3)  # Сглаживание
                
                # Распознавание символа
                char = pytesseract.image_to_string(char_roi, 
                    config='--psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                
                if char.strip():  # Если символ распознан
                    plate_chars.append(char.strip())
        
        # Step 8: Объединение символов в строку
        plate_number = ''.join(plate_chars)
        return plate_number if plate_number else None
        
    except Exception as e:
        print(f"[-] Ошибка обработки номера: {e}")
        return None

def display_plate_number(plate_text, img_roi):
    """Отображение номера в отдельном окне"""
    # Создаем два отдельных окна
    
    # 1. Окно с номером и текстом
    display = np.ones((200, 600, 3), dtype=np.uint8) * 255
    plate_img = cv2.resize(img_roi, (200, 100))
    display[50:150, 20:220] = plate_img
    cv2.putText(display, f"Номер: {plate_text}", 
                (240, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                1.2, (0, 0, 0), 2)
    
    # 2. Окно только с номером (увеличенное)
    zoomed_plate = cv2.resize(img_roi, (400, 200))
    processed_plate = preprocess_plate(zoomed_plate)
    
    # Показываем оба окна
    cv2.imshow("Detected License Plate", display)
    cv2.imshow("Zoomed Plate", zoomed_plate)
    cv2.imshow("Processed Plate", processed_plate)
    
    # Позиционируем окна
    cv2.moveWindow("Detected License Plate", 0, 0)
    cv2.moveWindow("Zoomed Plate", 0, 250)
    cv2.moveWindow("Processed Plate", 0, 500)

# Добавляем простую функцию записи в файл
def write_plate_to_file(plate_text):
    """Простая запись номера в файл"""
    try:
        with open('detected_numbers.txt', 'a', encoding='utf-8') as f:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{current_time}] Номер: {plate_text}\n")
            print(f"[+] Записан номер: {plate_text}")
    except Exception as e:
        print(f"[-] Ошибка записи в файл: {e}")

def process_plate(img_roi, plate_x, plate_y, pw, ph, img):
    """Упрощенная обработка номера"""
    try:
        # Увеличиваем изображение для лучшего распознавания
        img_roi = cv2.resize(img_roi, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        
        # Преобразуем в градации серого
        gray = cv2.cvtColor(img_roi, cv2.COLOR_BGR2GRAY)
        
        # Применяем пороговую обработку
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Распознаем текст
        plate_text = pytesseract.image_to_string(
            thresh,
            config='--psm 8 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        ).strip()

        if plate_text:
            # Записываем в файл
            write_plate_to_file(plate_text)
            
            # Отображаем на экране
            cv2.putText(img, plate_text, (plate_x, plate_y - 5),
                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            # Показываем увеличенное изображение номера
            zoomed = cv2.resize(img_roi, (400, 200))
            cv2.imshow("Detected Plate", zoomed)
            cv2.moveWindow("Detected Plate", 0, 0)
            
            return True
            
        return False
        
    except Exception as e:
        print(f"[-] Ошибка распознавания: {e}")
        return False

def process_plates_worker():
    """Фоновый процесс обработки номеров"""
    while True:
        if not plate_queue.empty():
            plate_data = plate_queue.get()
            if plate_data is None:
                break
            process_plate(*plate_data)
        else:
            time.sleep(0.01)

# Запускаем поток обработки номеров
plate_processor = Thread(target=process_plates_worker, daemon=True)
plate_processor.start()

# Заменяем инициализацию YOLO на новый детектор
detector = VehicleDetector()

# Модифицируем основной цикл
frame_count = 0
while cap.isOpened():
    success, img = cap.read()
    if not success:
        break

    frame_count += 1
    if frame_count % SKIP_FRAMES != 0:
        continue

    # Детекция автомобилей
    vehicles = detector.detect_vehicles(img)
    
    # Обработка каждого найденного автомобиля
    for vehicle in vehicles:
        x, y, w, h = vehicle['bbox']
        
        # Зеленая рамка для авто
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Область поиска номера
        vehicle_roi = img[y:y+h, x:x+w]
        
        # Поиск номера в автомобиле
        plates = detector.detect_plates(vehicle_roi)
        
        for plate in plates:
            px, py, pw, ph = plate['bbox']
            plate_x, plate_y = x + px, y + py
            
            # Синяя рамка для номера
            cv2.rectangle(img, (plate_x, plate_y),
                        (plate_x + pw, plate_y + ph), (255, 0, 0), 2)
            
            img_roi = img[plate_y:plate_y + ph, plate_x:plate_x + pw]
            if not plate_queue.full():
                plate_queue.put((img_roi, plate_x, plate_y, pw, ph, img))

    cv2.imshow("Result", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Очистка
plate_queue.put(None)  # Сигнал для завершения потока
plate_processor.join()
cap.release()
cv2.destroyAllWindows()
