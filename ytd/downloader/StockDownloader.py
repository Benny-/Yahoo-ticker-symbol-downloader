from ..SymbolDownloader import SymbolDownloader
from ..symbols.Stock import Stock

from ..compat import text

class StockDownloader(SymbolDownloader):
    def __init__(self):
        SymbolDownloader.__init__(self, "stocks")

    def decodeSymbolsContainer(self, json):
        symbols = []
        count = 0

        for row in json['data']['result']:
            ticker = text(row['symbol'])
            name = row['companyName']
            exchange = row['exchange']
            categoryName = row['industryName']
            symbols.append(Stock(ticker, name, exchange, categoryName))

        if ('S' in json['data']['hits']):
            count = int(json['data']['hits']['S']['count'])

        return (symbols, count)

    def getRowHeader(self):
        return SymbolDownloader.getRowHeader(self) + ["categoryName"]

