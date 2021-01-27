__all__ = ["do_lexical_analysis"]

from layoutpass import Symbol


def do_lexical_analysis(s: Symbol):
    return lexical_analysis(s)


def lexical_analysis(s: Symbol):
    if s is None:
        return

    # Пока такое решение. Иногда точка попадает в below..
    if s.subsc is not None and s.subsc.symbol_label == 'dot':
        s.subsc.symbol_label = 'dec_dot'
        s.subsc.next = s.next
        s.next = s.subsc
        s.subsc = None

    if s.above is not None and \
            s.below is not None and \
            s.symbol_label == '-':
        s.symbol_label = 'fraction'

    lexical_analysis(s.next)
    lexical_analysis(s.super)
    lexical_analysis(s.subsc)
    lexical_analysis(s.below)
    lexical_analysis(s.above)


