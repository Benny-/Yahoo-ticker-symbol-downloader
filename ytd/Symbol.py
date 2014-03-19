class Symbol:
    """Abstract class"""
    def __init__(self, ticker, name, exchange):
        self.ticker = ticker
        self.name = name # <--- may be "None"
        self.exchange = exchange # <--- may be "None" too for some reason

    def getType(self):
        return "Undefined"

    def getRow(self):
        return [self.ticker, self.name, self.exchange]

    def __str__(self):
        return self.getType() + " " + self.ticker + " " + str(self.exchange) + " " + str(self.name)
