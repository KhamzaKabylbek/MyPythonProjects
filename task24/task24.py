import numpy as np
import cv2

cap = cv2.VideoCapture('slow_traffic_small.mp4')

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_ids = np.random.randint(0, frame_count, size=25)

frames = []
for fid in frame_ids:
    cap.set(cv2.CAP_PROP_POS_FRAMES, fid)
    ret, frame = cap.read()
    if ret:
        frames.append(frame)

median_frame = np.median(frames, axis=0).astype(np.uint8)

cv2.imshow('Median Frame', median_frame)
cv2.waitKey(0)

cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

gray_median_frame = cv2.cvtColor(median_frame, cv2.COLOR_BGR2GRAY)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frame_diff = cv2.absdiff(gray_frame, gray_median_frame)

    _, binary_frame = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)

    cv2.imshow('Frame Difference', binary_frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
