from ..SymbolDownloader import SymbolDownloader
from ..symbols.MutualFund import MutualFund

from ..compat import text

class MutualFundDownloader(SymbolDownloader):
    def __init__(self):
        SymbolDownloader.__init__(self, "funds")

    def decodeSymbolsContainer(self, json):
        symbols = []
        count = 0

        for row in json['data']['result']:
            ticker = text(row['symbol'])
            name = row['companyName']
            exchange = row['exchange']
            symbols.append(MutualFund(ticker, name, exchange))

        if ('M' in json['data']['hits']):
            count = int(json['data']['hits']['M']['count'])

        return (symbols, count)