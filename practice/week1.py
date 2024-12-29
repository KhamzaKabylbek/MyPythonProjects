import cv2

# Open the default camera (camera index 0)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if the frame is read correctly
    if not ret:
        print("Error: Couldn't read frame.")
        break

    # Flip the frame horizontally to create a mirror effect
    mirrored_frame = cv2.flip(frame, 1)

    # Add your name (Хамза) to the mirrored frame
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(mirrored_frame, 'Khamza', (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the mirrored frame
    cv2.imshow('Mirror Effect with Name', mirrored_frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
