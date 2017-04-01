from ..SymbolDownloader import SymbolDownloader
from ..symbols.ETF import ETF

from ..compat import text

class ETFDownloader(SymbolDownloader):
    def __init__(self):
        SymbolDownloader.__init__(self, "ETF")

    def decodeSymbolsContainer(self, symbolsContainer):
        symbols = []
        for row in symbolsContainer:
            ticker = text(row.contents[0].string)
            name = row.contents[1].string
            if name is not None:
                name = text(name)
            t = text(row.contents[3].string)
            if(t.strip().lower() != 'ETF'.lower()):
                pass # raise TypeError("Unexpected type. Got: " + t)
            exchange = row.contents[5].string
            if exchange is not None:
                exchange = text(exchange)
            
            symbols.append(ETF(ticker, name, exchange))
        return symbols

