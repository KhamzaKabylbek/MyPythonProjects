import cv2
import numpy as np

image_path = 'Apple.jpg'
image = cv2.imread(image_path)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

sift = cv2.SIFT_create()

keypoints, descriptors = sift.detectAndCompute(gray_image, None)

image_with_keypoints = cv2.drawKeypoints(image, keypoints, None)
e1 = cv2.getTickCount()
e2 = cv2.getTickCount()
time_sift = (e2 - e1) / cv2.getTickFrequency()

print("Время выполнения алгоритма SIFT:", time_sift)
cv2.imshow("Image with SIFT Keypoints", image_with_keypoints)
cv2.waitKey(0)
cv2.destroyAllWindows()
