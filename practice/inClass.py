import cv2 as cv
import numpy as np

cap = cv.VideoCapture(1)

while True:
    _, frame = cap.read()

    if frame is None:
        print("Error: Could not read frame.")
        break

    # Mirror the frame horizontally
    frame = cv.flip(frame, 1)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])

    mask = cv.inRange(hsv, lower_green, upper_green)

    res = cv.bitwise_and(frame, frame, mask=mask)

    cv.imshow('frame', frame)
    cv.imshow('res', res)

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()
cap.release()
