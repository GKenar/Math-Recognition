__all__ = ["parse_image"]

import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Conv2D, Flatten, MaxPool2D, Dropout
import cv2
import matplotlib.pyplot as plt

symbols_dictionary = {
    0: '0',
    1: '1',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9',
    10: '+',
    11: '-',
}

def scale_contour(cnt, scale):
    # M = cv2.moments(cnt)
    (x, y, w, h) = cv2.boundingRect(cnt)
    cx = x  # int(M['m10']/M['m00'])
    cy = y  # int(M['m01']/M['m00'])

    cnt_norm = cnt - [cx, cy]
    cnt_scaled = cnt_norm * scale
    cnt_scaled = cnt_scaled + [cx, cy]
    cnt_scaled = cnt_scaled.astype(np.int32)

    return cnt_scaled


def parse_image(img):
    # Подгружаем картинку
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    img_erode = cv2.erode(thresh, np.ones((3, 3), np.uint8), iterations=1)

    # Достаём отдельные контуры из картинки
    contours, hierarchy = cv2.findContours(img_erode, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # CHAIN_APPROX_SIMPLE

    # print(hierarchy)

    # output = img.copy()

    # Формируем массив символов из полученных ранее контуров; сжимаем каждую картинку
    # символа до 28x28
    symbols = []
    symbols_bounds = []
    # cv2.contourArea(cnt) > 200 Посмотреть
    for idx, contour in enumerate(contours):
        if hierarchy[0][idx][3] == 0:
            (x, y, w, h) = cv2.boundingRect(contour)
            # cv2.rectangle(output, (x, y), (x + w, y + h), (70, 0, 0), 1)

            size_max = max(w, h)
            symbol_squared = 255 * np.ones((28, 28))
            aspect = 24.0 / size_max

            symbol = gray[y:y + h, x:x + w]
            # Сжимаем до 24px по бОльшей стороне
            symbol = cv2.resize(symbol, (int(np.ceil(w * aspect)), int(np.ceil(h * aspect))),
                                interpolation=cv2.INTER_LANCZOS4)  # Посмотреть другие interp
            symbol_size = symbol.shape

            if h > 300 or w > 300:  # Если символ слишком большой, то использовать не сжатое изображений, а сжатый контур
                test_img = 255 * np.ones((28, 28))
                contour_scaled = scale_contour(contour, aspect)
                cv2.drawContours(test_img, [contour_scaled], 0, (0, 0, 0), 2, offset=(-x, -y))
                # cv2.fillPoly(test_img, contour_scaled, (0, 0, 0), offset=(-x, -y))
                # test_img = cv2.resize(test_img, (500, 500),
                #                    interpolation=cv2.INTER_LANCZOS4)  # Посмотреть другие interp
                # cv2.imshow('11', test_img)
                # cv2.waitKey(0)
                symbol = test_img

            # Создаём квадратный символ 28x28 и по центру помещаем исходный 26x26
            shiftW = int(28.0 // 2 - symbol_size[1] // 2)
            shiftH = int(28.0 // 2 - symbol_size[0] // 2)
            for i in range(symbol_size[0]):
                for j in range(symbol_size[1]):
                    symbol_squared[i + shiftH, j + shiftW] = symbol[i, j]

            # cv2.imshow("squared!", symbol_squared)
            # cv2.waitKey(0)

            symbols.append(symbol_squared)
            symbols_bounds.append([x, y, w, h])

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
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.25))
    model.add(Dense(12, activation='softmax'))

    model.compile(loss="categorical_crossentropy",
                  optimizer="adam",
                  metrics=['accuracy'])

    model.load_weights(checkpoint_path)

    print("loaded.")

    predicted_symbol_labels = []
    for id in range(len(symbols)):
        # Нормализируем
        symbols[id] = symbols[id] / 255.0
        symbols[id] = 1 - symbols[id]

        id_symbol_predicted = np.argmax(model.predict(np.array([symbols[id].reshape(28, 28, 1)])))
        symbol_predicted = symbols_dictionary[id_symbol_predicted]

        predicted_symbol_labels.append(symbol_predicted)
        # print(result)
        # print(np.argmax(result, axis=1))
        # symbols[id] = cv2.resize(symbols[id], (50, 50))
        # cv2.imshow(str(np.argmax(result, axis=1)), symbols[id])
        # cv2.resizeWindow(str(np.argmax(result, axis=1)), 200, 70)  # resize the window
        # print(symbols_bounds[id])
        # cv2.waitKey(0)

    # symbols_bounds.sort(key=lambda s: s[0])
    # print(symbols_bounds)
    return symbols, predicted_symbol_labels, symbols_bounds


if __name__ == "__main__":
    result = parse_image(cv2.imread('expr_examples/expression4444.png'))

    fig = plt.figure(figsize=(8, 8))
    for i in range(len(result[0])):
        plt.subplot(int(np.ceil(len(result[0]) / 10)), 10, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(result[0][i], cmap=plt.cm.binary)
        plt.xlabel(str(result[1][i]))
    plt.show()
