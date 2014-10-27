from ..Symbol import Symbol

class Warrant(Symbol):
    def __init__(self, ticker, name, exchange):
        Symbol.__init__(self, ticker, name, exchange)

    def getType(self):
        return 'Warrant'

    def getRow(self):
        return Symbol.getRow(self)
