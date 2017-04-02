from ..SymbolDownloader import SymbolDownloader
from ..symbols.Future import Future

from ..compat import text

class FutureDownloader(SymbolDownloader):
    def __init__(self):
        SymbolDownloader.__init__(self, "Future")

    def decodeSymbolsContainer(self, symbolsContainer):
        symbols = []
        for row in symbolsContainer:
            ticker = text(row.contents[0].string)
            name = row.contents[1].string
            if name is not None:
                name = text(name)
            t = text(row.contents[3].string)
            if(t.strip().lower() != 'Future'.lower()):
                pass #raise TypeError("Unexpected type. Got: " + t)
            exchange = row.contents[5].string
            if exchange is not None:
                exchange = text(exchange)
            
            symbols.append(Future(ticker, name, exchange))
        return symbols

