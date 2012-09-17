from yahoofinance.SymbolDownloader import SymbolDownloader
from yahoofinance.symbols.Curreny import Curreny

class CurrenyDownloader(SymbolDownloader):
	def __init__(self):
		SymbolDownloader.__init__(self, "Curreny")
	
	def decodeSymbolsContainer(self, symbolsContainer):
		symbols = []
		for row in symbolsContainer:
			ticker = row.contents[0].string
			name = row.contents[1].string
			type = row.contents[3].string
			exchange = row.contents[5].string
			
			symbols.append(Curreny(ticker, name, exchange))
		return symbols
	