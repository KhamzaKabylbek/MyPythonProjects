import cv2
import mediapipe as mp
from math import hypot
import subprocess
import numpy as np


def set_brightness(brightness):
    brightness = brightness * 100
    brightness = max(0, min(brightness, 100))
    applescript = f'tell application "System Events" to set brightness of display 1 to {brightness}'
    subprocess.run(['osascript', '-e', applescript], capture_output=True)



# Функция для управления громкостью звука
def set_volume(volume):
    subprocess.run(['osascript', '-e', f'set volume output volume {volume}'])


# Захват видеопотока с камеры
cap = cv2.VideoCapture(1)

# Инициализация объектов для обнаружения рук с помощью Mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.75)
mpDraw = mp.solutions.drawing_utils

# Минимальное и максимальное значения громкости
volMin, volMax = 0, 100

while True:
    # Получение кадра из видеопотока
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    left_lmList, right_lmList = [], []

    # Обработка результатов обнаружения рук
    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            if handedness.classification[0].label.lower() == 'left':
                for lm in hand_landmarks.landmark:
                    h, w, _ = img.shape
                    left_lmList.append([int(lm.x * w), int(lm.y * h)])
                mpDraw.draw_landmarks(img, hand_landmarks, mpHands.HAND_CONNECTIONS)
            elif handedness.classification[0].label.lower() == 'right':
                for lm in hand_landmarks.landmark:
                    h, w, _ = img.shape
                    right_lmList.append([int(lm.x * w), int(lm.y * h)])
                mpDraw.draw_landmarks(img, hand_landmarks, mpHands.HAND_CONNECTIONS)

    # Обработка движений левой руки
    if left_lmList:
        x1, y1 = left_lmList[4][0], left_lmList[4][1]
        x2, y2 = left_lmList[8][0], left_lmList[8][1]

        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

        length = hypot(x2 - x1, y2 - y1)

        bright = np.interp(length, [15, 200], [0, 1])
        print(bright, length)
        set_brightness(bright)

    # Обработка движений правой руки
    if right_lmList:
        x1, y1 = right_lmList[4][0], right_lmList[4][1]
        x2, y2 = right_lmList[8][0], right_lmList[8][1]

        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

        length = hypot(x2 - x1, y2 - y1)

        vol = np.interp(length, [15, 200], [volMin, volMax])
        print(vol, length)
        set_volume(vol)

    # Отображение изображения
    cv2.imshow('Image', img)

    # Выход из цикла при нажатии клавиши 'q'
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

# Освобождение ресурсов и закрытие окон
cap.release()
cv2.destroyAllWindows()
