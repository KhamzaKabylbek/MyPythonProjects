# Import the necessary packages
import cv2

# Open the video capture device
cap = cv2.VideoCapture(1)

# Load the pre-trained face detection classifier
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Main loop to capture frames from the camera
while True:
    # Read a frame from the camera
    success, img = cap.read()

    # Detect faces in the frame
    faces = faceCascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=4)

    # If faces are detected, blur them
    for (x, y, w, h) in faces:
        ROI = img[y:y + h, x:x + w]
        blur = cv2.GaussianBlur(ROI, (91, 91), 0)
        img[y:y + h, x:x + w] = blur

    # If no faces are detected, display a message
    if len(faces) == 0:
        cv2.putText(img, 'No Face Found!', (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))

    # Display the frame with face blur or message
    cv2.imshow('Face Blur', img)

    # Check for the 'q' key press to exit the loop
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

# Release the video capture device
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
