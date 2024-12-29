import numpy as np
import cv2 as cv

brush_color = [80, 80, 80]
brush_size = 2
drawing = False

def draw_circle(event, x, y, flags, param):
    global brush_color, brush_size, drawing
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            cv.circle(img, (x, y), brush_size, brush_color, -1)
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        cv.circle(img, (x, y), brush_size, brush_color, -1)

def changeColor(x):
    global brush_color
    blue = cv.getTrackbarPos('Blue', 'image')
    green = cv.getTrackbarPos('Green', 'image')
    red = cv.getTrackbarPos('Red', 'image')
    brush_color = [blue, green, red]

def changeSize(x):
    global brush_size
    brush_size = cv.getTrackbarPos('brush-size', 'image')

img = np.full((512, 512, 3), 255, dtype=np.uint8)
cv.namedWindow('image')

cv.createTrackbar('Blue', 'image', 80, 255, changeColor)
cv.createTrackbar('Green', 'image', 80, 255, changeColor)
cv.createTrackbar('Red', 'image', 80, 255, changeColor)
cv.createTrackbar('brush-size', 'image', 2, 5, changeSize)

cv.setMouseCallback('image', draw_circle)

while True:
    cv.imshow('image', img)
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()