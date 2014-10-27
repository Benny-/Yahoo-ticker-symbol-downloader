from ..Symbol import Symbol

class Warrant(Symbol):
    def __init__(self, ticker, name, exchange, categoryName, categoryNr):
        Symbol.__init__(self, ticker, name, exchange)
        self.categoryName = categoryName
        self.categoryNr = categoryNr


    def getType(self):
        return 'Warrant'

    def getRow(self):
        return Symbol.getRow(self) + [self.categoryName , self.categoryNr]
