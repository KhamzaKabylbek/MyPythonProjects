# # Import Libraries
# import cv2
# import numpy as np
# from keras.models import model_from_json
# import streamlit as st
# import tempfile
#
# # Paths for the face detection model
# FACE_PROTO = "deploy.prototxt.txt"
# FACE_MODEL = "res10_300x300_ssd_iter_140000.caffemodel"
#
# # Load the face detection model
# face_net = cv2.dnn.readNetFromCaffe(FACE_PROTO, FACE_MODEL)
#
# # Paths for gender and age prediction models
# GENDER_MODEL = 'deploy_gender.prototxt'
# GENDER_PROTO = 'gender_net.caffemodel'
# AGE_MODEL = 'deploy_age.prototxt'
# AGE_PROTO = 'age_net.caffemodel'
#
# # Load the gender and age prediction models
# gender_net = cv2.dnn.readNetFromCaffe(GENDER_MODEL, GENDER_PROTO)
# age_net = cv2.dnn.readNetFromCaffe(AGE_MODEL, AGE_PROTO)
#
# # Paths for the emotion prediction model
# EMOTION_MODEL_JSON = 'emotion_model.json'
# EMOTION_MODEL_WEIGHTS = 'emotion_model_weights.h5'
#
# # Load the emotion prediction model
# with open(EMOTION_MODEL_JSON, 'r') as json_file:
#     emotion_model_json = json_file.read()
# emotion_model = model_from_json(emotion_model_json)
# emotion_model.load_weights(EMOTION_MODEL_WEIGHTS)
#
# # Define gender labels
# GENDER_LIST = ['Male', 'Female']
#
# # Define age labels
# AGE_INTERVALS = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)',
#                  '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
#
# # Define emotion labels
# emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise',
#                   'Neutral']
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
#             box = output[i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
#             start_x, start_y, end_x, end_y = box.astype(np.int)
#             start_x, start_y, end_x, end_y = start_x - 10, start_y - 10, end_x + 10, end_y + 10
#             start_x = 0 if start_x < 0 else start_x
#             start_y = 0 if start_y < 0 else start_y
#             end_x = 0 if end_x < 0 else end_x
#             end_y = 0 if end_y < 0 else end_y
#             faces.append((start_x, start_y, end_x, end_y))
#     return faces
#
# # Function to predict gender
# def get_gender_predictions(face_img):
#     blob = cv2.dnn.blobFromImage(
#         image=face_img, scalefactor=1.0, size=(227, 227),
#         mean=MODEL_MEAN_VALUES, swapRB=False, crop=False
#     )
#     gender_net.setInput(blob)
#     return gender_net.forward()
#
# # Function to predict age
# def get_age_predictions(face_img):
#     blob = cv2.dnn.blobFromImage(
#         image=face_img, scalefactor=1.0, size=(227, 227),
#         mean=MODEL_MEAN_VALUES, swapRB=False
#     )
#     age_net.setInput(blob)
#     return age_net.forward()
#
# # Function to predict emotion
# def get_emotion_predictions(face_img):
#     face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
#     face_img = cv2.resize(face_img, (48, 48))
#     face_img = np.expand_dims(face_img, axis=0)
#     face_img = face_img / 255.0
#     emotion_preds = emotion_model.predict(face_img)
#     return emotion_preds
#
# # Function to load image and predict
# def load_image_and_predict(uploaded_image):
#     with tempfile.NamedTemporaryFile(delete=False) as temp_image:
#         temp_image.write(uploaded_image.read())
#
#     predict_age_gender_and_emotion(temp_image.name)
#
# # Function for main application
# def main():
#     st.write('<h1 class="title">Age, Gender, and Emotion Detection App</h1>', unsafe_allow_html=True)
#     st.write("")
#     st.write("")
#     st.write("The 'Age, Gender, and Emotion Detection App' is a powerful AI-driven tool that instantly analyzes human faces to determine age, gender, and emotional states. This versatile application finds applications in market research, user experience enhancement, and more, providing valuable insights through real-time facial analysis.")
#     st.sidebar.title("Options")
#
#     # Add a choice in the sidebar to select the mode
#     app_mode = st.sidebar.selectbox(
#         "Choose the detection mode",
#         ["Choose an option...", "Webcam", "Image"],
#     )
#
#     if app_mode == "Webcam":
#         age_gender_emotion.main()
#     elif app_mode == "Image":
#         uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "bmp", "gif", "tiff", "tif"])
#         if uploaded_image is not None:
#             img_det.load_image_and_predict(uploaded_image)
#
# if __name__ == "__main__":
#     main()
