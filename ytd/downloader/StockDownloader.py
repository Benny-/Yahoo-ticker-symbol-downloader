from ..SymbolDownloader import SymbolDownloader
from ..symbols.Stock import Stock

from ..compat import unicode

class StockDownloader(SymbolDownloader):
    def __init__(self):
        SymbolDownloader.__init__(self, "Stock")

    def decodeSymbolsContainer(self, symbolsContainer):
        symbols = []
        for row in symbolsContainer:
            ticker = unicode(row.contents[0].string)
            name = row.contents[1].string
            if name is not None:
                name = unicode(name)
            type = row.contents[3].string
            exchange = row.contents[4].string
            if exchange is not None:
                exchange = unicode(exchange)
            symbols.append(Stock(ticker, name, exchange))
        return symbols

    def getRowHeader(self):
        return SymbolDownloader.getRowHeader(self)

