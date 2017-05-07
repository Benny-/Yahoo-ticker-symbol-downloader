from ..SymbolDownloader import SymbolDownloader
from ..symbols.Index import Index

from ..compat import text

class IndexDownloader(SymbolDownloader):
    def __init__(self):
        SymbolDownloader.__init__(self, "indices")

    def decodeSymbolsContainer(self, json):
        symbols = []
        count = 0

        for row in json['data']['result']:
            ticker = text(row['symbol'])
            name = row['companyName']
            exchange = row['exchange']
            symbols.append(Index(ticker, name, exchange))

        if ('I' in json['data']['hits']):
            count = int(json['data']['hits']['I']['count'])

        return (symbols, count)