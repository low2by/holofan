# https://towardsdatascience.com/face-landmark-detection-with-cnns-tensorflow-cf4d191d2f0

import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import pandas as pd
from keras.callbacks import ModelCheckpoint
matplotlib.use('TkAgg')

x_train = np.load("face_landmarks_cleaned/x_train.npy") / 255
y_train = np.load("face_landmarks_cleaned/y_train.npy") / 96
# x_test = np.load("face_landmarks_cleaned/x_test.npy") / 255
# y_test = np.load("face_landmarks_cleaned/y_test.npy") / 96
photos = np.load("face_landmarks_cleaned/face_images.npz")['face_images']
landmarks = np.genfromtxt(
    "face_landmarks_cleaned/facial_keypoints.csv", dtype=float, delimiter=',', names=True)
landmarks = pd.DataFrame(landmarks)
indices = landmarks.index[~landmarks['left_eye_center_x'].isnull() & ~landmarks['left_eye_center_y'].isnull() & ~landmarks['right_eye_center_x'].isnull() & ~landmarks['right_eye_center_y'].isnull()]
landmarks = landmarks[~landmarks['left_eye_center_x'].isnull() & ~landmarks['left_eye_center_y'].isnull() & ~landmarks['right_eye_center_x'].isnull() & ~landmarks['right_eye_center_y'].isnull()]
landmarks = landmarks[['left_eye_center_x', 'left_eye_center_y', 'right_eye_center_x', 'right_eye_center_y']].values
landmarks = np.reshape(landmarks, (-1, 1, 1, 4))/96

photos = np.take(photos, indices, axis=2)
photos = photos.reshape((photos.shape[2],96,96,1))/255

# y_train = np.reshape(y_train, (-1, 1, 1, 30))
# y_test = np.reshape(y_test, (-1, 1, 1, 30))

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

    tf.keras.layers.Conv2D(4, kernel_size=(
        3, 3), strides=1, activation='relu'),
    tf.keras.layers.Conv2D(4, kernel_size=(
        3, 3), strides=1, activation='relu'),
    tf.keras.layers.Conv2D(4, kernel_size=(3, 3), strides=1),

]
model = tf.keras.Sequential(model_layers)
model.compile(loss=tf.keras.losses.mean_squared_error,
              optimizer=tf.keras.optimizers.Adam(lr=0.0001), metrics=['mse'])

mcp_save = ModelCheckpoint(
    'best weights.hdf5', save_best_only=True, monitor='val_loss', mode='min')
model.fit(
    x=photos,
    y=landmarks,
    validation_split=0.2,
    callbacks=[mcp_save],
    epochs=1,
    batch_size=50
)

fig = plt.figure(figsize=(50, 50))

for i in range(1, 6):
    sample_image = np.reshape(photos[i] * 255, (96, 96)).astype(np.uint8)
    pred = model.predict(photos)
    pred = pred.astype(np.int32)
    pred = np.reshape(pred[0, 0, 0], (2, 2))
    fig.add_subplot(1, 10, i)
    plt.imshow(sample_image.T, cmap='gray')
    plt.scatter(pred[:, 0], pred[:, 1], c='yellow')

plt.show()
