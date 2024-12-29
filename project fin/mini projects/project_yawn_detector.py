import cv2
import numpy as np
import face_recognition

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(imgRGB)
    face_landmarks_list = face_recognition.face_landmarks(imgRGB)

    for (top, right, bottom, left), landmarks in zip(face_locations, face_landmarks_list):
        # Определение точек рта
        top_lip_point = landmarks['top_lip'][0]
        bottom_lip_point = landmarks['bottom_lip'][0]

        # Вычисление длины горизонтальной и вертикальной линий
        hor_line_length = bottom_lip_point[0] - top_lip_point[0]
        ver_line_length = bottom_lip_point[1] - top_lip_point[1]

        # Расчет отношения длин
        mouth_ratio = hor_line_length / ver_line_length

        # Если отношение длин меньше порогового значения, считаем, что человек зевает
        if mouth_ratio < 1.65:
            cv2.putText(img, "Yawning", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        # Рисуем рамку вокруг лица
        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 3)

    cv2.imshow('Facial Landmark Detection', img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
