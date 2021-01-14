__all__ = ["Symbol", "do_layout_pass"]

from enum import Enum
from collections import namedtuple
import math

Bounds = namedtuple('Bounds', ['left', 'top', 'right', 'bottom'])  # Можно переделать на какой-то другой тип (dataclass mb?)
Regions = namedtuple('Regions', ['next', 'super', 'subsc', 'above', 'below'])


class SymbolClass(Enum):
    NON_SCRIPTED = 1
    PLAIN_CENTERED = 2
    PLAIN_DESCENDER = 3
    PLAIN_ASCENDER = 4


# Пока для классификации буду использовать словарь, потом может что-то другое придумаю
classes_dictionary = {
    'x': SymbolClass.PLAIN_CENTERED,
    'y': SymbolClass.PLAIN_DESCENDER,
    '+': SymbolClass.NON_SCRIPTED,
    '2': SymbolClass.PLAIN_ASCENDER
}

# Глобальные переменные
centroid_ratio = 0.5
threshold_ratio = 0.3  # t <= c; t, c iz [0, 0.5]
###


class Symbol:
    """Класс, описывающий один символ из математического выражения"""
    __symbol_label = None
    __symbol_class = None  # SymbolClass.NON_SCRIPTED
    __next = None
    __super = None
    __subsc = None
    __above = None
    __below = None
    # И другие ещё ...
    # Везде будем использовать абсолютные координаты
    __bounds = None  # Bounds(0, 0, 0, 0)
    __centroid = None  # [x, y]
    __regions = None  # Regions(0, 0, 0, 0, 0)

    def __init__(self, label):
        self.__symbol_label = label

    @property
    def symbol_class(self):
        return self.__symbol_class

    @symbol_class.setter
    def symbol_class(self, sym_class):  # При изменении класса нужно также менять regions и т.д.
        self.__symbol_class = sym_class

    @property
    def bounds(self):
        return self.__bounds

    @bounds.setter
    def bounds(self, b):
        self.__bounds = b
        # self.__centroid = [(b[2] + b[0]) / 2, (b[3] + b[1]) / 2]

    @property
    def regions(self):
        return self.__regions

    @regions.setter
    def regions(self, b):
        self.__regions = b

    @property
    def centroid(self):
        return self.__centroid

    @centroid.setter
    def centroid(self, c):
        self.__centroid = c

    @property
    def symbol_label(self):
        return self.__symbol_label

    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, n):
        self.__next = n

    @property
    def super(self):
        return self.__super

    @super.setter
    def super(self, s):
        self.__super = s

    def about(self):
        print(self.__symbol_label)
        print(self.__symbol_class)
        print(self.__bounds)
        print(self.__centroid)
        print(self.__regions)

    def __eq__(self, other):  # Может, не надо так?
        if isinstance(other, Symbol):
            return id(self) == id(other)
        return False


# Функция для создания списка объектов Symbol из списка, полученного от модуля с нейронкой
def symbols_data_convertor(input_symbols_data):
    symbols_list = []
    for x in input_symbols_data:
        s = Symbol(x[0])
        s.bounds = Bounds(left=x[1][0], top=x[1][1], right=x[1][0] + x[1][2], bottom=x[1][1] + x[1][3])
        s.symbol_class = classes_dictionary[s.symbol_label]
        set_symbol_thresholds_and_centroid(s)

        symbols_list.append(s)

    return symbols_list


# Параметры могут отлючаться от табличных
# Нужно перепроверить..
def set_symbol_thresholds_and_centroid(symbol):
    H = symbol.bounds.bottom - symbol.bounds.top
    if symbol.symbol_class == SymbolClass.NON_SCRIPTED:
        symbol.centroid = [(symbol.bounds.right + symbol.bounds.left) / 2,
                           symbol.bounds.bottom - 1 / 2 * H]
        symbol.regions = Regions(next=symbol.bounds.right,
                                 super=-math.inf,  # Нужно не inf, а границы символа. Думаю, что будет лучше
                                 subsc=math.inf,  # ??? -inf?
                                 above=symbol.bounds.bottom - H / 2,
                                 below=symbol.bounds.bottom - H / 2)
    elif symbol.symbol_class == SymbolClass.PLAIN_ASCENDER:
        symbol.centroid = [(symbol.bounds.right + symbol.bounds.left) / 2,
                           symbol.bounds.bottom - centroid_ratio * H]
        symbol.regions = Regions(next=symbol.bounds.right,
                                 super=symbol.bounds.bottom - (H - threshold_ratio * H),
                                 subsc=symbol.bounds.bottom - threshold_ratio * H,
                                 above=symbol.bounds.bottom - (H - threshold_ratio * H),
                                 below=symbol.bounds.bottom - threshold_ratio * H)
    elif symbol.symbol_class == SymbolClass.PLAIN_DESCENDER:
        symbol.centroid = [(symbol.bounds.right + symbol.bounds.left) / 2,
                           symbol.bounds.bottom - (H - centroid_ratio * H)]
        symbol.regions = Regions(next=symbol.bounds.right,
                                 super=symbol.bounds.bottom - (H - threshold_ratio / 2 * H),
                                 subsc=symbol.bounds.bottom - (H / 2 + threshold_ratio / 2 * H),
                                 above=symbol.bounds.bottom - (H - threshold_ratio / 2 * H),
                                 below=symbol.bounds.bottom - (H / 2 + threshold_ratio / 2 * H))
    elif symbol.symbol_class == SymbolClass.PLAIN_CENTERED:
        symbol.centroid = [(symbol.bounds.right + symbol.bounds.left) / 2,
                           symbol.bounds.bottom - 1 / 2 * H]
        symbol.regions = Regions(next=symbol.bounds.right,
                                 super=symbol.bounds.bottom - (H - threshold_ratio * H),
                                 subsc=symbol.bounds.bottom - threshold_ratio * H,
                                 above=symbol.bounds.bottom - (H - threshold_ratio * H),
                                 below=symbol.bounds.bottom - threshold_ratio * H)


def sort_symbols_list(symbols):
    symbols.sort(key=lambda s: s.bounds.left)


# Пока так
def dominance(s1, s2):
    return False


def find_start_symbol(symbols):
    L = symbols.copy()
    n = len(L)
    while n > 1:
        if dominance(L[n - 1], L[n - 2]):
            del L[n - 2]
        else:
            del L[n - 1]
        n = n - 1

    return L[0]


def is_adjacent(s1, s2):
    if s1.regions[1] <= s2.centroid[1] <= s1.regions[2]: # >= ??? Везде сделать одинаково
        return True

    return False


def belong_region(s1, s2):
    x_cent = s2.centroid[0]
    y_cent = s2.centroid[1]

    if x_cent > s1.bounds.right and y_cent < s1.regions[1]:
        return 1  # 1 - это super из Regions. Пока так...

    pass  # Дописать


# HOR
def find_next_in_baseline(s_cur, symbols):
    for x in symbols:
        if x.bounds.left <= s_cur.bounds.left:
            continue
        if is_adjacent(s_cur, x):
            return x

    return None


def do_layout_pass(data):
    symbols = symbols_data_convertor(data)

    #for s in symbols:
    #    s.about()
    return layout_pass(symbols)


def layout_pass(symbols):
    if symbols is None or len(symbols) == 0:
        return None

    sort_symbols_list(symbols)
    s_return = s = find_start_symbol(symbols)

    next_s = find_next_in_baseline(s, symbols)
    while len(symbols) > 0:
        #
        list = [[]]  # Странно выглядит, но пока так..
        #
        while len(symbols) > 0 and symbols[0] != next_s:
            if symbols[0] == s:
                symbols.pop(0)
                continue
            region = belong_region(s, symbols[0]) - 1
            list[region].append(symbols[0])
            symbols.pop(0)

        s.next = next_s
        s.super = layout_pass(list[0])
        # И т.д.
        s = next_s
        next_s = find_next_in_baseline(s, symbols)

    return s_return
