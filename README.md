Yahoo ticker downloader
==============================

A python3 script to scrape a lot - but not all - ticker symbols from yahoo finance.

It produces a .csv file for stocks, futures, ETF, indexes, mutual funds and currency. The ticker symbol, (company)name and exchange are saved. The category is stored too for stock symbols.

Its source is [http://finance.yahoo.com/lookup/](http://finance.yahoo.com/lookup/).

## Installation

```bash
python setup.py install
```

## Running

The first param is one of the following values: stocks etf index currency future mutualfund

```bash
YahooTickerDownloader.py stocks
```

The program takes up a lot of RAM (up to 2GB) and several hours before it produces the .csv file. Sorry. The program supports suspending and resuming a download. Simply press CTRL+C to suspend download. Restart the program in the same working directory to resume downloading.

Example of output:
```csv
Ticker,Name,Exchange,categoryName,categoryNr
ENZ,"Enzo Biochem Inc.",NYQ,"Medical Laboratories & Research",525
ENZN,"Enzon Pharmaceuticals Inc.",NMS,Biotechnology,515
ENZR,"Energizer Resources Inc.",PNK,,0
EOAA.DE,"E.ON AG",GER,"Diversified Utilities",913
KMX,"CarMax Inc.",NYQ,"Auto Dealerships",744
KMY.MU,KIMBERLY-CLARK,MUN,"Personal Products",323
KN1.DU,ECOUNION,DUS,"Business Software & Services",826
KNCAY,"Konica Minolta Holdings Inc.",PNK,,0
KND,"Kindred Healthcare Inc.",NYQ,"Long-Term Care Facilities",523
KNDI,"Kandi Technologies, Corp",NGM,"Auto Manufacturers - Major",330
```
