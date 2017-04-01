from ..SymbolDownloader import SymbolDownloader
from ..symbols.Warrant import Warrant

from ..compat import text

class WarrantDownloader(SymbolDownloader):
    def __init__(self):
        SymbolDownloader.__init__(self, "Warrant")

    def decodeSymbolsContainer(self, symbolsContainer):
        symbols = []
        for row in symbolsContainer:
            ticker = text(row.contents[0].string)
            name = row.contents[1].string
            if name is not None:
                name = text(name)
            t = text(row.contents[3].string)
            if(t.strip().lower() != 'Warrant'.lower()):
                pass # raise TypeError("Unexpected type. Got: " + t)
            exchange = row.contents[5].string
            if exchange is not None:
                exchange = text(exchange)

            symbols.append(Warrant(ticker, name, exchange))
        return symbols

    def getRowHeader(self):
        return SymbolDownloader.getRowHeader(self)

0

