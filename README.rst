Yahoo ticker downloader
=======================

A web scraper for ticker symbols from yahoo finance.

It produces a .csv file for stocks, futures, ETF, indexes, mutual funds
and currency. The ticker symbol, company name and exchange are saved.
The category is stored only for stock symbols.

It gets its data from `http://finance.yahoo.com/lookup/`_.

Installation
------------

From python package manager (preferred):

.. code:: bash

    pip install Yahoo-ticker-downloader

From source:

.. code:: bash

    python setup.py install

Running
-------

The first param is one of the following types: ``stocks`` ``etf``
``index`` ``currency`` ``future`` ``mutualfund``

.. code:: bash

    YahooTickerDownloader.py stocks

The program takes up a lot of RAM (up to 2GB) and several hours before
it produces the .csv file. The program supports suspending and resuming
a download. Simply press CTRL+C to suspend download. Restart the program
in the same working directory to resume downloading.

Example of output:

.. code:: csv

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
    ...ect

Depending on the type you are downloading, you will get 3.000 to 14.000
entries.

.. _`http://finance.yahoo.com/lookup/`: http://finance.yahoo.com/lookup/
