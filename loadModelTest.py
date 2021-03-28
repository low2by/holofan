import tensorflow as tf
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

x_test = np.load("face_landmarks_cleaned/x_test.npy")/255

model_layers = [

    tf.keras.layers.Conv2D(256, input_shape=(96, 96, 1),
                           kernel_size=(3, 3), strides=2, activation='relu'),
    tf.keras.layers.Conv2D(256, kernel_size=(
        3, 3), strides=2, activation='relu'),
    tf.keras.layers.BatchNormalization(),

    tf.keras.layers.Conv2D(128, kernel_size=(
        3, 3), strides=1, activation='relu'),
    tf.keras.layers.Conv2D(128, kernel_size=(
        3, 3), strides=1, activation='relu'),
    tf.keras.layers.BatchNormalization(),

    tf.keras.layers.Conv2D(128, kernel_size=(
        3, 3), strides=1, activation='relu'),
    tf.keras.layers.Conv2D(128, kernel_size=(
        3, 3), strides=1, activation='relu'),
    tf.keras.layers.BatchNormalization(),

    tf.keras.layers.Conv2D(64, kernel_size=(
        3, 3), strides=1, activation='relu'),
    tf.keras.layers.Conv2D(64, kernel_size=(
        3, 3), strides=1, activation='relu'),
    tf.keras.layers.BatchNormalization(),

    tf.keras.layers.Conv2D(32, kernel_size=(
        3, 3), strides=1, activation='relu'),
    tf.keras.layers.Conv2D(32, kernel_size=(
        3, 3), strides=1, activation='relu'),
    tf.keras.layers.BatchNormalization(),

    tf.keras.layers.Conv2D(30, kernel_size=(
        3, 3), strides=1, activation='relu'),
    tf.keras.layers.Conv2D(30, kernel_size=(
        3, 3), strides=1, activation='relu'),
    tf.keras.layers.Conv2D(30, kernel_size=(3, 3), strides=1),

]
model = tf.keras.Sequential(model_layers)
model.compile(loss=tf.keras.losses.mean_squared_error,
              optimizer=tf.keras.optimizers.Adam(lr=0.0001), metrics=['mse'])

model.load_weights('best_weights_3.26.2021.hdf5')

# x_train = np.load( "face_landmarks_cleaned/x_train.npy" ) / 255
# print(x_train)
i = 100

im1 = np.array(Image.open('face_landmarks_cleaned/me3.jpg').convert('L')).reshape((1, 96, 96, 1))/255
im1 = im1.T

im2 = x_test[i:i+1]

pred1 = model.predict(im1) * 96
pred1 = pred1.astype(np.int32)
pred1 = np.reshape(pred1[0, 0, 0], (15, 2))

pred2 = model.predict(im2) * 96
pred2 = pred2.astype(np.int32)
pred2 = np.reshape(pred2[0, 0, 0], (15, 2))

fig = plt.figure(figsize=(50, 50))
fig.add_subplot(1, 2, 1)
plt.imshow(im1.reshape((96,96)).T.astype( np.float )*255 , cmap='gray' )
plt.scatter(pred1[:, 0], pred1[:, 1], c='yellow')

fig.add_subplot(1, 2, 2)
plt.imshow(im2.reshape((96,96)).T.astype( np.float )*255 , cmap='gray' )
plt.scatter(pred2[:, 0], pred2[:, 1], c='yellow')

plt.show()
