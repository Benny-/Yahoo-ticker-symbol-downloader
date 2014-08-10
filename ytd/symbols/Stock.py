from ..Symbol import Symbol

class Stock(Symbol):
    def __init__(self, ticker, name, exchange, categoryName, categoryNr):
        Symbol.__init__(self, ticker, name, exchange)
        self.categoryName = categoryName
        self.categoryNr = categoryNr


    def getType(self):
        return 'Stock'

    def getRow(self):
        return Symbol.getRow(self) + [self.categoryName , self.categoryNr]
