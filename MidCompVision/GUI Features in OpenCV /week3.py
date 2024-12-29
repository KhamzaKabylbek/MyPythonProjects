import cv2

def detect_faces_realtime_mirror():
    # Инициализация каскадного классификатора для обнаружения лиц
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Запуск видеопотока с камеры (обычно 0 - встроенная камера, 1 - внешняя камера)
    cap = cv2.VideoCapture(1)

    while True:
        # Чтение кадра из видеопотока
        ret, frame = cap.read()

        # Зеркальное отражение кадра по горизонтали
        frame = cv2.flip(frame, 1)

        # Преобразование кадра в оттенки серого для улучшения работы алгоритма
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Обнаружение лиц на кадре
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        # Отрисовка прямоугольников вокруг обнаруженных лиц
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Отображение кадра с обозначенными лицами
        cv2.imshow('Real-time Face Detection (Mirrored)', frame)

        # Прерывание цикла при нажатии клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Освобождение ресурсов и закрытие окна
    cap.release()
    cv2.destroyAllWindows()

# Запуск функции для обнаружения лиц в реальном времени с зеркальным отражением
detect_faces_realtime_mirror()
