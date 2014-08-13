from ..SymbolDownloader import SymbolDownloader
from ..symbols.Future import Future

from ..compat import unicode

class FutureDownloader(SymbolDownloader):
    def __init__(self):
        SymbolDownloader.__init__(self, "Future")

    def decodeSymbolsContainer(self, symbolsContainer):
        symbols = []
        for row in symbolsContainer:
            ticker = unicode(row.contents[0].string)
            name = row.contents[1].string
            if name is not None:
                name = unicode(name)
            type = row.contents[3].string
            exchange = row.contents[5].string
            if exchange is not None:
                exchange = unicode(exchange)

            symbols.append(Future(ticker, name, exchange))
        return symbols

