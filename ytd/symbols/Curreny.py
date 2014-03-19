from ytd.Symbol import Symbol

class Curreny(Symbol):
    def __init__(self, ticker, name, exchange):
        Symbol.__init__(self, ticker, name, exchange)
    
    def getType(self):
        return 'Curreny'
