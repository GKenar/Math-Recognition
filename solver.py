from wolframclient.evaluation import SecuredAuthenticationKey, WolframCloudSession, WolframLanguageSession
from wolframclient.language import wl
from wolframclient.language.expression import WLFunction


class Solver:
    def __init__(self, key, secret):
        self.sak = SecuredAuthenticationKey(key, secret)
        self.session = WolframCloudSession(credentials=self.sak)

    def start_session(self):
        self.session.start()

    def solve(self, expr):
        result = self.session.evaluate(expr)
        return result


def solver_output_to_str(data):
    if type(data) is WLFunction:
        if data.head == wl.Rational:
            return '{0}/{1}'.format(data.args[0], data.args[1])
        else:
            return str(data)

    return str(data)
