import cv2
import numpy as np

def trackbar_low(value):
    global low_threshold
    low_threshold = value
    update_edges()

def trackbar_high(value):
    global high_threshold
    high_threshold = value
    update_edges()

def update_edges():
    edges = cv2.Canny(gray_image, low_threshold, high_threshold)
    cv2.imshow('Edge Detection', edges)

image = cv2.imread('Apple — копия 2.jpg')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

low_threshold = 50
high_threshold = 50

cv2.namedWindow('Edge Detection')

cv2.createTrackbar('Low Threshold', 'Edge Detection', low_threshold, 200, trackbar_low)
cv2.createTrackbar('High Threshold', 'Edge Detection', high_threshold, 200, trackbar_high)

update_edges()

cv2.waitKey(0)
cv2.destroyAllWindows()
