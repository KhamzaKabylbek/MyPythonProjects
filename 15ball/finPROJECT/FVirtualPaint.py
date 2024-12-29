import cv2
import numpy as np
import mediapipe as mp
from collections import deque

brush_thickness = 2

bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]
opoints = [deque(maxlen=1024)]
ppoints = [deque(maxlen=1024)]

blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0
orange_index = 0
purple_index = 0

kernel = np.ones((5,5),np.uint8)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (0, 128, 255), (128, 0, 128)]
colorIndex = 0

def draw_circle_with_white_border(image, center, radius, color, border_thickness):
    cv2.circle(image, center, radius, color, -1)

    border_color = (255, 255, 255)
    cv2.circle(image, center, radius, border_color, border_thickness)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(1)
ret = True
while ret:
    ret, frame = cap.read()

    x, y, c = frame.shape

    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    paintWindow = np.zeros((x, y, 3)) + 0
    paintWindow = cv2.circle(paintWindow, (70, 50), 40, (255, 255, 255), -1)
    paintWindow = cv2.circle(paintWindow, (200, 50), 40, (255, 0, 0), -1)
    paintWindow = cv2.circle(paintWindow, (330, 50), 40, (0, 255, 0), -1)
    paintWindow = cv2.circle(paintWindow, (460, 50), 40, (0, 0, 255), -1)
    paintWindow = cv2.circle(paintWindow, (585, 50), 40, (0, 255, 255), -1)
    paintWindow = cv2.circle(paintWindow, (710, 50), 40, (0, 128, 255), -1)
    paintWindow = cv2.circle(paintWindow, (840, 50), 40, (128, 0, 128), -1)

    cv2.putText(paintWindow, "CLEAR", (45, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "BLUE", (175, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "GREEN", (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "RED", (440, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "YELLOW", (555, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "ORANGE", (675, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "PURPLE", (805, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

    cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

    frame = cv2.circle(frame, (70, 50), 40, (255, 255, 255), -1)
    frame = cv2.circle(frame, (200, 50), 40, (255, 0, 0), -1)
    frame = cv2.circle(frame, (330, 50), 40, (0, 255, 0), -1)
    frame = cv2.circle(frame, (460, 50), 40, (0, 0, 255), -1)
    frame = cv2.circle(frame, (585, 50), 40, (0, 255, 255), -1)
    frame = cv2.circle(frame, (710, 50), 40, (0, 128, 255), -1)
    frame = cv2.circle(frame, (840, 50), 40, (128, 0, 128), -1)

    cv2.putText(frame, "CLEAR", (45, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (175, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (440, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (555, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "ORANGE", (675, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "PURPLE", (805, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

    result = hands.process(framergb)

    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int(lm.x * y)
                lmy = int(lm.y * x)
                landmarks.append([lmx, lmy])

            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
        fore_finger = (landmarks[8][0],landmarks[8][1])
        center = fore_finger
        thumb = (landmarks[4][0],landmarks[4][1])
        cv2.circle(frame, center, 3, (0,255,0),-1)

        if (thumb[1]-center[1]<30):
            bpoints.append(deque(maxlen=512))
            blue_index += 1
            gpoints.append(deque(maxlen=512))
            green_index += 1
            rpoints.append(deque(maxlen=512))
            red_index += 1
            ypoints.append(deque(maxlen=512))
            yellow_index += 1
            opoints.append(deque(maxlen=512))
            orange_index += 1
            ppoints.append(deque(maxlen=512))
            purple_index += 1

        elif center[1] <= 90:
            if 30 <= center[0] <= 110:
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]
                opoints = [deque(maxlen=512)]
                ppoints = [deque(maxlen=512)]

                blue_index = 0
                green_index = 0
                red_index = 0
                yellow_index = 0
                orange_index = 0
                purple_index = 0

                paintWindow[100:,:,:] = 0
            elif 160<= center[0] <= 240:
                    colorIndex = 0 # Blue
            elif 290 <= center[0] <= 370:
                    colorIndex = 1 # Green
            elif 420<= center[0] <= 500:
                    colorIndex = 2 # Red
            elif 545 <= center[0] <= 665:
                    colorIndex = 3 # Yellow
            elif 675 <= center[0] <= 755:  #orange
                    colorIndex = 4  # Orange
            elif 805 <= center[0] <= 885:  # purple
                    colorIndex = 5  # Purple
        else :
            if colorIndex == 0:
                bpoints[blue_index].appendleft(center)
            elif colorIndex == 1:
                gpoints[green_index].appendleft(center)
            elif colorIndex == 2:
                rpoints[red_index].appendleft(center)
            elif colorIndex == 3:
                ypoints[yellow_index].appendleft(center)
            elif colorIndex == 4:
                opoints[orange_index].appendleft(center)
            elif colorIndex == 5:
                ppoints[purple_index].appendleft(center)
    else:
        bpoints.append(deque(maxlen=512))
        blue_index += 1
        gpoints.append(deque(maxlen=512))
        green_index += 1
        rpoints.append(deque(maxlen=512))
        red_index += 1
        ypoints.append(deque(maxlen=512))
        yellow_index += 1
        opoints.append(deque(maxlen=512))
        orange_index += 1
        ppoints.append(deque(maxlen=512))
        purple_index += 1

    points = [bpoints, gpoints, rpoints, ypoints, opoints, ppoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], brush_thickness * 2)
                cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], brush_thickness * 2)

    cv2.imshow("Output", frame)
    cv2.imshow("Paint", paintWindow)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
