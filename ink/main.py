import numpy as np
import cv2
from collections import deque

# Определение границ цвета для распознавания "синего"
blueLower = np.array([105, 50, 50])
blueUpper = np.array([125, 255, 255])

# Ядро для морфологических преобразований
kernel = np.ones((5, 5), np.uint8)

# Очереди для хранения точек каждого цвета
bpoints = [deque(maxlen=512)]
gpoints = [deque(maxlen=512)]
rpoints = [deque(maxlen=512)]
ypoints = [deque(maxlen=512)]

bindex = 0
gindex = 0
rindex = 0
yindex = 0

# Цвета в формате (B, G, R)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

# Подключение к камере
camera = cv2.VideoCapture(1)

# Получение размера кадра из камеры
ret, frame = camera.read()
if not ret:
    print("Не удалось получить кадр с камеры.")
    camera.release()
    cv2.destroyAllWindows()
    exit()

frame_height, frame_width, _ = frame.shape

# Создание интерфейса Paint с тем же размером, что и кадр
Paint = np.zeros((frame_height, frame_width, 3), dtype=np.uint8) + 255

# Добавление инструментов на интерфейс Paint
Paint = cv2.rectangle(Paint, (40, 41), (140, 105), (0, 0, 0), 2)
Paint = cv2.rectangle(Paint, (160, 41), (255, 105), colors[0], -1)
Paint = cv2.rectangle(Paint, (275, 41), (370, 105), colors[1], -1)
Paint = cv2.rectangle(Paint, (390, 41), (485, 105), colors[2], -1)
Paint = cv2.rectangle(Paint, (505, 41), (600, 105), colors[3], -1)
cv2.putText(Paint, "CLEAR ALL", (49, 73), cv2.FONT_ITALIC, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(Paint, "BLUE", (185, 73), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(Paint, "GREEN", (298, 73), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(Paint, "RED", (420, 73), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(Paint, "YELLOW", (520, 73), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 2, cv2.LINE_AA)

# Основной цикл программы
while True:
    # Получение текущего кадра
    grabbed, frame = camera.read()
    if not grabbed:
        break

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Добавление инструментов на кадр
    frame = cv2.rectangle(frame, (40, 41), (140, 105), (122, 122, 122), -1)
    frame = cv2.rectangle(frame, (160, 41), (255, 105), colors[0], -1)
    frame = cv2.rectangle(frame, (275, 41), (370, 105), colors[1], -1)
    frame = cv2.rectangle(frame, (390, 41), (485, 105), colors[2], -1)
    frame = cv2.rectangle(frame, (505, 41), (600, 105), colors[3], -1)
    cv2.putText(frame, "CLEAR ALL", (49, 73), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 73), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (298, 73), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (420, 73), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (520, 73), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 2, cv2.LINE_AA)

    # Определение маски для синего цвета
    blueMask = cv2.inRange(hsv, blueLower, blueUpper)

    # Преобразования для маски
    blueMask = cv2.erode(blueMask, kernel, iterations=2)
    blueMask = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, kernel)
    blueMask = cv2.dilate(blueMask, kernel, iterations=1)

    # Поиск контуров
    cnts, _ = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None

    # Если контуры найдены
    if len(cnts) > 0:
        cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

        if center[1] <= 105:
            if 40 <= center[0] <= 140:  # Очистить все
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]
                bindex = gindex = rindex = yindex = 0
                Paint[107:, :, :] = 255
            elif 160 <= center[0] <= 255:
                colorIndex = 0  # Синий
            elif 275 <= center[0] <= 370:
                colorIndex = 1  # Зеленый
            elif 390 <= center[0] <= 485:
                colorIndex = 2  # Красный
            elif 505 <= center[0] <= 600:
                colorIndex = 3  # Желтый
        else:
            if colorIndex == 0:
                bpoints[bindex].appendleft(center)
            elif colorIndex == 1:
                gpoints[gindex].appendleft(center)
            elif colorIndex == 2:
                rpoints[rindex].appendleft(center)
            elif colorIndex == 3:
                ypoints[yindex].appendleft(center)
    else:
        bpoints.append(deque(maxlen=512))
        gpoints.append(deque(maxlen=512))
        rpoints.append(deque(maxlen=512))
        ypoints.append(deque(maxlen=512))

    # Рисование линий
    points = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.line(Paint, points[i][j][k - 1], points[i][j][k], colors[i], 2)

    # Показ окон
    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", Paint)

    # Обработка нажатий клавиш
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):  # Выход
        break
    elif key == ord("s"):  # Сохранить
        filename = "drawing.png"
        cv2.imwrite(filename, Paint)
        print(f"Изображение сохранено как {filename}")

# Очистка ресурсов
camera.release()
cv2.destroyAllWindows()
