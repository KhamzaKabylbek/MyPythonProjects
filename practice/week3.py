import cv2
import numpy as np

image = cv2.imread('../task15/Apple.jpg')

blue_value = 80
green_value = 80
red_value = 80

def update_values(x):
    global blue_value, green_value, red_value
    blue_value = cv2.getTrackbarPos('Blue', 'image')
    green_value = cv2.getTrackbarPos('Green', 'image')
    red_value = cv2.getTrackbarPos('Red', 'image')
    update_image()

def update_image():
    global image, blue_value, green_value, red_value
    updated_image = np.copy(image)
    updated_image[:, :, 0] = np.clip(updated_image[:, :, 0] + blue_value - 80, 0, 255)
    updated_image[:, :, 1] = np.clip(updated_image[:, :, 1] + green_value - 80, 0, 255)
    updated_image[:, :, 2] = np.clip(updated_image[:, :, 2] + red_value - 80, 0, 255)
    cv2.imshow('image', updated_image)

cv2.namedWindow('image')
cv2.createTrackbar('Blue', 'image', 80, 255, update_values)
cv2.createTrackbar('Green', 'image', 80, 255, update_values)
cv2.createTrackbar('Red', 'image', 80, 255, update_values)

update_image()
cv2.waitKey(0)
cv2.destroyAllWindows()

