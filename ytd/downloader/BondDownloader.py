from ..SymbolDownloader import SymbolDownloader
from ..symbols.Bond import Bond

from ..compat import text

class BondDownloader(SymbolDownloader):
    def __init__(self):
        SymbolDownloader.__init__(self, "Bond")

    def decodeSymbolsContainer(self, symbolsContainer):
        symbols = []
        for row in symbolsContainer:
            ticker = text(row.contents[0].string)
            name = row.contents[1].string
            if name is not None:
                name = text(name)
            t = text(row.contents[4].string)
            if(t.strip().lower() != 'Bond'.lower()):
                pass # raise TypeError("Unexpected type. Got: " + t)
            exchange = row.contents[5].string
            if exchange is not None:
                exchange = text(exchange)

            symbols.append(Bond(ticker, name, exchange))
        return symbols

    def getRowHeader(self):
        return SymbolDownloader.getRowHeader(self)
