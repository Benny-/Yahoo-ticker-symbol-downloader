from ..Symbol import Symbol

class ETF(Symbol):
    def __init__(self, ticker, name, exchange):
        Symbol.__init__(self, ticker, name, exchange)

    def getType(self):
        return 'ETF'
