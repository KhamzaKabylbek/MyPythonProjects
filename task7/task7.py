import cv2
import numpy as np
import matplotlib.pyplot as plt

def mouse_callback(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
        points.append((x, y))
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow('Select Points', img)

image_path = '3.jpg'

img = cv2.imread(image_path)

rows, cols, ch = img.shape

points = []

cv2.namedWindow('Select Points')
cv2.setMouseCallback('Select Points', mouse_callback)

cv2.imshow('Select Points', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

assert len(points) == 4, "Please select exactly four points."

pts1 = np.float32(points)
pts2 = np.float32([[0, 0], [cols, 0], [0, rows], [cols, rows]])

M = cv2.getPerspectiveTransform(pts1, pts2)

dst = cv2.warpPerspective(img, M, (cols, rows))

plt.subplot(121), plt.imshow(img), plt.title('Input')
plt.subplot(122), plt.imshow(dst), plt.title('Output')
plt.show()
