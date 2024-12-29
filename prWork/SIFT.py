import cv2 as cv
img = cv.imread('IMG_9566-720x404.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

sift = cv.SIFT_create()

kp = sift.detect(gray, None)

kp, des = sift.compute(gray, kp)

img_with_rich_keypoints = cv.drawKeypoints(gray, kp, img, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv.imwrite('sift.jpg', img_with_rich_keypoints)

