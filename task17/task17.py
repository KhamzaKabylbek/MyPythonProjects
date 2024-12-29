import cv2
BackgroundSubtraction = cv2.createBackgroundSubtractorMOG2()
capture = cv2.VideoCapture(0)
while True:
    ret, frame = capture.read()
    if not ret:
        break
    fgMask = BackgroundSubtraction.apply(frame)

    cv2.imshow('Frame', frame)
    cv2.imshow('FG Mask', fgMask)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
capture.release()
cv2.destroyAllWindows()
