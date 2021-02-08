__all__ = ["do_lexical_analysis"]

from layoutpass import Symbol
from enum import Enum
from symbols import Symbols, SymbolType, symbol_type, symbol_to_str


class TokenType(Enum):
    NUMBER = 1
    OPERATOR = 2
    BRACKET = 3


class Token:
    """Класс, описывающий один токен"""
    __value = None
    __token_type = None
    __next = None
    __super = None
    __subsc = None
    __above = None
    __below = None

    def __init__(self, value, t_type):
        self.__value = value
        self.__token_type = t_type

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, v):
        self.__value = v

    # Можно сделать общий родительский класс с next и т.п.
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

    @property
    def subsc(self):
        return self.__subsc

    @subsc.setter
    def subsc(self, s):
        self.__subsc = s

    @property
    def below(self):
        return self.__below

    @below.setter
    def below(self, b):
        self.__below = b

    @property
    def above(self):
        return self.__above

    @above.setter
    def above(self, a):
        self.__above = a


def is_grouping(st1, st2):
    if st1 == SymbolType.DIGIT:
        if st2 == SymbolType.DIGIT or st2 == SymbolType.DECIMAL_DOT:
            return True
    elif st1 == SymbolType.DECIMAL_DOT:
        if st2 == SymbolType.DIGIT:
            return True
    else:
        return False


def have_surrounds(s: Symbol):
    if s.subsc is None and s.super is None and \
            s.above is None and s.below is None:
        return False
    else:
        return True


def do_lexical_analysis(s: Symbol):  # Не очень круто, что функция меняет значение входящего параметра и что-то ещё и возвращает
    preprocessing(s)
    t = tokenizer(s)
    return t


def preprocessing(s: Symbol):
    if s is None:
        return

    # Пока такое решение. Иногда точка попадает в below..
    if s.subsc is not None and s.subsc.symbol_label == Symbols.SYMBOL_DOT:
        s.subsc.symbol_label = Symbols.SYMBOL_DECIMAL_DOT
        s.subsc.next = s.next
        s.next = s.subsc
        s.subsc = None

    if s.symbol_label == Symbols.SYMBOL_DOT:  # Пока такое решение
        s.symbol_label = Symbols.SYMBOL_MUL

    if s.above is not None and \
            s.below is not None and \
            s.symbol_label == Symbols.SYMBOL_MINUS:
        s.symbol_label = Symbols.SYMBOL_FRACTION

    preprocessing(s.next)
    preprocessing(s.super)
    preprocessing(s.subsc)
    preprocessing(s.below)
    preprocessing(s.above)


def group_to_number(group):  # Пока такой костыль
    l = []
    for x in group:
        l.append(symbol_to_str(x))

    str = ''.join(l)
    return int(str)


def tokenizer(s: Symbol):
    if s is None:
        return None

    group = [s.symbol_label]
    s_type = symbol_type(s.symbol_label)
    while s.next is not None and \
            is_grouping(symbol_type(s.symbol_label), symbol_type(s.next.symbol_label)) and \
            not have_surrounds(s):
        group.append(s.next.symbol_label)
        s = s.next

    if s_type == SymbolType.DIGIT:
        token_value = group_to_number(group)
    else:
        token_value = group.pop()

    token = Token(token_value, s_type)
    token.next = tokenizer(s.next)
    token.super = tokenizer(s.super)
    token.subsc = tokenizer(s.subsc)
    token.above = tokenizer(s.above)
    token.below = tokenizer(s.below)
    return token
