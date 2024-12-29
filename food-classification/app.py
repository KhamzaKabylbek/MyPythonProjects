import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.inception_resnet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image
Saved_model = load_model('model.h5')
Classes = ['Bread', 'Dairy Product', 'Dessert', 'Egg', 'Fried Food', 'Meat', 'Noodles-Pasta', 'Rice', 'Seafood', 'Soup', 'Vegetable-Fruit']
def preprocess_image(image_path, image_shape):
    img = image.load_img(image_path, target_size=image_shape)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x
def predict_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((250, 250))
        img = ImageTk.PhotoImage(img)
        image_label.configure(image=img)
        image_label.image = img  
        processed_img = preprocess_image(file_path, (250, 250))
        predictions = Saved_model.predict(processed_img)
        class_index = np.argmax(predictions)
        predicted_class = Classes[class_index]
        predicted_label.configure(text=f"Predicted class: {predicted_class}")
window = tk.Tk()
window.title("Food Classification App By PythonGeeks")
window.geometry("600x400")
upload_button = tk.Button(window, text="Upload Image", command=predict_image, bg="blue", fg="white")
def on_enter(e):
    upload_button.configure(bg="lightblue")
def on_leave(e):
    upload_button.configure(bg="blue")
upload_button.bind("<Enter>", on_enter)
upload_button.bind("<Leave>", on_leave)
upload_button.pack(pady=10)
image_label = tk.Label(window)
image_label.pack()
predicted_label = tk.Label(window, text="")
predicted_label.pack(pady=10)
window.mainloop()
