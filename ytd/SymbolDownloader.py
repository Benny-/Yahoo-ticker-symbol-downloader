import requests
import string
from time import sleep
import math

from ytd.compat import text
from ytd.compat import quote

user_agent = 'yahoo-ticker-symbol-downloader'

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

    def _encodeParams(self, params):
        encoded = ''
        for key, value in params.items():
            encoded += ';' + quote(key) + '=' + quote(text(value))
        return encoded

    def _fetch(self, insecure, market):
        params = {
            'm': market,
            'b': text(self.current_q_item_offset),
            's': self.current_q,
            't': self.type[0].upper(),
            'p': 1,
        }
        query_string = {
            'device': 'console',
            'returnMeta': 'true',
        }
        protocol = 'http' if insecure else 'https'
        req = requests.Request('GET',
            protocol+'://finance.yahoo.com/_finance_doubledown/api/resource/finance.yfinlist.symbol_lookup'+self._encodeParams(params),
            headers={'User-agent': user_agent},
            params=query_string
        )
        req = req.prepare()
        print("req " + req.url)
        resp = self.rsession.send(req, timeout=(12, 12))
        resp.raise_for_status()

        if self.current_q_item_offset > 2000:  # Y! stops returning symbols at offset > 2000, workaround: add finer granulated search query
            self._add_queries(self.current_q)

        return resp.json()

    def decodeSymbolsContainer(self, symbolsContainer):
        raise Exception("Function to extract symbols must be overwritten in subclass. Generic symbol downloader does not know how.")

    def _getQueryIndex(self):
        return self.queries.index(self.current_q)

    def getTotalQueries(self):
        return len(self.queries)

    def _nextQuery(self):
        self.current_page_retries = 0
        self.current_q_item_offset = 0
        self.current_q_total_items = 'Unknown'
        self.query_done = 0

        if self._getQueryIndex() + 1 >= len(self.queries):
            self.current_q = self.queries[0]
        else:
            self.current_q = self.queries[self._getQueryIndex() + 1]

    def nextRequest(self, insecure=False, pandantic=False, market='all'):

        # You would expect query_done to be a boolean.
        # But unfortunaly we can't depend on Yahoo telling use if there
        # are any more entries. Only if yahoo tells us x amount of times in
        # succession they are done will we actually go on to the next query.
        if(self.query_done >= self.query_done_max):
            self._nextQuery()

        success = False
        retryCount = 0
        json = None
        # Eponential back-off algorithm
        # to attempt 3 more times sleeping 5, 25, 125 seconds
        # respectively.
        while(success == False):
            try:
                json = self._fetch(insecure, market)
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

        (symbols, count) = self.decodeSymbolsContainer(json)

        for symbol in symbols:
            self.symbols[symbol.ticker] = symbol

        current_q_item_offset = self.current_q_item_offset + len(symbols)
        current_q_total_items = count

        if(current_q_item_offset == current_q_total_items):
            self.query_done += 1
        elif(current_q_item_offset > current_q_total_items and pandantic):
            # This should never happen now that we are using the a JSON API
            raise Exception("Funny things are happening: current_q_item_offset "
                            + text(current_q_item_offset)
                            + " > "
                            + text(self.current_q_total_items)
                            + " current_q_total_items. Content:"
                            + "\n"
                            + repr(json))
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
