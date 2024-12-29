import dlib
import cv2
import numpy as np
from scipy.spatial import distance as dist
import tkinter as tk

# source /Users/hamza/PycharmProjects/pythonProject/venv_py39/bin/activate

def calculate_distance(point1, point2):
    return dist.euclidean((point1.x, point1.y), (point2.x, point2.y))


def apply_mask(face_img, mask_img, landmarks):
    mask_width = int(calculate_distance(landmarks.part(17), landmarks.part(26)) * 1.5)
    mask_height = int(mask_width * (mask_img.shape[0] / mask_img.shape[1]))
    mask_resized = cv2.resize(mask_img, (mask_width, mask_height))

    top_left = (int(landmarks.part(1).x - mask_width / 10), int(landmarks.part(17).y - mask_height / 10))
    bottom_right = (top_left[0] + mask_resized.shape[1], top_left[1] + mask_resized.shape[0])

    if top_left[0] >= 0 and top_left[1] >= 0 and bottom_right[0] <= face_img.shape[1] and bottom_right[1] <= face_img.shape[0]:
        mask_area = face_img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        mask_gray = cv2.cvtColor(mask_resized, cv2.COLOR_BGR2GRAY)
        ret, mask_mask = cv2.threshold(mask_gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask_mask)

        face_no_mask = cv2.bitwise_and(mask_area, mask_area, mask=mask_inv)
        mask_area_masked = cv2.bitwise_and(mask_resized, mask_resized, mask=mask_mask)

        face_img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]] = cv2.add(face_no_mask, mask_area_masked)

    return face_img


def apply_glasses(face_img, glasses_img, eye_center):
    glasses_width = int(face_width)
    glasses_height = int(glasses_img.shape[0] / glasses_img.shape[1] * glasses_width)
    glasses_resized = cv2.resize(glasses_img, (glasses_width, glasses_height))

    glasses_top_left = (int(eye_center[0] - glasses_width / 2), int(eye_center[1] - glasses_height / 2))
    glasses_bottom_right = (glasses_top_left[0] + glasses_width, glasses_top_left[1] + glasses_height)

    if glasses_top_left[0] >= 0 and glasses_top_left[1] >= 0 and glasses_bottom_right[0] <= face_img.shape[1] and glasses_bottom_right[1] <= face_img.shape[0]:
        glasses_area = face_img[glasses_top_left[1]:glasses_bottom_right[1], glasses_top_left[0]:glasses_bottom_right[0]]

        glasses_mask_gray = cv2.cvtColor(glasses_resized, cv2.COLOR_BGR2GRAY)
        ret, glasses_mask = cv2.threshold(glasses_mask_gray, 10, 255, cv2.THRESH_BINARY)
        glasses_mask_inv = cv2.bitwise_not(glasses_mask)

        glasses_mask_inv = glasses_mask_inv.astype(np.uint8)

        face_no_glasses = cv2.bitwise_and(glasses_area, glasses_area, mask=glasses_mask_inv)
        glasses_area_masked = cv2.bitwise_and(glasses_resized, glasses_resized, mask=glasses_mask)

        face_img[glasses_top_left[1]:glasses_bottom_right[1], glasses_top_left[0]:glasses_bottom_right[0]] = cv2.add(face_no_glasses, glasses_area_masked)

    return face_img


def apply_flow_mask(face_img, mask_img, landmarks):
    mask_width = int(calculate_distance(landmarks.part(10), landmarks.part(20)))


    scale_factor = 0.3
    mask_width = int(mask_width * scale_factor)
    mask_height = int(mask_width * (mask_img.shape[0] / mask_img.shape[1]))
    mask_resized = cv2.resize(mask_img, (mask_width, mask_height))

    shift_left = 50

    top_left = (int(landmarks.part(1).x - mask_width / 8) - shift_left, int(landmarks.part(17).y - mask_height / 2))
    bottom_right = (top_left[0] + mask_resized.shape[1], top_left[1] + mask_resized.shape[0])

    if top_left[0] >= 0 and top_left[1] >= 0 and bottom_right[0] <= face_img.shape[1] and bottom_right[1] <= \
            face_img.shape[0]:
        mask_area = face_img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        mask_gray = cv2.cvtColor(mask_resized, cv2.COLOR_BGR2GRAY)
        ret, mask_mask = cv2.threshold(mask_gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask_mask)

        face_no_mask = cv2.bitwise_and(mask_area, mask_area, mask=mask_inv)
        mask_area_masked = cv2.bitwise_and(mask_resized, mask_resized, mask=mask_mask)

        face_img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]] = cv2.add(face_no_mask, mask_area_masked)

    return face_img


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

cap = cv2.VideoCapture(1)

mask_img = cv2.imread('maskback.png')
glasses_img = cv2.imread('glassBlur.png')
flow_mask_img = cv2.imread('flow.png')

mask_mode = False
glasses_mode = False
flow_mode = False

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)


    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(imgGray)

    for face in faces:
        landmarks = predictor(imgGray, face)

        if mask_mode:
            img = apply_mask(img, mask_img, landmarks)
        elif glasses_mode:
            face_width = calculate_distance(landmarks.part(1), landmarks.part(16))
            eye_center = ((landmarks.part(42).x + landmarks.part(39).x) // 2, (landmarks.part(42).y + landmarks.part(39).y) // 2)
            img = apply_glasses(img, glasses_img, eye_center)
        elif flow_mode:
            img = apply_flow_mask(img, flow_mask_img, landmarks)

        for i in range(0, 68):
            x = landmarks.part(i).x
            y = landmarks.part(i).y
            cv2.circle(img, (x, y), 2, (0, 255, 0), cv2.FILLED)

    cv2.imshow('Facial Landmark Detection', img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('m'):
        mask_mode = not mask_mode
        glasses_mode = False
        flow_mode = False
    elif key == ord('g'):
        glasses_mode = not glasses_mode
        mask_mode = False
        flow_mode = False
    elif key == ord('f'):
        flow_mode = not flow_mode
        mask_mode = False
        glasses_mode = False
    elif key == ord('j'):
        mask_mode = True
        glasses_mode = True
        flow_mode = False

cap.release()
cv2.destroyAllWindows()