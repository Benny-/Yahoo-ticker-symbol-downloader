from ..SymbolDownloader import SymbolDownloader
from ..symbols.Currency import Currency

from ..compat import text

class CurrencyDownloader(SymbolDownloader):
    def __init__(self):
        SymbolDownloader.__init__(self, "Currency")

    def decodeSymbolsContainer(self, symbolsContainer):
        symbols = []
        for row in symbolsContainer:
            ticker = text(row.contents[0].string)
            name = row.contents[1].string
            if name is not None:
                name = text(name)
            t = text(row.contents[3].string)
            if(t.strip().lower() != 'Currencies'.lower()):
                pass # raise TypeError("Unexpected type. Got: " + t)
            exchange = row.contents[5].string
            if exchange is not None:
                exchange = text(exchange)

            symbols.append(Currency(ticker, name, exchange))
        return symbols

