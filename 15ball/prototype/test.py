import cv2
import numpy as np
import mediapipe as mp
from collections import deque

# Добавляем функцию изменения толщины кисти с клавиатуры
brush_thickness = 3  # Изначальная толщина кисти
# initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

eraser_color = (0, 0, 0)  # Black color for the eraser

# Giving different arrays to handle colour points of different colour
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]
opoints = [deque(maxlen=1024)]  # Define opoints for storing orange points
# These indexes will be used to mark the points in particular arrays of specific colour
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0
orange_index = 0  # Initialize orange_index
#The kernel to be used for dilation purpose
kernel = np.ones((5,5),np.uint8)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (0, 128, 255), (128, 0, 128), eraser_color]
colorIndex = 0
# Inside the drawing loop...



def draw_circle_with_white_border(image, center, radius, color, border_thickness):
    # Draw filled circle
    cv2.circle(image, center, radius, color, -1)

    # Draw white border
    border_color = (255, 255, 255)
    cv2.circle(image, center, radius, border_color, border_thickness)

# Initialize the webcam
cap = cv2.VideoCapture(1)
ret = True
while ret:
    # Read each frame from the webcam
    ret, frame = cap.read()

    x, y, c = frame.shape

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Here is code for Canvas setup
    paintWindow = np.zeros((x, y, 3)) + 0
    paintWindow = cv2.circle(paintWindow, (70, 50), 40, (255, 255, 255), -1)
    paintWindow = cv2.circle(paintWindow, (200, 50), 40, (255, 0, 0), -1)
    paintWindow = cv2.circle(paintWindow, (330, 50), 40, (0, 255, 0), -1)
    paintWindow = cv2.circle(paintWindow, (460, 50), 40, (0, 0, 255), -1)
    paintWindow = cv2.circle(paintWindow, (585, 50), 40, (0, 255, 255), -1)
    paintWindow = cv2.circle(paintWindow, (715, 50), 40, (0, 128, 255), -1)  # Orange color button
    paintWindow = cv2.circle(paintWindow, (845, 50), 40, (128, 0, 128), -1)  # Purple color button
    paintWindow = cv2.circle(paintWindow, (975, 50), 40, (255, 255, 255), -1)  # Eraser button

    cv2.putText(paintWindow, "CLEAR", (45, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "BLUE", (175, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "GREEN", (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "RED", (440, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "YELLOW", (555, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "ORANGE", (685, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)  # Orange color button
    cv2.putText(paintWindow, "PURPLE", (815, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)  # Purple color button
    cv2.putText(paintWindow, "ERASER", (945, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)  # Eraser button
    cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

    frame = cv2.circle(frame, (70, 50), 40, (255, 255, 255), -1)
    frame = cv2.circle(frame, (200, 50), 40, (255, 0, 0), -1)
    frame = cv2.circle(frame, (330, 50), 40, (0, 255, 0), -1)
    frame = cv2.circle(frame, (460, 50), 40, (0, 0, 255), -1)
    frame = cv2.circle(frame, (585, 50), 40, (0, 255, 255), -1)
    frame = cv2.circle(frame, (715, 50), 40, (0, 128, 255), -1)  # Orange color button
    frame = cv2.circle(frame, (845, 50), 40, (128, 0, 128), -1)  # Purple color button
    frame = cv2.circle(frame, (975, 50), 40, (255, 255, 255), -1)  # Eraser button

    cv2.putText(frame, "CLEAR", (45, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (175, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (440, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (555, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "ORANGE", (685, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)  # Orange color button
    cv2.putText(frame, "PURPLE", (815, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)  # Purple color button
    cv2.putText(frame, "ERASER", (945, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)  # Eraser button

    # Get hand landmark prediction
    result = hands.process(framergb)

    # post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int(lm.x * y)
                lmy = int(lm.y * x)
                landmarks.append([lmx, lmy])

            # Drawing landmarks on frames
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
            opoints.append(deque(maxlen=512))  # Append new deque for orange points
            orange_index += 1  # Increment orange_index

        elif center[1] <= 90:
            if 30 <= center[0] <= 110: # Clear Button
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]
                opoints = [deque(maxlen=512)]  # Reset opoints
                blue_index = 0
                green_index = 0
                red_index = 0
                yellow_index = 0
                orange_index = 0  # Reset orange_index

                paintWindow[100:,:,:] = 0
            elif 160<= center[0] <= 240:
                    colorIndex = 0 # Blue
            elif 290 <= center[0] <= 370:
                    colorIndex = 1 # Green
            elif 420<= center[0] <= 500:
                    colorIndex = 2 # Red
            elif 545 <= center[0] <= 665:
                    colorIndex = 3 # Yellow
            elif 675 <= center[0] <= 755:  # Orange color button
                    colorIndex = 4  # Orange
            elif 805 <= center[0] <= 885:  # Purple color button
                    colorIndex = 5  # Purple
            elif 935 <= center[0] <= 1015:  # Eraser button
                    colorIndex = -1  # Eraser
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
                opoints[orange_index].appendleft(center)  # Append points to opoints for orange color
            elif colorIndex == 5:
                pass  # Handle purple color if needed
            elif colorIndex == -1:
                pass  # Handle eraser functionality

    # Append the next deques when nothing is detected to avoid messing up
    else:
        bpoints.append(deque(maxlen=512))
        blue_index += 1
        gpoints.append(deque(maxlen=512))
        green_index += 1
        rpoints.append(deque(maxlen=512))
        red_index += 1
        ypoints.append(deque(maxlen=512))
        yellow_index += 1
        opoints.append(deque(maxlen=512))  # Append new deque for orange points
        orange_index += 1  # Increment orange_index

    # Draw lines of all the colors on the canvas and frame
    points = [bpoints, gpoints, rpoints, ypoints, opoints]  # Include opoints
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                # Inside the drawing loop...

                if colorIndex == -1:  # Eraser selected
                    pass  # Don't draw anything when eraser is selected
                else:
                    if i == 4:  # Check if the color is the eraser color
                        cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i],
                                 brush_thickness * 2)  # Draw with the selected color
                        cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i],
                                 brush_thickness * 2)  # Draw on the paint window with the selected color
                    else:
                        cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i],
                                 brush_thickness * 2)  # Draw with the selected color
                        cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i],
                                 brush_thickness * 2)  # Draw on the paint window with the selected color

    cv2.imshow("Output", frame)
    cv2.imshow("Paint", paintWindow)

    if cv2.waitKey(1) == ord('q'):
        break

# release the webcam and destroy all active windows
cap.release()
cv2.destroyAllWindows()
