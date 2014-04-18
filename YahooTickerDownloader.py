#!/usr/bin/env python

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

sys.setrecursionlimit(10000) # Do not remove this line. It contains magic. Required for correct pickling/unpickling.

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
        pickle.dump(downloader, file=file, protocol=pickle.HIGHEST_PROTOCOL)

def main():
    
    downloader = None

    print("Checking if we can resume a old download session")
    try:
        downloader = loadDownloader();
        print("Downloader found on disk, resuming")
    except:
        print("No old downloader found on disk")
        if(len(sys.argv) <= 1):
            print("First argument must be the symbol type to download:")
            for key in options.keys():
                print( " " + key )
            print("Example: YahooTickerDownloader.py stocks")
            exit(1)
        else:
            downloader = options[sys.argv[1]]

    try:
        if not downloader.isDone():
            print("Downloading " + downloader.type)
            print ("")
            symbols = downloader.fetchNextSymbols()
            lastSaveQuery = downloader.getQuery()
            while not downloader.isDone():
            
                print("Got " + str(len(symbols)) + " downloaded " + downloader.type + " symbols:")
                if(len(symbols)>2):
                    print (" " + str(symbols[0]))
                    print (" " + str(symbols[1]))
                    print ("  ect...")
            
                print("Progress:" +
                    " Query " + str(downloader.getQueryNr()) + "/" + str(downloader.getTotalQueries()) + "."
                    " Items in current query: " + str(downloader.getItems()) + "/" + str(downloader.getTotalItems()) + "."
                    " Total collected unique " + downloader.type + " entries: " + str(downloader.getCollectedSymbolsSize())
                    )
                print ("")
            
                # Save download state. We do this in case this long running is suddenly interrupted.
                if downloader.getQuery() != lastSaveQuery:
                    lastSaveQuery = downloader.getQuery()
                    print ("Saving downloader to disk...")
                    saveDownloader(downloader)
                    print ("Downloader successfully saved.")
                    print ("")
            
                sleep(5) # So we don't overload the server.
                
                symbols = downloader.fetchNextSymbols()
                
    except Exception as ex:
        print("A exception occurred while downloading. Suspending downloader to disk")
        saveDownloader(downloader)
        print("Successfully saved download state")
        print("Remove downloader.pickle if this error persists")
        print("Issues can be reported on https://github.com/Benny-/Yahoo-ticker-symbol-downloader/issues")
        print("")
        raise
    except KeyboardInterrupt as ex:
        print("Suspending downloader to disk")
        saveDownloader(downloader)
    
    if downloader.isDone():
        print("Exporting "+downloader.type+" symbols to "+downloader.type+".csv")
        with open(downloader.type+'.csv', 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(downloader.getRowHeader())
            for symbol in downloader.getCollectedSymbols():
                csvwriter.writerow(symbol.getRow())

if __name__ == "__main__":
    main()

