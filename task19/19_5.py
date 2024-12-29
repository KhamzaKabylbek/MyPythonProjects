import cv2
import pandas as pd

def detect_faces(img, faces_df):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for i, (x, y, w, h) in enumerate(faces):
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face_img = img[y:y + h, x:x + w]

        # Detect gender
        # gender_model.predict(face_img)  # You need to implement this using a pre-trained model

        # Detect emotion
        # emotion_model.predict(face_img)  # You need to implement this using a pre-trained model

        # Estimate approximate age
        # age = estimate_age(face_img)  # You need to implement this

        cv2.imshow(f'Face {i + 1}', face_img)
        faces_df = faces_df._append({'Face': i + 1, 'X': x, 'Y': y, 'Width': w, 'Height': h,
                                    'Gender': 'Unknown', 'Emotion': 'Unknown', 'Age': 'Unknown'}, ignore_index=True)

    return img, faces_df

# Initialize VideoCapture
cap = cv2.VideoCapture('q.mp4')

# Initialize DataFrame for storing face information
faces_df = pd.DataFrame(columns=['Face', 'X', 'Y', 'Width', 'Height', 'Gender', 'Emotion', 'Age'])

# Main loop for video processing
while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame_with_faces, faces_df = detect_faces(frame, faces_df)

    cv2.imshow('Video', frame_with_faces)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Save face information to CSV
faces_df.to_csv('faces_info.csv', index=False)

# Release VideoCapture and destroy windows
cap.release()
cv2.destroyAllWindows()
