import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def onmouse(event, x, y, flags, param):
    global rect, drawing, rectangle
    if event == cv.EVENT_RBUTTONDOWN:
        rectangle = True
        rect = (x, y, 1, 1)
        drawing = False
    elif event == cv.EVENT_RBUTTONUP and rectangle:
        rectangle = False
        rect = (rect[0], rect[1], x - rect[0], y - rect[1])
        rect_or_mask = 0  # Assuming rect is selected for background initially
        try:
            bgd_model = np.zeros((1, 65), np.float64)
            fgd_model = np.zeros((1, 65), np.float64)
            cv.grabCut(img, mask, rect, bgd_model, fgd_model, 5, cv.GC_INIT_WITH_RECT)
        except:
            import traceback
            traceback.print_exc()

# Load the image
img = cv.imread('messi5.jpg')
assert img is not None, "File could not be read, check with os.path.exists()"

# Initialize variables
mask = np.zeros(img.shape[:2], np.uint8)
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)
rect = (0, 0, 1, 1)  # Default rectangle
drawing = False
rectangle = False

# Create windows and set the mouse callback
cv.namedWindow('image')
cv.setMouseCallback('image', onmouse)

while True:
    img2 = img.copy()

    if rectangle:
        cv.rectangle(img2, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 2)

    cv.imshow('image', img2)
    k = cv.waitKey(1) & 0xFF

    if k == 27:  # ESC key to exit
        break

cv.destroyAllWindows()
