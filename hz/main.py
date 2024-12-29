from pynput.keyboard import Key, Controller
import cv2
from cvzone.HandTrackingModule import HandDetector
import time

# Инициализация клавиатуры и детектора
keyboard = Controller()
detector = HandDetector(detectionCon=0.8, maxHands=1)
time.sleep(2.0)

# Видеозахват
video = cv2.VideoCapture(1)

while True:
    ret, frame = video.read()
    hands, img = detector.findHands(frame)

    # Рисуем области на изображении
    cv2.rectangle(img, (0, 480), (300, 425), (145, 243, 246), -2)
    cv2.rectangle(img, (640, 480), (400, 425), (145, 243, 246), -2)

    if hands:
        lnList = hands[0]
        fingerUp = detector.fingersUp(lnList)

        # Определяем действия в зависимости от поднятых пальцев
        if fingerUp == [0, 0, 0, 0, 0]:  # Все пальцы опущены
            cv2.putText(frame, "finger Count :0", (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "JUMPING", (420, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            keyboard.press(Key.space)
            keyboard.release(Key.space)

        elif fingerUp == [0, 1, 0, 0, 0]:  # Один палец поднят
            cv2.putText(frame, "finger Count :1", (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "NOT JUMPING", (420, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # Отображение кадра
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):  # Выход из программы по нажатию 'q'
        break

video.release()
cv2.destroyAllWindows()
