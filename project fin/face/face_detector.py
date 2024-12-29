import cv2
import numpy as np
modelFile = "res10_300x300_ssd_iter_140000.caffemodel"
configFile = "deploy.prototxt"
net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
cap = cv2.VideoCapture(1)
while True:
    _,img = cap.read()
    h, w = img.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0,(300, 300), (104.0, 117.0, 123.0))
    net.setInput(blob)
    faces = net.forward()
    for i in range(faces.shape[2]):
        confidence = faces[0, 0, i, 2]
        if confidence > 0.5:
            box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x, y, x1, y1) = box.astype("int")
            cv2.rectangle(img, (x, y), (x1, y1), (128,128,128), 2)
    cv2.imshow('Video',img)
    if cv2.waitKey(1) & 0xff==ord('q'):
        break








#
# import cv2
# import numpy as np
#
# # Load face detection model
# modelFile = "res10_300x300_ssd_iter_140000.caffemodel"
# configFile = "deploy.prototxt"
# net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
#
# # Load age and gender prediction models
# GENDER_MODEL = 'deploy_gender.prototxt'
# GENDER_PROTO = 'gender_net.caffemodel'
# AGE_MODEL = 'deploy_age.prototxt'
# AGE_PROTO = 'age_net.caffemodel'
# gender_net = cv2.dnn.readNetFromCaffe(GENDER_MODEL, GENDER_PROTO)
# age_net = cv2.dnn.readNetFromCaffe(AGE_MODEL, AGE_PROTO)
#
# # Function to predict gender
# def get_gender_predictions(face_img):
#     blob = cv2.dnn.blobFromImage(
#         image=face_img, scalefactor=1.0, size=(227, 227),
#         mean=(78.4263377603, 87.7689143744, 114.895847746), swapRB=False, crop=False
#     )
#     gender_net.setInput(blob)
#     return gender_net.forward()
#
# # Function to predict age
# def get_age_predictions(face_img):
#     blob = cv2.dnn.blobFromImage(
#         image=face_img, scalefactor=1.0, size=(227, 227),
#         mean=(78.4263377603, 87.7689143744, 114.895847746), swapRB=False
#     )
#     age_net.setInput(blob)
#     return age_net.forward()
#
# cap = cv2.VideoCapture(1)
# while True:
#     _,img = cap.read()
#     h, w = img.shape[:2]
#     blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0))
#     net.setInput(blob)
#     faces = net.forward()
#     for i in range(faces.shape[2]):
#         confidence = faces[0, 0, i, 2]
#         if confidence > 0.5:
#             box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
#             (x, y, x1, y1) = box.astype("int")
#             cv2.rectangle(img, (x, y), (x1, y1), (128,128,128), 2)
#
#             # Extract face from the image
#             face_img = img[y:y1, x:x1]
#
#             # Predict gender and age
#             gender_preds = get_gender_predictions(face_img)
#             age_preds = get_age_predictions(face_img)
#
#             # Find the indices with the highest prediction scores
#             gender_idx = gender_preds[0].argmax()
#             gender = 'Male' if gender_idx == 1 else 'Female'
#             gender_confidence = gender_preds[0][gender_idx]
#
#             age_idx = age_preds[0].argmax()
#             age = age_idx * 5 + 5  # Assuming age intervals of 5 years
#             age_confidence = age_preds[0][age_idx]
#
#             # Display predicted gender and age
#             cv2.putText(img, f"Gender: {gender} ({gender_confidence:.2f})", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
#             cv2.putText(img, f"Age: {age} ({age_confidence:.2f})", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
#
#     cv2.imshow('Video',img)
#     if cv2.waitKey(1) & 0xff==ord('q'):
#         break
#
# cv2.destroyAllWindows()
#

# import cv2
# import numpy as np
# from keras.models import model_from_json
# import streamlit as st
# import tempfile

# # Paths for the face detection model
# FACE_PROTO = "deploy.prototxt.txt"
# FACE_MODEL = "res10_300x300_ssd_iter_140000_fp16.caffemodel"
#
# # Paths for gender and age prediction models
# GENDER_MODEL = 'deploy_gender.prototxt'
# GENDER_PROTO = 'gender_net.caffemodel'
# AGE_MODEL = 'deploy_age.prototxt'
# AGE_PROTO = 'age_net.caffemodel'
#
# # Paths for the emotion prediction model
# EMOTION_MODEL_JSON = 'emotion_model.json'
# EMOTION_MODEL_WEIGHTS = 'emotion_model_weights.h5'
#
# # Define gender labels
# GENDER_LIST = ['Male', 'Female']
# # Define age labels
# AGE_INTERVALS = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)',
#                  '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
# # Define emotion labels
# EMOTION_LABELS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
#
# # Load the face detection model
# face_net = cv2.dnn.readNetFromCaffe(FACE_PROTO, FACE_MODEL)
# # Load the gender and age prediction models
# gender_net = cv2.dnn.readNetFromCaffe(GENDER_MODEL, GENDER_PROTO)
# age_net = cv2.dnn.readNetFromCaffe(AGE_MODEL, AGE_PROTO)
# # Load the emotion prediction model
# with open(EMOTION_MODEL_JSON, 'r') as json_file:
#     emotion_model_json = json_file.read()
# emotion_model = model_from_json(emotion_model_json)
# emotion_model.load_weights(EMOTION_MODEL_WEIGHTS)
#
# # Function to predict gender
# def get_gender_predictions(face_img):
#     blob = cv2.dnn.blobFromImage(
#         image=face_img, scalefactor=1.0, size=(227, 227),
#         mean=(78.4263377603, 87.7689143744, 114.895847746), swapRB=False, crop=False
#     )
#     gender_net.setInput(blob)
#     return gender_net.forward()
#
# # Function to predict age
# def get_age_predictions(face_img):
#     blob = cv2.dnn.blobFromImage(
#         image=face_img, scalefactor=1.0, size=(227, 227),
#         mean=(78.4263377603, 87.7689143744, 114.895847746), swapRB=False
#     )
#     age_net.setInput(blob)
#     return age_net.forward()
#
# # Function to predict emotion
# def get_emotion_predictions(face_img):
#     face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
#     face_img = cv2.resize(face_img, (48, 48))
#     face_img = np.expand_dims(face_img, axis=0)
#     face_img = face_img / 255.0  # Normalize the image
#     emotion_preds = emotion_model.predict(face_img)
#     return emotion_preds
#
# # Function to detect faces
# def get_faces(frame, confidence_threshold=0.5):
#     blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104, 177.0, 123.0))
#     face_net.setInput(blob)
#     output = np.squeeze(face_net.forward())
#     faces = []
#     for i in range(output.shape[0]):
#         confidence = output[i, 2]
#         if confidence > confidence_threshold:
#             box = output[i, 3:7] * np.array([frame.shape[1], frame.shape[0],
#                                               frame.shape[1], frame.shape[0]])
#             start_x, start_y, end_x, end_y = box.astype(np.int)
#             start_x, start_y = max(0, start_x), max(0, start_y)
#             end_x, end_y = min(frame.shape[1], end_x), min(frame.shape[0], end_y)
#             faces.append((start_x, start_y, end_x, end_y))
#     return faces
#
# # Function to process an image
# def process_image(image):
#     img = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_COLOR)
#     faces = get_faces(img)
#     for (start_x, start_y, end_x, end_y) in faces:
#         face_img = img[start_y:end_y, start_x:end_x]
#         # Predict gender, age, and emotion
#         gender_preds = get_gender_predictions(face_img)
#         age_preds = get_age_predictions(face_img)
#         emotion_preds = get_emotion_predictions(face_img)
#         # Extract gender, age, and emotion labels
#         gender_idx = gender_preds[0].argmax()
#         gender = GENDER_LIST[gender_idx]
#         age_idx = age_preds[0].argmax()
#         age = AGE_INTERVALS[age_idx]
#         emotion_idx = emotion_preds[0].argmax()
#         emotion = EMOTION_LABELS[emotion_idx]
#         # Draw bounding box and labels
#         cv2.rectangle(img, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
#         cv2.putText(img, f"Gender: {gender}", (start_x, start_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
#         cv2.putText(img, f"Age: {age}", (start_x, start_y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
#         cv2.putText(img, f"Emotion: {emotion}", (start_x, start_y - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
#     return img
#
# # Streamlit app
# def main():
#     st.title("Age, Gender, and Emotion Prediction App")
#     st.write("Upload an image to predict age, gender, and emotion.")
#     uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
#     if uploaded_image is not None:
#         img = process_image(uploaded_image)
#         st.image(img, caption='Processed Image', use_column_width=True)
#
# if __name__ == "__main__":
#     main()
