import requests
import string

from bs4 import BeautifulSoup

class SymbolDownloader:
    """Abstract class"""
    
    def __init__(self, type):
        self.symbols = {} # All downloaded symbols are stored in a dict before exporting. This is to unsure no duplicate data
        self.rsession = requests.Session()
        self.type = type
        self.nextq = string.ascii_lowercase[0]
        self.items = 0
        self.totalItems = 0
    
    def fetchHtml(self):
        query_string = {
                's':self.nextq,
                't':self.type[0],
                'm':'ALL',
                'r':'',
                'b':str(self.items)
            }
        user_agent = { 'User-agent': 'yahoo-ticker-symbol-downloader' }
        req = requests.Request('GET', 'http://finance.yahoo.com/lookup/', headers = user_agent, params=query_string)
        req = req.prepare()
        # print("req " + req.url) # Used for debugging
        return self.rsession.send(req).text
        
    def makeSoup(self, html):
        return BeautifulSoup(html)
    
    def getSymbolsContainer(self, soup):
        symbolsContainer = soup.find("table", { "class" : "yui-dt" }).tbody
        return symbolsContainer
    
    def decodeSymbolsContainer(self, symbolsContainer):
        raise Exception("Function to extract symbols must be overwritten in subclass. Generic symbol downloader does not know how.")
    
    def getQuery(self):
        return self.nextq
    
    def getQueryNr(self):
        return string.ascii_lowercase.index(self.nextq)
    
    def getTotalQueries(self):
        return len(string.ascii_lowercase)
    
    def getTotalItemsFromSoup(self, soup):
        try:
            div = soup.find(id="pagination")
            yikkes = str(div).split("of")[1].split("|")[0]
            yikkes = "".join([char for char in yikkes if char in string.digits])
            return int( yikkes )
        except Exception as ex:
            pass
        return -1;
    
    def getItems(self):
        return self.items
    
    def getTotalItems(self):
        return self.totalItems
    
    def nextQuery(self):
        if self.getQueryNr()+1 >= len(string.ascii_lowercase):
            self.items = 0
            self.nextq = string.ascii_lowercase[0]
        else:
            self.nextq = string.ascii_lowercase[self.getQueryNr()+1]
            self.items = 0
            self.totalItems = -1

    def fetchNextSymbols(self):
        html = self.fetchHtml()
        soup = self.makeSoup(html)
        try:
            symbolsContainer = self.getSymbolsContainer(soup)
        except:
            self.nextQuery()
            if self.isDone():
                return []
            return self.fetchNextSymbols()
        symbols = self.decodeSymbolsContainer(symbolsContainer)
        for symbol in symbols:
            self.symbols[symbol.ticker] = symbol
        self.items = self.items + len(symbols)
        self.totalItems = self.getTotalItemsFromSoup(soup)
        if len(symbols) == 0:
            self.nextQuery()
        return symbols
    
    def isDone(self):
        return self.nextq == string.ascii_lowercase[0] and self.items == 0 and len(self.symbols) > 0
    
    def getCollectedSymbols(self):
        return self.symbols.values()
    
    def getCollectedSymbolsSize(self):
        return len(self.symbols)
    
    def getRowHeader(self):
        return ["Ticker", "Name", "Exchange"]

