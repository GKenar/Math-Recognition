from symbols import symbol_to_str, Symbols
from layoutpass import Symbol


def adapt_to_solver(s: Symbol):
    return ''.join(__adapt_to_solver(s))


def __adapt_to_solver(s: Symbol):
    list = []
    while s is not None:
        if s.symbol_label == Symbols.SYMBOL_FRACTION:
            list.extend('(')
            list.extend(adapt_to_solver(s.above))
            list.extend(')/(')
            list.extend(adapt_to_solver(s.below))
            list.extend(')')
            s = s.next  # Переделать
            continue

        list.append(symbol_to_str(s.symbol_label))

        if s.super is not None:
            list.extend('^(')
            list.extend(adapt_to_solver(s.super))
            list.extend(')')
        if s.subsc is not None:
            list.extend('_(')
            list.extend(adapt_to_solver(s.subsc))
            list.extend(')')

        s = s.next
    return list