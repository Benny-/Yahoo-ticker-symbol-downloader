from .compat import is_py3, unicode

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

    def __unicode__(self):
        return "" + self.getType() + " " + self.ticker + " " + unicode(self.exchange) + " " + unicode(self.name)

if is_py3:
    Symbol.__str__ = Symbol.__unicode__
