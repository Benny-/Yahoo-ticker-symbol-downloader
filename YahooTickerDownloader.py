#!/usr/bin/env python

import sys
import pickle
import tablib
from time import sleep

from ytd.downloader.StockDownloader import StockDownloader
from ytd.downloader.ETFDownloader import ETFDownloader
from ytd.downloader.FutureDownloader import FutureDownloader
from ytd.downloader.IndexDownloader import IndexDownloader
from ytd.downloader.MutualFundDownloader import MutualFundDownloader
from ytd.downloader.CurrencyDownloader import CurrencyDownloader
from ytd.compat import unicode

import bs4

# Do not remove this line. It contains magic.
# Required for correct pickling/unpickling.
sys.setrecursionlimit(10000)

options = {
    "stocks": StockDownloader(),
    "etf": ETFDownloader(),
    "future": FutureDownloader(),
    "index": IndexDownloader(),
    "mutualfund": MutualFundDownloader(),
    "currency": CurrencyDownloader(),
}


def loadDownloader():
    with open("downloader.pickle", "rb") as f:
        return pickle.load(f)


def saveDownloader(downloader):
    with open("downloader.pickle", "wb") as f:
        pickle.dump(downloader, file=f, protocol=pickle.HIGHEST_PROTOCOL)


def downloadEverything(downloader):

    loop = 0
    while not downloader.isDone():

        symbols = downloader.nextRequest()
        print("Got " + str(len(symbols)) + " downloaded " + downloader.type + " symbols:")
        if(len(symbols)>2):
            print (" " + unicode(symbols[0]))
            print (" " + unicode(symbols[1]))
            print ("  ect...")
        downloader.printProgress()

        # Save download state occasionally.
        # We do this in case this long running is suddenly interrupted.
        loop = loop + 1
        if loop % 200 == 0:
            print ("Saving downloader to disk...")
            saveDownloader(downloader)
            print ("Downloader successfully saved.")
            print ("")

        if not downloader.isDone():
            sleep(5)  # So we don't overload the server.

def main():
    downloader = None

    print("Checking if we can resume a old download session")
    try:
        downloader = loadDownloader()
        print("Downloader found on disk, resuming")
    except:
        print("No old downloader found on disk")
        if(len(sys.argv) <= 1):
            print("First argument must be the symbol type to download:")
            for key in list(options.keys()):
                print( " " + key )
            print("Example: YahooTickerDownloader.py stocks")
            exit(1)
        else:
            downloader = options[sys.argv[1]]

    try:
        if not downloader.isDone():
            print("Downloading " + downloader.type)
            print("")
            downloadEverything(downloader)
            print ("Saving downloader to disk...")
            saveDownloader(downloader)
            print ("Downloader successfully saved.")
            print ("")
        else:
            print("The downloader has already finished downloading everything")
            print("")

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
        print("Exporting "+downloader.type+" symbols")

        data = tablib.Dataset()
        data.headers = downloader.getRowHeader()

        # This piece is a workaround for old saved downloader.pickle's
        # who still have bs4.element.NavigableString classes pickled.
        # It can be removed in next release.
        for symbol in downloader.getCollectedSymbols():
            row = symbol.getRow()
            for i, cell in enumerate(row):
                if cell is None:
                    row[i] = ""
                if isinstance(cell, bs4.element.NavigableString):
                    row[i] = unicode(cell)

            data.append(row)

        with open(downloader.type + '.csv', 'w') as f:
            f.write(data.csv)

        with open(downloader.type + '.json', 'w') as f:
            f.write(data.json)

        with open(downloader.type + '.yaml', 'w') as f:
            f.write(data.yaml)

        with open(downloader.type + '.xls', 'wb') as f:
            f.write(data.xls)

if __name__ == "__main__":
    main()
