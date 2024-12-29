import cv2
import numpy as np

image_path = 'Apple.jpg'
image = cv2.imread(image_path)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
block_size = 2
aperture_size = 3
k = 0.04
dst = cv2.cornerHarris(gray_image, block_size, aperture_size, k)

dst = cv2.dilate(dst, None)

image[dst > 0.01 * dst.max()] = [0, 0, 255]

harris_detector = cv2.cornerHarris(gray_image, blockSize=2, ksize=3, k=0.04)
e1 = cv2.getTickCount()
e2 = cv2.getTickCount()
time_harris = (e2 - e1) / cv2.getTickFrequency()
print("Время выполнения алгоритма Харриса:", time_harris)

cv2.imshow('Harris Corner Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
