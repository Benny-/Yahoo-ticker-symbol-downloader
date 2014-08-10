from ..Symbol import Symbol

class Future(Symbol):
    def __init__(self, ticker, name, exchange):
        Symbol.__init__(self, ticker, name, exchange)

    def getType(self):
        return 'Future'
