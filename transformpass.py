__all__ = ["do_transform"]

from layoutpass import Symbol, Bounds, set_symbol_thresholds_and_centroid
from symbols import Symbols


def do_transform(s: Symbol):
    transform(s)


def transform(s: Symbol):
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

    if s.symbol_label == Symbols.SYMBOL_MINUS and ((s.above is not None and
                                                    s.above.symbol_label == Symbols.SYMBOL_MINUS and
                                                    __is_no_surroundings(s.above)) or
                                                   (s.below is not None and
                                                    s.below.symbol_label == Symbols.SYMBOL_MINUS and
                                                    __is_no_surroundings(s.below))):
        __transform_to_equal(s)

    if s.above is not None and \
            s.below is not None and \
            s.symbol_label == Symbols.SYMBOL_MINUS:
        s.symbol_label = Symbols.SYMBOL_FRACTION

    transform(s.next)
    transform(s.super)
    transform(s.subsc)
    transform(s.below)
    transform(s.above)


def __is_no_surroundings(s: Symbol):
    if s.above is None and s.below is None and \
            s.subsc is None and s.super is None and s.next is None:
        return True
    else:
        return False


def __transform_to_equal(s: Symbol):
    if s.above is not None:
        second_line = s.above
    else:
        second_line = s.below

    left = s.bounds.left if s.bounds.left < second_line.bounds.left else second_line.bounds.left
    right = s.bounds.right if s.bounds.right > second_line.bounds.right else second_line.bounds.right
    top = s.bounds.top if s.bounds.top < second_line.bounds.top else second_line.bounds.top
    bottom = s.bounds.bottom if s.bounds.bottom > second_line.bounds.bottom else second_line.bounds.bottom

    s.symbol_label = Symbols.SYMBOL_EQUAL
    s.bounds = Bounds(left=left, top=top, right=right, bottom=bottom)
    set_symbol_thresholds_and_centroid(s)

    s.above = None
    s.below = None
