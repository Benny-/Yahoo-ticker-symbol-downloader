from ..SymbolDownloader import SymbolDownloader
from ..symbols.Currency import Currency

from ..compat import text

class CurrencyDownloader(SymbolDownloader):
    def __init__(self):
        SymbolDownloader.__init__(self, "currency")

    def decodeSymbolsContainer(self, json):
        symbols = []
        count = None

        for row in json['data']['result']:
            ticker = text(row['symbol'])
            name = row['companyName']
            exchange = row['exchange']
            symbols.append(Currency(ticker, name, exchange))

        if ('C' in json['data']['hits']):
            count = int(json['data']['hits']['C']['count'])

        return (symbols, count)
