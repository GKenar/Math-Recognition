from main import math_recognition_image_by_path, prepare_network
from symbols_tree_adapter import adapt_to_solver
from os import path
import numpy as np

tests_data = [
    {'id': 1, 'answer': '1234567890', 'expression_path': 'test_images/1.png'},
    {'id': 2, 'answer': '3-4+8-0', 'expression_path': 'test_images/2.png'},
    {'id': 3, 'answer': '(8)/(2)', 'expression_path': 'test_images/3.png'},
    {'id': 4, 'answer': '(1)/(2)+(3)/(4)-(5)/(6)', 'expression_path': 'test_images/4.png'},
    {'id': 5, 'answer': '(((9)/(4))/(2))/(10)', 'expression_path': 'test_images/5.png'},
    {'id': 6, 'answer': '2^(9)-3^(12-4)+5^(6-4)', 'expression_path': 'test_images/6.png'},
    {'id': 7, 'answer': '(3^(2))/(4^(3))', 'expression_path': 'test_images/7.png'},
    {'id': 8, 'answer': '2^(3^(4^(5)))', 'expression_path': 'test_images/8.png'},
    {'id': 9, 'answer': '(12-4)', 'expression_path': 'test_images/9.png'},
    {'id': 10, 'answer': '((12-4)^(2)-7)^(2)', 'expression_path': 'test_images/10.png'},
    {'id': 11, 'answer': '(((1-4)^(2)+3)^(2))^(2)', 'expression_path': 'test_images/11.png'},
    {'id': 12, 'answer': '((-3)/(12))^(20)', 'expression_path': 'test_images/12.png'},
    {'id': 13, 'answer': '10^((-3)^(2)+4)', 'expression_path': 'test_images/13.png'},
    {'id': 14, 'answer': '(15^((1)/(4)))-8', 'expression_path': 'test_images/14.png'},
    {'id': 15, 'answer': '(305+(-5))^((-3))', 'expression_path': 'test_images/15.png'},
    {'id': 16, 'answer': '1.000007', 'expression_path': 'test_images/16.png'},
    {'id': 17, 'answer': '0.5+0.05', 'expression_path': 'test_images/17.png'},
    {'id': 18, 'answer': '(0.01)/(100)', 'expression_path': 'test_images/18.png'},
    {'id': 19, 'answer': '10.1*10', 'expression_path': 'test_images/19.png'},
    {'id': 20, 'answer': '0.1^(0.01)', 'expression_path': 'test_images/20.png'},
    {'id': 21, 'answer': '(2+2*2)/(1*2*3.4)', 'expression_path': 'test_images/21.png'},
    {'id': 22, 'answer': '11111111', 'expression_path': 'test_images/22.png'},
    {'id': 23, 'answer': '2222222', 'expression_path': 'test_images/23.png'},
    {'id': 24, 'answer': '00000000', 'expression_path': 'test_images/24.png'},
    {'id': 25, 'answer': '33333333', 'expression_path': 'test_images/25.png'},
    {'id': 26, 'answer': '44444444', 'expression_path': 'test_images/26.png'},
    {'id': 27, 'answer': '5555555', 'expression_path': 'test_images/27.png'},
    {'id': 28, 'answer': '66666666', 'expression_path': 'test_images/28.png'},
    {'id': 29, 'answer': '7777777', 'expression_path': 'test_images/29.png'},
    {'id': 30, 'answer': '88888888', 'expression_path': 'test_images/30.png'},
    {'id': 31, 'answer': '99999999', 'expression_path': 'test_images/31.png'},
    {'id': 32, 'answer': '**********', 'expression_path': 'test_images/32.png'},
    {'id': 33, 'answer': '(((((((((', 'expression_path': 'test_images/33.png'},
    {'id': 34, 'answer': '))))))))', 'expression_path': 'test_images/34.png'},
    {'id': 35, 'answer': '+++++++', 'expression_path': 'test_images/35.png'},
    {'id': 36, 'answer': '--------', 'expression_path': 'test_images/36.png'},
    {'id': 37, 'answer': 'xxxxxxx', 'expression_path': 'test_images/37.png'},
    {'id': 38, 'answer': 'ExportString[Solve[x^(2)+7*x==10], "Text"]', 'expression_path': 'test_images/38.png'},
    {'id': 39, 'answer': 'ExportString[Solve[============], "Text"]', 'expression_path': 'test_images/39.png'},
]

if __name__ == "__main__":
    prepare_network()

    for test in tests_data:
        math_r_answer = adapt_to_solver(math_recognition_image_by_path(test['expression_path']))
        if math_r_answer == test['answer']:
            print('id', test['id'], 'correct.')
        else:
            print('id: ', test['id'], 'wrong. ', 'expect: ', test['answer'], ' math-r: ', math_r_answer)

