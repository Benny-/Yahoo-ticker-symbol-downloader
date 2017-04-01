from ..SymbolDownloader import SymbolDownloader
from ..symbols.Stock import Stock

from ..compat import text

class StockDownloader(SymbolDownloader):
    def __init__(self):
        SymbolDownloader.__init__(self, "Stock")

    def decodeSymbolsContainer(self, symbolsContainer):
        symbols = []
        for row in symbolsContainer:
            ticker = text(row.contents[0].string)
            name = row.contents[1].string
            if name is not None:
                name = text(name)
            t = text(row.contents[3].string)
            if(t.strip().lower() != 'Stock'.lower()):
                pass # raise TypeError("Unexpected type. Got: " + t)
            categoryName = row.contents[4].string
            if categoryName is not None:
                categoryName = text(categoryName)
            categoryNr = 0
            if(categoryName != None):
                categoryNr = int(row.contents[4].a.get('href').split("/").pop().split(".")[0])
            exchange = row.contents[5].string
            if exchange is not None:
                exchange = text(exchange)

            symbols.append(Stock(ticker, name, exchange, categoryName, categoryNr))
        return symbols

    def getRowHeader(self):
        return SymbolDownloader.getRowHeader(self) + ["categoryName", "categoryNr"]

