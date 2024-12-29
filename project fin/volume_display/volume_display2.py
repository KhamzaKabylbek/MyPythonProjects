# import cv2
# import mediapipe as mp
# from math import hypot
# import subprocess
# import numpy as np
# import objc
#
# # Define functions to control screen brightness and volume on macOS
# def set_brightness(brightness):
#     brightness = brightness * 100  # Adjust brightness value to be in the range [0, 100]
#     brightness = max(0, min(brightness, 100))  # Ensure brightness is within the valid range
#     # Use AppleScript to set the screen brightness
#     applescript = f'tell application "System Events" to set brightness of first monitor to {brightness}'
#     subprocess.run(['osascript', '-e', applescript], capture_output=True)
#
#
#
# def set_volume(volume):
#     subprocess.run(['osascript', '-e', f'set volume output volume {volume}'])
#
# cap = cv2.VideoCapture(0)
#
# mpHands = mp.solutions.hands
# hands = mpHands.Hands(min_detection_confidence=0.75)
# mpDraw = mp.solutions.drawing_utils
#
# volMin, volMax = 0, 100
#
# while True:
#     success, img = cap.read()
#     img = cv2.flip(img, 1)
#     imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(imgRGB)
#
#     left_lmList, right_lmList = [], []
#     if results.multi_hand_landmarks and results.multi_handedness:
#         for i in results.multi_handedness:
#             label = i.classification[0].label.lower()
#             if label == 'left':
#                 for lm in results.multi_hand_landmarks[0].landmark:
#                     h, w, _ = img.shape
#                     left_lmList.append([int(lm.x * w), int(lm.y * h)])
#                 mpDraw.draw_landmarks(img, results.multi_hand_landmarks[0], mpHands.HAND_CONNECTIONS)
#             if label == 'right':
#                 index = 0
#                 if len(results.multi_hand_landmarks) == 2:
#                     index = 1
#                 for lm in results.multi_hand_landmarks[index].landmark:
#                     h, w, _ = img.shape
#                     right_lmList.append([int(lm.x * w), int(lm.y * h)])
#                     mpDraw.draw_landmarks(img, results.multi_hand_landmarks[index], mpHands.HAND_CONNECTIONS)
#
#     if left_lmList != []:
#         x1, y1 = left_lmList[4][0], left_lmList[4][1]
#         x2, y2 = left_lmList[8][0], left_lmList[8][1]
#
#         cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
#
#         length = hypot(x2 - x1, y2 - y1)
#
#         bright = np.interp(length, [15, 200], [0, 1])
#         print(bright, length)
#         set_brightness(bright)
#
#     if right_lmList != []:
#         x1, y1 = right_lmList[4][0], right_lmList[4][1]
#         x2, y2 = right_lmList[8][0], right_lmList[8][1]
#
#         cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
#
#         length = hypot(x2 - x1, y2 - y1)
#
#         vol = np.interp(length, [15, 200], [volMin, volMax])
#         print(vol, length)
#         set_volume(vol)
#
#     cv2.imshow('Image', img)
#     if cv2.waitKey(1) & 0xff == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()


import cv2
import mediapipe as mp
from math import hypot
import subprocess
import numpy as np
import brightness

def set_brightness(brightness):
    # Convert the brightness value to a valid range (0 to 1)
    brightness = max(0, min(brightness, 1))
    # Use AppleScript to set the screen brightness
    applescript = f'tell application "System Events" to set brightness of display 1 to {brightness}'
    subprocess.run(['osascript', '-e', applescript], capture_output=False)


# Функция для установки громкости звука
def set_volume(volume):
    subprocess.run(['osascript', '-e', f'set volume output volume {volume}'])

cap = cv2.VideoCapture(1)

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.75)
mpDraw = mp.solutions.drawing_utils

volMin, volMax = 0, 100

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    left_lmList, right_lmList = [], []
    if results.multi_hand_landmarks and results.multi_handedness:
        for i in results.multi_handedness:
            label = i.classification[0].label.lower()
            if label == 'left':
                for lm in results.multi_hand_landmarks[0].landmark:
                    h, w, _ = img.shape
                    left_lmList.append([int(lm.x * w), int(lm.y * h)])
                mpDraw.draw_landmarks(img, results.multi_hand_landmarks[0], mpHands.HAND_CONNECTIONS)
            if label == 'right':
                index = 0
                if len(results.multi_hand_landmarks) == 2:
                    index = 1
                for lm in results.multi_hand_landmarks[index].landmark:
                    h, w, _ = img.shape
                    right_lmList.append([int(lm.x * w), int(lm.y * h)])
                    mpDraw.draw_landmarks(img, results.multi_hand_landmarks[index], mpHands.HAND_CONNECTIONS)

    if left_lmList != []:
        x1, y1 = left_lmList[4][0], left_lmList[4][1]
        x2, y2 = left_lmList[8][0], left_lmList[8][1]

        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

        length = hypot(x2 - x1, y2 - y1)

        bright = np.interp(length, [15, 200], [0, 1])
        print(bright, length)
        set_brightness(bright)

    if right_lmList != []:
        x1, y1 = right_lmList[4][0], right_lmList[4][1]
        x2, y2 = right_lmList[8][0], right_lmList[8][1]

        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

        length = hypot(x2 - x1, y2 - y1)

        vol = np.interp(length, [15, 200], [volMin, volMax])
        print(vol, length)
        set_volume(vol)

    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
