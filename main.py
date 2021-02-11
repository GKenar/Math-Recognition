from layoutpass import do_layout_pass, Symbol
from math_r import parse_image, build_model, load_weights
from transformpass import do_transform
from symbols import symbol_to_str
from solver import Solver
from symbols_tree_adapter import adapt_to_solver
import cv2
import numpy as np


# Преобразует данные от нейронной сети в формат для layoutpass
def image_parser_data_converter(data):
    output = []
    symbols_imgs, symbols, symbols_bounds = data
    for i in range(len(symbols)):
        output.append([symbols[i], symbols_bounds[i]])

    return output


# Функция для перевода layoutpass в список
def layout_pass_to_list(layout: Symbol):
    list = []
    while layout is not None:
        if layout.above is not None:
            list.extend('(')
            list.extend(layout_pass_to_list(layout.above))
            list.extend(')')

        list.append(symbol_to_str(layout.symbol_label))

        if layout.super is not None:
            list.extend('^(')
            list.extend(layout_pass_to_list(layout.super))
            list.extend(')')
        if layout.subsc is not None:
            list.extend('_(')
            list.extend(layout_pass_to_list(layout.subsc))
            list.extend(')')
        if layout.below is not None:
            list.extend('(')
            list.extend(layout_pass_to_list(layout.below))
            list.extend(')')

        layout = layout.next
    return list


# mouse callback function
def paint_draw(event, former_x, former_y, flags, param):
    global current_former_x, current_former_y, mouse1_hold, mouse2_hold
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse1_hold = True
    elif event == cv2.EVENT_RBUTTONDOWN:
        mouse2_hold = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if mouse1_hold:
            cv2.line(image, (current_former_x, current_former_y), (former_x, former_y), (0, 0, 0), 5)
        if mouse2_hold:
            cv2.line(image, (current_former_x, current_former_y), (former_x, former_y), (255, 255, 255), 35)
        current_former_x = former_x
        current_former_y = former_y
    elif event == cv2.EVENT_LBUTTONUP:
        mouse1_hold = False
    elif event == cv2.EVENT_RBUTTONUP:
        mouse2_hold = False

    return former_x, former_y


mouse1_hold = False  # true if mouse1 is pressed
mouse2_hold = False  # true if mouse2 is pressed
current_former_x = 0
current_former_y = 0

wolfram_keys_file = open("wolfram_cloud_keys.txt", "r")
wolfram_keys = wolfram_keys_file.read().split('\n')
consumer_key = wolfram_keys[0]
consumer_secret = wolfram_keys[1]

solver = Solver(consumer_key, consumer_secret)
solver.start_session()

build_model()
checkpoint_path = "training/cp.ckpt"
load_weights(checkpoint_path)

image = 255 * np.ones((500, 800, 3), dtype=np.uint8)
cv2.namedWindow('Math-r Test')
cv2.setMouseCallback('Math-r Test', paint_draw)
while True:
    cv2.imshow('Math-r Test', image)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # Escape KEY
        break
    elif k == ord('c'):
        image[:] = 255
    elif k == ord('r'):
        # cv2.imwrite("tmp_expression.jpg", image)

        result = parse_image(image)
        result = image_parser_data_converter(result)

        x = do_layout_pass(result)
        do_transform(x)
        str_simple = ''.join(layout_pass_to_list(x))
        str_adapted = adapt_to_solver(x)
        print(str_simple)
        print(str_adapted)
        print('result: ', solver.solve(str_adapted))

cv2.destroyAllWindows()
