from ..Symbol import Symbol

class Bond(Symbol):
    def __init__(self, ticker, name, exchange):
        Symbol.__init__(self, ticker, name, exchange)


    def getType(self):
        return 'Bond'

    def getRow(self):
        return Symbol.getRow(self)
