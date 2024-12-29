# import cv2
# import mediapipe as mp
# import numpy as np  # Добавляем импорт NumPy
#
#
# cap = cv2.VideoCapture(1)
#
# mpHands = mp.solutions.hands
# hands = mpHands.Hands()
# mpDraw = mp.solutions.drawing_utils
#
# # Переменные для хранения предыдущего и текущего положения указательного пальца
# prev_x, prev_y = 0, 0
# curr_x, curr_y = 0, 0
#
# # Переменная для хранения состояния рисования (включено/выключено)
# drawing = False
#
# # Создаем холст
# canvas = None
# canvas_copy = None
#
# while True:
#     success, img = cap.read()
#     img = cv2.flip(img, 1)  # Зеркальное отражение изображения
#     imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(imgRGB)
#
#     if results.multi_hand_landmarks:
#         for handlandmark in results.multi_hand_landmarks:
#             for id, lm in enumerate(handlandmark.landmark):
#                 h, w, _ = img.shape
#                 cx, cy = int(lm.x * w), int(lm.y * h)
#
#                 if id == 8:  # Индекс указательного пальца
#                     if drawing:
#                         if canvas is not None and canvas_copy is not None:
#                             cv2.line(canvas, (prev_x, prev_y), (cx, cy), (0, 0, 255), 5)
#                             cv2.line(canvas_copy, (prev_x, prev_y), (cx, cy), (0, 0, 255), 5)
#                     prev_x, prev_y = curr_x, curr_y
#                     curr_x, curr_y = cx, cy
#
#                     # Проверяем состояние указательного пальца (согнут или разогнут)
#                     if lm.y < handlandmark.landmark[mpHands.HandLandmark.MIDDLE_FINGER_DIP].y:
#                         drawing = True
#                     else:
#                         drawing = False
#
#             mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS)
#
#     # Если рисование включено, показываем холст
#     if drawing:
#         if canvas is None:
#             canvas = np.zeros_like(img)
#             canvas_copy = canvas.copy()
#         img = cv2.addWeighted(img, 0.5, canvas_copy, 0.5, 0)
#
#     cv2.imshow('Image', img)
#     if cv2.waitKey(1) & 0xff == ord('q'):
#         break
#
# # Освобождаем ресурсы
# cap.release()
# cv2.destroyAllWindows()


import cv2
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(1)

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Переменные для хранения предыдущего и текущего положения указательного пальца
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0

# Переменная для хранения состояния рисования (включено/выключено)
drawing = False

# Создаем холст
canvas = None
canvas_copy = None

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Зеркальное отражение изображения
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handlandmark in results.multi_hand_landmarks:
            for id, lm in enumerate(handlandmark.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                # Применяем фильтрацию для сглаживания движений
                cx = int(prev_x * 0.5 + cx * 0.5)
                cy = int(prev_y * 0.5 + cy * 0.5)

                if id == 8:  # Индекс указательного пальца
                    if drawing:
                        if canvas is not None and canvas_copy is not None:
                            cv2.line(canvas, (prev_x, prev_y), (cx, cy), (0, 0, 255), 5)
                            cv2.line(canvas_copy, (prev_x, prev_y), (cx, cy), (0, 0, 255), 5)
                    prev_x, prev_y = curr_x, curr_y
                    curr_x, curr_y = cx, cy

                    # Проверяем состояние указательного пальца (согнут или разогнут)
                    if lm.y < handlandmark.landmark[mpHands.HandLandmark.MIDDLE_FINGER_DIP].y:
                        drawing = True
                    else:
                        drawing = False

            mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS)

    # Если рисование включено, показываем холст
    if drawing:
        if canvas is None:
            canvas = np.zeros_like(img)
            canvas_copy = canvas.copy()
        img = cv2.addWeighted(img, 0.5, canvas_copy, 0.5, 0)

    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

# Освобождаем ресурсы
cap.release()
cv2.destroyAllWindows()
