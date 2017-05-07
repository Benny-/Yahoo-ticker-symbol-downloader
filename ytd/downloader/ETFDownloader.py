from ..SymbolDownloader import SymbolDownloader
from ..symbols.ETF import ETF

from ..compat import text

class ETFDownloader(SymbolDownloader):
    def __init__(self):
        SymbolDownloader.__init__(self, "etfs")

    def decodeSymbolsContainer(self, json):
        symbols = []
        count = None

        for row in json['data']['result']:
            ticker = text(row['symbol'])
            name = row['companyName']
            exchange = row['exchange']
            symbols.append(ETF(ticker, name, exchange))

        if ('E' in json['data']['hits']):
            count = int(json['data']['hits']['E']['count'])

        return (symbols, count)