
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import GlobalAveragePooling2D,Dense, BatchNormalization, Dropout, Flatten, Conv2D, MaxPooling2D,Activation
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline
import numpy as np
import pandas as pd
import random
import os
import warnings
warnings.filterwarnings("ignore")

test= "/content/evaluation/"
val = "/content/validation/"
train = "/content/training/"

BATCH_SIZE = 16
seeds = 41
img_shape = (250,250)



from tensorflow.keras.applications.inception_resnet_v2 import InceptionResNetV2, preprocess_input

data_generator = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        shear_range=0.2,
        zoom_range=0.2,
        validation_split=0.25,
        rotation_range=45,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')

val_data_generator = ImageDataGenerator(preprocessing_function=preprocess_input,validation_split=0.25)

test_generator = ImageDataGenerator(preprocessing_function=preprocess_input)

train_generator = data_generator.flow_from_directory(train, target_size=img_shape, shuffle=True, seed=seeds,
                                                     class_mode='categorical', batch_size=BATCH_SIZE, subset="training")

validation_generator = val_data_generator.flow_from_directory(train, target_size=img_shape, shuffle=False, seed=seeds,
                                                     class_mode='categorical', batch_size=BATCH_SIZE, subset="validation")


test_generator = test_generator.flow_from_directory(test, target_size=img_shape, shuffle=False, seed=seeds,
                                                     class_mode='categorical', batch_size=BATCH_SIZE)

nb_train_samples = train_generator.samples
nb_validation_samples = validation_generator.samples
nb_test_samples = test_generator.samples
classes = list(train_generator.class_indices.keys())
print('Classes:- '+str(classes))
total_classes  = len(classes)
print('Number of Classes :- '+str(total_classes))

plt.figure(figsize=(10,10))
for i in range(9):
    #gera subfigures
    plt.subplot(330 + 1 + i)
    batch = train_generator.next()[0]*255
    image = batch[0].astype('uint8')
    plt.imshow(image)
    plt.axis('off')
plt.show()

import random

random_images = []
for _ in range(4):
    batch = next(train_generator)
    image = batch[0][0]
    random_images.append(image)
plt.figure(figsize=(10, 10))
for i in range(4):
    plt.subplot(2, 2, i+1)
    plt.imshow(random_images[i])
    plt.axis('off')
plt.show()

base_model = InceptionResNetV2(weights='imagenet', include_top=False, input_shape=(img_shape[0], img_shape[1], 3))

x = base_model.output
x = Flatten()(x)
x = Dense(100, activation='relu')(x)
predictions = Dense(total_classes, activation='softmax', kernel_initializer='random_uniform')(x)

model = Model(inputs=base_model.input, outputs=predictions)

for layer in base_model.layers:
    layer.trainable=False

optimizer = Adam()
model.compile(optimizer=optimizer,loss='categorical_crossentropy',metrics=['accuracy'])

epochs = 15

callbacks_list = [
    keras.callbacks.ModelCheckpoint(
        filepath='model.h5',
        monitor='val_loss', save_best_only=True, verbose=1),
    keras.callbacks.EarlyStopping(monitor='val_loss', patience=6, verbose=1)
]

history = model.fit(
    train_generator,
    steps_per_epoch=nb_train_samples // BATCH_SIZE,
    epochs=epochs,
    callbacks=callbacks_list,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // BATCH_SIZE,
    verbose=1
)

history_dict = history.history
loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']
epochs_x = range(1, len(loss_values) + 1)
plt.figure(figsize=(10,10))
plt.subplot(2,1,1)
plt.plot(epochs_x, loss_values, 'bo', label='Training loss')
plt.plot(epochs_x, val_loss_values, 'b', label='Validation loss')
plt.title('Loss and Accuracy of Training and Validation')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.subplot(2,1,2)
acc_values = history_dict['accuracy']
val_acc_values = history_dict['val_accuracy']
plt.plot(epochs_x, acc_values, 'bo', label='Training acc')
plt.plot(epochs_x, val_acc_values, 'r', label='Validation acc')
plt.xlabel('Epochs')
plt.ylabel('Acc')
plt.legend()
plt.show()

from tensorflow.keras.models import load_model
val_accuracy = list()
val_loss = list()
test_loss= list()
test_accuracy = list()
model = load_model('/content/model.h5')
score = model.evaluate_generator(validation_generator)
val_loss.append(score[0])
val_accuracy.append(score[1])
print('Validation loss:', score[0])
print('Validation accuracy:', score[1])

score = model.evaluate_generator(test_generator)

print('Test loss:', score[0])
print('Test accuracy:', score[1])

test_loss.append(score[0])
test_accuracy.append(score[1])

from tensorflow.keras.applications.inception_resnet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt

img_path = '/content/validation/Dairy product/10.jpg'
img = image.load_img(img_path, target_size=img_shape)
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

plt.imshow(img)
plt.axis('off')
plt.show()

predictions = model.predict(x)
class_index = np.argmax(predictions)
predicted_class = classes[class_index]
print('Predicted class:', predicted_class)

