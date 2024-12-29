import cv2
import numpy as np
import mediapipe as mp
from collections import deque

cap = cv2.VideoCapture(1)
ret = True

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

def draw_circle_with_white_border(image, center, radius, color, border_thickness):
    cv2.circle(image, center, radius, color, -1)

    border_color = (255, 255, 255)
    cv2.circle(image, center, radius, border_color, border_thickness)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

while ret:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(framergb)
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int(lm.x * frame.shape[1])
                lmy = int(lm.y * frame.shape[0])
                landmarks.append([lmx, lmy])

            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

        fore_finger = (landmarks[8][0], landmarks[8][1])
        center = fore_finger
        thumb = (landmarks[4][0], landmarks[4][1])

        if (thumb[1] - center[1] < 30):
            colorIndex += 1
            if colorIndex >= len(colors):
                colorIndex = 0
        else:
            cv2.circle(frame, center, 5, colors[colorIndex], -1)

    for i, color in enumerate(colors):
        draw_circle_with_white_border(frame, (50 + i * 140, 50), 60, color, 3)


    cv2.imshow("Paint", frame)

    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
