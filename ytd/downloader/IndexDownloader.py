from ytd.SymbolDownloader import SymbolDownloader
from ytd.symbols.Index import Index

class IndexDownloader(SymbolDownloader):
    def __init__(self):
        SymbolDownloader.__init__(self, "Index")
    
    def decodeSymbolsContainer(self, symbolsContainer):
        symbols = []
        for row in symbolsContainer:
            ticker = row.contents[0].string
            name = row.contents[1].string
            type = row.contents[3].string
            exchange = row.contents[5].string
            
            symbols.append(Index(ticker, name, exchange))
        return symbols
    
