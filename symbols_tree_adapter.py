from symbols import symbol_to_str, Symbols
from layoutpass import Symbol


def adapt_to_solver(s: Symbol):
    return ''.join(__adapt_to_solver(s))


def fraction_handling(s: Symbol, super, subsc, above, below):
    list = []
    list.extend('(')
    list.extend(above)
    list.extend(')/(')
    list.extend(below)
    list.extend(')')

    return {'head': list, 'tail': None, 'last_symbol': None}


def __adapt_to_solver(s: Symbol):
    list = []
    stack = []
    while s is not None:
        list_super = adapt_to_solver(s.super)
        list_subsc = adapt_to_solver(s.subsc)
        list_above = adapt_to_solver(s.above)
        list_below = adapt_to_solver(s.below)

        if s.symbol_label == Symbols.SYMBOL_FRACTION:
            func_parts = fraction_handling(s, list_super, list_subsc, list_above, list_below)
            list.extend(func_parts['head'])
            if func_parts['last_symbol'] is not None:
                stack.append((func_parts['last_symbol'], func_parts['tail']))
        else:
            list.append(symbol_to_str(s.symbol_label))

            if s.super is not None:
                list.extend('^(')
                list.extend(adapt_to_solver(s.super))
                list.extend(')')
            if s.subsc is not None:
                list.extend('_(')
                list.extend(adapt_to_solver(s.subsc))
                list.extend(')')

        while len(stack) != 0:
            if stack[-1][0] == s:
                list.extend(stack[-1][1])
                stack.pop()
            else:
                break

        s = s.next
    return list


