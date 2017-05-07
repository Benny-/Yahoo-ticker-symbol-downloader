from ..SymbolDownloader import SymbolDownloader
from ..symbols.Future import Future

from ..compat import text

class FutureDownloader(SymbolDownloader):
    def __init__(self):
        SymbolDownloader.__init__(self, "futures")

    def decodeSymbolsContainer(self, json):
        symbols = []
        count = 0

        for row in json['data']['result']:
            ticker = text(row['symbol'])
            name = row['companyName']
            exchange = row['exchange']
            symbols.append(Future(ticker, name, exchange))

        if ('F' in json['data']['hits']):
            count = int(json['data']['hits']['F']['count'])

        return (symbols, count)