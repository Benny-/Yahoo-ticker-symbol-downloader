#!/usr/bin/env python3

import sys
import pickle
import csv
from pprint import pprint
from time import sleep

from ytd.downloader.StockDownloader import StockDownloader
from ytd.downloader.ETFDownloader import ETFDownloader
from ytd.downloader.FutureDownloader import FutureDownloader
from ytd.downloader.IndexDownloader import IndexDownloader
from ytd.downloader.MutualFundDownloader import MutualFundDownloader
from ytd.downloader.CurrencyDownloader import CurrencyDownloader

sys.setrecursionlimit(10000) # Do not remove this line. It contains magic.

options = {
	"stocks":StockDownloader(),
	"etf":ETFDownloader(),
	"future":FutureDownloader(),
	"index":IndexDownloader(),
	"mutualfund":MutualFundDownloader(),
	"currency":CurrencyDownloader(),
}

def loadDownloader():
	with open("downloader.pickle", "rb") as file:
		return pickle.load(file);

def saveDownloader(downloader):
	with open("downloader.pickle","wb") as file:
		pickle.dump(downloader, file=file)

def main():
	
	downloader = None

	print("Checking if we can resume a old download session")
	try:
		downloader = loadDownloader();
		print("Downloader found on disk, resuming")
	except:
		print("No old downloader found on disk")
		if(len(sys.argv) <= 1):
			print("First argument must be the symbol type to download")
			print("Options are:")
			for key in options.keys():
				print(key)
			exit(1)
		else:
			downloader = options[sys.argv[1]]

	try:
		if not downloader.isDone():
			print("Downloading " + downloader.type)
			symbols = downloader.fetchNextSymbols()
			lastSaveQuery = downloader.getQuery()
			while not downloader.isDone():
				print("Progress-- " +
						" Queries: " + str(downloader.getQueryNr()) + "/" + str(downloader.getTotalQueries()) +
						" Items in query: " + str(downloader.getItems()) + "/" + str(downloader.getTotalItems()) +
						" collected " + downloader.type + " data: " + str(downloader.getCollectedSymbolsSize())
						)
				symbols = downloader.fetchNextSymbols()
				print("Got " + str(len(symbols)) + " downloaded symbols")
				if(len(symbols)>2):
					print (str(symbols[0]))
					print (str(symbols[1]))
					print ("..ect")
					print ("")
			
				if downloader.getQuery() != lastSaveQuery:
					lastSaveQuery = downloader.getQuery()
					print ("Saving downloader to disk...")
					saveDownloader(downloader)
				else:
					sleep(5) # We dont wish to overload the server.
	except Exception as ex:
		print("A exception occured while downloading. Suspending downloader to disk")
		print("Remove downloader.pickle if this error persists")
		saveDownloader(downloader)
		print("Succesfully saved download state")
		print("")
		raise
	except KeyboardInterrupt as ex:
		print("Suspending downloader to disk")
		saveDownloader(downloader)
	
	if downloader.isDone():
		print("Exporting "+downloader.type+" symbols")
		with open(downloader.type+'.csv', 'w', newline='') as csvfile:
			csvwriter = csv.writer(csvfile)
			csvwriter.writerow(downloader.getRowHeader())
			for symbol in downloader.getCollectedSymbols():
				csvwriter.writerow(symbol.getRow())

if __name__ == "__main__":
    main()
