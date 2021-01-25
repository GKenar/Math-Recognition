from layoutpass import do_layout_pass, Symbol
from math_r import parse_image
import cv2
import numpy as np

### Тут временная заглушка
data_expr_5 = [
    ['y', [279, 40, 50, 72]],
    ['+', [168, 33, 58, 57]],
    ['x', [47, 29, 75, 68]],
    ['2', [348, 12, 36, 39]]
]

data_expr_7 = [
    ['y', [279, 54, 50, 72]],
    ['+', [168, 47, 58, 57]],
    ['x', [47, 43, 75, 68]],
    ['2', [452, 7, 28, 40]],
    ['z', [339, 8, 40, 42]],
    ['+', [394, 7, 41, 45]],
    ['3', [123, 103, 29, 39]],
    ['1', [324, 106, 18, 42]],
    ['8', [384, 39, 20, 34]]
]

data_expr_8 = [
    ['(', [12, 127, 32, 97]],
    ['x', [49, 153, 49, 45]],
    ['+', [118, 153, 33, 42]],
    ['1', [181, 145, 33, 67]],
    [')', [215, 124, 32, 104]],
    ['(', [254, 101, 16, 43]],
    ['-', [272, 117, 16, 7]],
    ['1', [298, 105, 16, 40]],
    ['+', [325, 108, 23, 33]],
    ['3', [362, 104, 26, 39]],
    [')', [393, 98, 13, 45]],
    ['z', [407, 74, 30, 22]],
    ['-', [441, 180, 37, 7]],
    ['(', [504, 147, 24, 86]],
    ['-', [523, 181, 35, 7]],
    ['y', [570, 164, 39, 71]],
    [')', [613, 144, 19, 96]],
]

data_expr_9 = [
    ['(', [29, 31, 40, 184]],
    ['(', [64, 63, 30, 123]],
    ['(', [102, 87, 25, 81]],
    ['3', [143, 103, 31, 52]],
    ['-', [198, 124, 34, 7]],
    ['1', [249, 100, 20, 52]],
    [')', [293, 88, 20, 69]],
    ['+', [337, 103, 26, 40]],
    ['x', [374, 102, 43, 42]],
    [')', [404, 75, 25, 104]],
    ['2', [432, 64, 29, 39]],
    ['-', [464, 126, 17, 8]],
    ['y', [502, 107, 36, 66]],
    [')', [545, 53, 25, 150]],
    ['3', [573, 23, 24, 56]],
]

data_expr_10 = [
    ['fraction', [78, 108, 125, 10]],
    ['1', [90, 46, 26, 49]],
    ['5', [134, 131, 33, 53]],
    ['2', [135, 40, 46, 55]],
    ['-', [225, 105, 44, 10]],
    ['3', [296, 88, 35, 59]],
    ['fraction', [350, 107, 114, 9]],
    ['fraction', [383, 64, 52, 8]],
    ['1', [395, 24, 21, 38]],
    ['x', [398, 135, 41, 37]],
    ['2', [405, 74, 37, 26]],
]

data_expr_11 = [
    ['5', [97, 65, 68, 96]],
    ['+', [195, 75, 66, 60]],
    ['1', [280, 34, 48, 63]],
    ['fraction', [300, 99, 119, 8]],
    ['x', [343, 122, 50, 58]],
    ['2', [352, 34, 54, 57]],
]


###

# x = do_layout_pass(data_expr_11)
# print(x)


# !!! Сейчас это просто заглушка для работы demo версии
# Потом сделать lexical analysis, чтобы заменять - на дробь и т.д.
def semantic_correction(data):
    for symbol in data:
        if symbol[0] == '-':
            for symbol2 in data:
                if symbol != symbol2 and symbol[1][0] < symbol2[1][0] + symbol2[1][2] / 2 < symbol[1][0] + symbol[1][2]:
                    symbol[0] = 'fraction'
                    break


# Преобразует данные от нейронной сети в формат для layoutpass
def image_parser_data_converter(data):
    output = []
    symbols_imgs, symbols, symbols_bounds = data
    for i in range(len(symbols)):
        output.append([symbols[i], symbols_bounds[i]])

    return output


# Функция для перевода layoutpass в список
def layout_pass_to_string(layout: Symbol):
    list = []
    while layout is not None:
        if layout.above is not None:
            list.extend('(')
            list.extend(layout_pass_to_string(layout.above))
            list.extend(')')

        list.append(layout.symbol_label)

        if layout.super is not None:
            list.extend('^(')
            list.extend(layout_pass_to_string(layout.super))
            list.extend(')')
        if layout.subsc is not None:
            list.extend('_(')
            list.extend(layout_pass_to_string(layout.subsc))
            list.extend(')')
        if layout.below is not None:
            list.extend('(')
            list.extend(layout_pass_to_string(layout.below))
            list.extend(')')

        layout = layout.next
    return list


"""
result = parse_image('expr_examples/expression1010.png')
result = image_parser_data_converter(result)
semantic_correction(result)

x = do_layout_pass(result)
str = ''.join(layout_pass_to_string(x))
print(str)
"""
###########

mouse1_hold = False  # true if mouse1 is pressed
mouse2_hold = False  # true if mouse2 is pressed
current_former_x = 0
current_former_y = 0


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
        semantic_correction(result)

        x = do_layout_pass(result)
        str = ''.join(layout_pass_to_string(x))
        print(str)

cv2.destroyAllWindows()
