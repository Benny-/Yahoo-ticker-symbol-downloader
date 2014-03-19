from ytd.SymbolDownloader import SymbolDownloader
from ytd.symbols.Stock import Stock

class StockDownloader(SymbolDownloader):
    def __init__(self):
        SymbolDownloader.__init__(self, "Stock")
    
    def decodeSymbolsContainer(self, symbolsContainer):
        symbols = []
        for row in symbolsContainer:
            ticker = row.contents[0].string
            companyName = row.contents[1].string
            type = row.contents[3].string
            categoryName = row.contents[4].string
            categoryNr = 0
            if(categoryName != None):
                categoryNr = row.contents[4].a.get('href').split("/").pop().split(".")[0]
            exchange = row.contents[5].string
            
            symbols.append(Stock(ticker, companyName, exchange, categoryName, categoryNr))
        return symbols

    def getRowHeader(self):
        return SymbolDownloader.getRowHeader(self) + ["categoryName", "categoryNr"]
