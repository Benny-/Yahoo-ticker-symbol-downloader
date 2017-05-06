from ytd.Symbol import Symbol

class Stock(Symbol):
    def __init__(self, ticker, name, exchange, categoryName):
        Symbol.__init__(self, ticker, name, exchange)
        self.categoryName = categoryName

    def getType(self):
        return 'Stock'

    def getRow(self):
        return Symbol.getRow(self) + [self.categoryName]
