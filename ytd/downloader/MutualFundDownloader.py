from ..SymbolDownloader import SymbolDownloader
from ..symbols.MutualFund import MutualFund

from ..compat import text

class MutualFundDownloader(SymbolDownloader):
    def __init__(self):
        SymbolDownloader.__init__(self, "MutualFund")

    def decodeSymbolsContainer(self, symbolsContainer):
        symbols = []
        for row in symbolsContainer:
            ticker = text(row.contents[0].string)
            name = row.contents[1].string
            if name is not None:
                name = text(name)
            t = text(row.contents[3].string)
            if(t.strip().lower() != 'Mutual Fund'.lower()):
                pass # raise TypeError("Unexpected type. Got: " + t)
            exchange = row.contents[5].string
            if exchange is not None:
                exchange = text(exchange)

            symbols.append(MutualFund(ticker, name, exchange))
        return symbols

