from wolframclient.evaluation import SecuredAuthenticationKey, WolframCloudSession, WolframLanguageSession
from wolframclient.language import wl


class Solver:
    def __init__(self, key, secret):
        self.sak = SecuredAuthenticationKey(key, secret)
        self.session = WolframCloudSession(credentials=self.sak)

    def start_session(self):
        self.session.start()

    def solve(self, expr):
        result = self.session.evaluate(expr)
        return result



