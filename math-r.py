import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import Dense, Conv2D, Flatten, MaxPool2D
import matplotlib.pyplot as plt
import skimage.data as data
import skimage.segmentation as seg
import skimage.filters as filters
import skimage.draw as draw
import skimage.color as color
from tensorflow.keras.utils import to_categorical
import cv2

# Подгружаем картинку
image_path = "expression2.png"
img = cv2.imread(image_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
img_erode = cv2.erode(thresh, np.ones((3, 3), np.uint8), iterations=1)

# Достаём отдельные контуры из картинки
contours, hierarchy = cv2.findContours(img_erode, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# print(hierarchy)

output = img.copy()

# Формируем массив символов из полученных ранее контуров; сжимаем каждую картинку
# символа до 28x28
symbols = []
for idx, contour in enumerate(contours):
    if hierarchy[0][idx][3] == 0:
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(output, (x, y), (x + w, y + h), (70, 0, 0), 1)

        size_max = max(w, h)
        symbol_squared = 255 * np.ones((28, 28))
        aspect = 24.0 / size_max

        symbol = gray[y:y + h, x:x + w]
        # Сжимаем до 24px по бОльшей стороне
        symbol = cv2.resize(symbol, (int(w * aspect), int(h * aspect)))
        symbol_size = symbol.shape

        # Создаём квадратный символ 28x28 и по центру помещаем исходный 26x26
        shiftW = int(28.0 // 2 - symbol_size[1] // 2)
        shiftH = int(28.0 // 2 - symbol_size[0] // 2)
        for i in range(symbol_size[0]):
            for j in range(symbol_size[1]):
                symbol_squared[i + shiftH, j + shiftW] = symbol[i, j]

        # cv2.imshow("squared!", symbol_squared)
        # cv2.waitKey(0)

        symbols.append(symbol_squared)

# cv2.imshow("Output", output)
# symbols.sort(key=lambda x: x[0])

# for id, s in enumerate(symbols):
#    cv2.imshow(str(id), s)


checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Создаем коллбек сохраняющий веса модели
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)
model = keras.Sequential()
model.add(Conv2D(32, kernel_size=3, activation='relu', input_shape=(28, 28, 1)))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Conv2D(64, kernel_size=3, activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Conv2D(64, kernel_size=3, activation='relu'))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(10, activation='softmax'))


model.compile(loss="categorical_crossentropy",
              optimizer="adam",
              metrics=['accuracy'])

model.load_weights(checkpoint_path)

print("loaded.")

for id in range(len(symbols)):
    # Нормализируем
    symbols[id] = symbols[id] / 255.0
    symbols[id] = 1 - symbols[id]

    result = model.predict(np.array([symbols[id].reshape(28, 28, 1)]))
    print(result)
    print(np.argmax(result, axis=1))
    cv2.imshow(str(np.argmax(result, axis=1)), symbols[id])
    cv2.resizeWindow(str(np.argmax(result, axis=1)), 200, 30)  # resize the window

    cv2.waitKey(0)

