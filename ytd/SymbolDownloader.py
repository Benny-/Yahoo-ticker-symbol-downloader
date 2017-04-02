import requests
import string
from time import sleep
import math

from ytd.compat import text

from bs4 import BeautifulSoup

class SymbolDownloader:
    """Abstract class"""

    def __init__(self, type):
        # All downloaded symbols are stored in a dict before exporting
        # This is to ensure no duplicate data
        self.symbols = {}
        self.rsession = requests.Session()
        self.type = type

        self.queries = []
        self._add_queries()
        self.current_q = self.queries[0]
        self.current_q_item_offset = 0
        self.current_q_total_items = 'Unknown'  # This field is normally a int
        self.query_done = 0
        self.query_done_max = 3
        self.current_page_retries = 0
        self.done = False

    def _add_queries(self, prefix=''):
        # This method will add (prefix+)a...z to self.queries

        for i in range(len(string.ascii_lowercase)):
            element = str(prefix) + str(string.ascii_lowercase[i])
            if element not in self.queries:  # Avoid having duplicates in list
                self.queries.append(element)

    def _fetchHtml(self, insecure):
        query_string = {
                's': self.current_q,
                't': self.type[0],
                'm': 'ALL',
                'b': str(self.current_q_item_offset),
                'bypass': 'true', # I have no clue what we are bypassing.
            }
        protocol = 'http' if insecure else 'https'
        user_agent = {'User-agent': 'yahoo-ticker-symbol-downloader'}
        req = requests.Request('GET',
                protocol+'://finance.yahoo.com/lookup/'+self.type[0],
                headers=user_agent,
                params=query_string
                )
        req = req.prepare()
        print("req " + req.url)
        resp = self.rsession.send(req, timeout=(12, 12))
        resp.raise_for_status()

        if self.current_q_item_offset > 2000:  # Y! stops returning symbols at offset > 2000, workaround: add finer granulated search query 
            self._add_queries(self.current_q)

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
        self.query_done = 0

        if self._getQueryIndex() + 1 >= len(self.queries):
            self.current_q = self.queries[0]
        else:
            self.current_q = self.queries[self._getQueryIndex() + 1]

    def nextRequest(self, insecure=False, pandantic=False):
    
        # You would expect query_done to be a boolean.
        # But unfortunaly we can't depend on Yahoo telling use if there
        # are any more entries. Only if yahoo tells us x amount of times in
        # succession they are done will we actually go on to the next query.
        if(self.query_done >= self.query_done_max):
            self._nextQuery()
    
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
            except (requests.HTTPError,
                    requests.exceptions.ChunkedEncodingError,
                    requests.exceptions.ReadTimeout,
                    requests.exceptions.ConnectionError) as ex:
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
            # 2. Yahoo randomly screws a http request up and table is missing (a bad page).
            #    A succesive http request might not result in a exception here.
            # 3. A TypeError is raised. This is disabled for now.
            #    TypeError should be thrown in the different downloaders like MutualFundDownloader.py
            #    It should be a sanity check to make sure we download the correct type.
            #    But for some reason Yahoo consistently gives back some incorrect types.
            #    Search for Mutual Fund and 1 out of the 20 are ETF's.
            #    I am not sure what is going on.
            #    At the moment the sanity checks have been disabled in the different downloaders.
            symbolsContainer = soup.find("table", {"class": "yui-dt"}).tbody
            symbols = self.decodeSymbolsContainer(symbolsContainer)
        except KeyboardInterrupt as ex:
            raise
        except TypeError as ex:
            raise
        except:
            symbols = []

        for symbol in symbols:
            self.symbols[symbol.ticker] = symbol

        current_q_item_offset = self.current_q_item_offset + len(symbols)
        current_q_total_items = self._getTotalItemsFromSoup(soup)
        
        if(current_q_total_items != 'Unknown'):
            if(current_q_item_offset == current_q_total_items):
                self.query_done = self.query_done + 1
            elif(current_q_item_offset > current_q_total_items and pandantic):
                # This happens rarely for multiple requests to the same url
                # Output is garanteed to be inconsistent between runs.
                raise Exception("Funny things are happening: current_q_item_offset "
                                + text(current_q_item_offset)
                                + " > "
                                + text(self.current_q_total_items)
                                + " current_q_total_items. HTML:"
                                + "\n"
                                + text(html))
            else:
                self.query_done = 0
        
        self.current_q_item_offset = current_q_item_offset
        self.current_q_total_items = current_q_total_items
        
        if len(symbols) == 0:
            self.current_page_retries += 1
            # Related to issue #4
            # See https://github.com/Benny-/Yahoo-ticker-symbol-downloader/issues/4#issuecomment-51718922
            # Yahoo sometimes gives a "bad" page. There is no way we can determine if we are
            # At the end of pagination or if we happen to get a bad page a few times in a row.
            # So we simply request the page a lot of times. At some point we are fairly certain
            # we are at end of pagination.
            if self.current_page_retries > 20:
                self.query_done = self.query_done + self.query_done_max
        else:
            self.current_page_retries = 0
            
        if(self.query_done >= self.query_done_max):
            if self._getQueryIndex() + 1 >= len(self.queries):
                self.done = True
            else:
                self.done = False
        
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
            print("Progress:"
                + " Query " + str(self._getQueryIndex()+1) + "/" + str(self.getTotalQueries()) + "."
                + " Items handled in current query: " + str(self.current_q_item_offset) + "/" + str(self.current_q_total_items) + "."
                + "\n"
                + str(len(self.symbols)) + " unique " + self.type + " entries collected so far."
                )
        print ("")
