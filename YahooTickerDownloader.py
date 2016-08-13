#!/usr/bin/env python

import pickle
from time import sleep
import argparse

from ytd.downloader.StockDownloader import StockDownloader
from ytd.downloader.ETFDownloader import ETFDownloader
from ytd.downloader.FutureDownloader import FutureDownloader
from ytd.downloader.IndexDownloader import IndexDownloader
from ytd.downloader.MutualFundDownloader import MutualFundDownloader
from ytd.downloader.CurrencyDownloader import CurrencyDownloader
from ytd.downloader.WarrantDownloader import WarrantDownloader
from ytd.downloader.BondDownloader import BondDownloader
from ytd.compat import unicode

import tablib

options = {
    "stocks": StockDownloader(),
    "etf": ETFDownloader(),
    "future": FutureDownloader(),
    "index": IndexDownloader(),
    "mutualfund": MutualFundDownloader(),
    "currency": CurrencyDownloader(),
    "warrant": WarrantDownloader(),
    "bond": BondDownloader(),
}


def loadDownloader(tickerType):
    with open(tickerType + ".pickle", "rb") as f:
        return pickle.load(f)


def saveDownloader(downloader, tickerType):
    with open(tickerType + ".pickle", "wb") as f:
        pickle.dump(downloader, file=f, protocol=pickle.HIGHEST_PROTOCOL)


def downloadEverything(downloader, tickerType, insecure):

    loop = 0
    while not downloader.isDone():

        symbols = downloader.nextRequest(insecure)
        print("Got " + str(len(symbols)) + " downloaded " + downloader.type + " symbols:")
        if(len(symbols) > 2):
            try:
                print (" " + unicode(symbols[0]))
                print (" " + unicode(symbols[1]))
                print ("  ect...")
            except:
                print (" Could not display some ticker symbols due to char encoding")
        downloader.printProgress()

        # Save download state occasionally.
        # We do this in case this long running is suddenly interrupted.
        loop = loop + 1
        if loop % 200 == 0:
            print ("Saving downloader to disk...")
            saveDownloader(downloader, tickerType)
            print ("Downloader successfully saved.")
            print ("")

        if not downloader.isDone():
            sleep(5)  # So we don't overload the server.

def main():
    downloader = None

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--insecure", help="use HTTP instead of HTTPS", action="store_true")
    parser.add_argument("-e", "--export", help="export current .pickle file", action="store_true")
    parser.add_argument('type', help='The type to download, this can be: '+" ".join(list(options.keys())))
    args = parser.parse_args()

    if args.insecure:
        print("Using insecure connection")

    if args.export:
        print("Exporting pickle file")

    tickerType = args.type = args.type.lower()

    print("Checking if we can resume a old download session")
    try:
        downloader = loadDownloader(tickerType)
        print("Downloader found on disk, resuming")
    except:
        print("No old downloader found on disk")
        print("Starting a new session")
        if tickerType not in options:
            print("Error: " + tickerType + " is not a valid type option. See --help")
            exit(1)
        else:
            downloader = options[tickerType]

    try:
        if not args.export:
            if not downloader.isDone():
                print("Downloading " + downloader.type)
                print("")
                downloadEverything(downloader, tickerType, args.insecure)
                print ("Saving downloader to disk...")
                saveDownloader(downloader, tickerType)
                print ("Downloader successfully saved.")
                print ("")
            else:
                print("The downloader has already finished downloading everything")
                print("")

    except Exception as ex:
        print("A exception occurred while downloading. Suspending downloader to disk")
        saveDownloader(downloader, tickerType)
        print("Successfully saved download state")
        print("Remove downloader.pickle if this error persists")
        print("Issues can be reported on https://github.com/Benny-/Yahoo-ticker-symbol-downloader/issues")
        print("")
        raise
    except KeyboardInterrupt as ex:
        print("Suspending downloader to disk")
        saveDownloader(downloader, tickerType)

    if downloader.isDone() or args.export:
        print("Exporting "+downloader.type+" symbols")

        data = tablib.Dataset()
        data.headers = downloader.getRowHeader()

        for symbol in downloader.getCollectedSymbols():
            data.append(symbol.getRow())

        with open(downloader.type + '.csv', 'wb') as f:
            f.write(data.csv.encode('UTF-8'))

        with open(downloader.type + '.json', 'wb') as f:
            f.write(data.json.encode('UTF-8'))

        with open(downloader.type + '.yaml', 'wb') as f:
            f.write(data.yaml.encode('UTF-8'))

        with open(downloader.type + '.xls', 'wb') as f:
            f.write(data.xls)

if __name__ == "__main__":
    main()
