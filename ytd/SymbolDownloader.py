import requests
import string
from time import sleep
import math

from bs4 import BeautifulSoup

class SymbolDownloader:
    """Abstract class"""

    def __init__(self, type):
        # All downloaded symbols are stored in a dict before exporting
        # This is to ensure no duplicate data
        self.symbols = {}
        self.rsession = requests.Session()
        self.type = type

        self.queries = string.ascii_lowercase;
        self.current_q = self.queries[0]
        self.current_q_item_offset = 0
        self.current_q_total_items = 'Unknown'  # This field is normally a int
        self.current_page_retries = 0
        self.done = False

    def _fetchHtml(self, insecure):
        query_string = {
                's': self.current_q,
                't': self.type[0],
                'm': 'ALL',
                'r': '',
                'b': str(self.current_q_item_offset)
            }

        protocol = 'http' if insecure else 'https'
        user_agent = {'User-agent': 'yahoo-ticker-symbol-downloader'}
        req = requests.Request('GET', protocol+'://finance.yahoo.com/lookup/',
                headers=user_agent, params=query_string)
        req = req.prepare()
        print("req " + req.url) # Used for debugging
        resp = self.rsession.send(req)
        resp.raise_for_status()

        return resp.text

    def decodeSymbolsContainer(self, symbolsContainer):
        raise Exception("Function to extract symbols must be overwritten in subclass. Generic symbol downloader does not know how.")

    def _getQueryIndex(self):
        return self.queries.index(self.current_q)

    def getTotalQueries(self):
        return len(self.queries)

    def _getTotalItemsFromSoup(self, soup):
        total_items = None
        try:
            div = soup.find(id="pagination")
            yikkes = str(div).split("of")[1].split("|")[0]
            yikkes = "".join([char for char in yikkes if char in string.digits])
            total_items = int(yikkes)
        except Exception as ex:
            total_items = 'Unknown'
        return total_items

    def _nextQuery(self):
        self.current_page_retries = 0
        self.current_q_item_offset = 0
        self.current_q_total_items = 'Unknown'

        if self._getQueryIndex() + 1 >= len(self.queries):
            self.current_q = self.queries[0]
            self.done = True
        else:
            self.current_q = self.queries[self._getQueryIndex() + 1]

    def nextRequest(self, insecure=False):

        success = False
        retryCount = 0
        html = ""
        # _fetchHtml may raise an exception based on response status or
        # if the request caused a transport error.
        # At this point we try a simple exponential back-off algorithm
        # to attempt 3 more times sleeping 5, 25, 125 seconds
        # respectively.
        while(success == False):
            try:
                html = self._fetchHtml(insecure)
                success = True
            except (requests.HTTPError, requests.exceptions.ChunkedEncodingError) as ex:
                if retryCount < 3:
                    attempt = retryCount + 1
                    sleepAmt = int(math.pow(5,attempt))
                    print("Retry attempt: " + str(attempt) + "."
                        " Sleep period: " + str(sleepAmt) + " seconds."
                        )
                    sleep(sleepAmt)
                    retryCount = attempt
                else:
                    raise

        soup = BeautifulSoup(html, "html.parser")
        symbols = None

        try:
            # A exception is thrown here for the following reasons:
            # 1. Yahoo does not include a table (or any results!) if you
            #    request items at offset 2020 or more
            # 2. Yahoo randomly screws a http request up and table is missing.
            #    A succesive http request might not result in a exception here.
            symbolsContainer = soup.find("table", {"class": "yui-dt"}).tbody
            symbols = self.decodeSymbolsContainer(symbolsContainer)
        except:
            symbols = []

        for symbol in symbols:
            self.symbols[symbol.ticker] = symbol

        self.current_q_item_offset = self.current_q_item_offset + len(symbols)
        self.current_q_total_items = self._getTotalItemsFromSoup(soup)
        if len(symbols) == 0:
            self.current_page_retries += 1
            if self.current_page_retries > 20:
                self._nextQuery()
        else:
            self.current_page_retries = 0
        return symbols

    def isDone(self):
        return self.done

    def getCollectedSymbols(self):
        return self.symbols.values()

    def getRowHeader(self):
        return ["Ticker", "Name", "Exchange"]

    def printProgress(self):
        if self.isDone():
            print("Progress: Done!")
        else:
            print("Progress:" +
                " Query " + str(self._getQueryIndex()) + "/" + str(self.getTotalQueries()) + "."
                " Items handled in current query: " + str(self.current_q_item_offset) + "/" + str(self.current_q_total_items) + "."
                " Total collected unique " + self.type + " entries: " + str(len(self.symbols))
                )
        print ("")
