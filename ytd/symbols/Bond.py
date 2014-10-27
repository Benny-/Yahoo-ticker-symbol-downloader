from ..Symbol import Symbol

class Bond(Symbol):
    def __init__(self, ticker, name, exchange, categoryName, categoryNr):
        Symbol.__init__(self, ticker, name, exchange)
        self.categoryName = categoryName
        self.categoryNr = categoryNr


    def getType(self):
        return 'Bond'

    def getRow(self):
        return Symbol.getRow(self) + [self.categoryName , self.categoryNr]
