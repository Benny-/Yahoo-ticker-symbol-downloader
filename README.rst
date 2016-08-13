Yahoo ticker downloader
=======================

Produces .csv, .json, .yaml, and .xls files (All files contain same data in a
different format) for stocks, ETF, futures, indexes, mutual funds, currency,
warrants and bonds. The ticker symbol, company name and exchange are saved.
The category the symbol belongs to is only stored for stock symbols.

It gets its data from `https://finance.yahoo.com/lookup/`_. Please note: it
is not possible to get all the symbols due to limitations set by Yahoo.
About 75%-90% of all symbols are gathered using this script depending on type.

Installation
---------------------

From python package manager (preferred):

.. code:: bash

    pip install Yahoo-ticker-downloader

From source:

.. code:: bash

    python setup.py install

Running
---------------------

The first param is one of the following types: ``stocks`` ``etf``
``future`` ``index`` ``mutualfund`` ``currency`` ``warrant`` ``bond``

.. code:: bash

    YahooTickerDownloader.py stocks

The program takes several hours before any output is generated.
The program supports suspending and resuming a download.
Press CTRL+C to suspend download. Restart the program
in the same working directory to resume downloading.

Example of output:

.. code::

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

Depending on the type you are downloading, you will between 3.000 and 26.000
entries.

Further resources
---------------------

Download history for symbols: ystockquote_

Changelog
---------------------

* Version 0.8.1

  * Workaround for #7 : downloading interruption
  * Solution for #9 : UnicodeEncodeError
  
* Version 0.7.0

  * Added --export option. It will transcode the .pickle file immediately to the desired output formats.

* Version 0.6.0

  * Add 3 retries with an exponential back-off if HTTPError or ChunkedEncodingError is raised when processing _fetchHtml.

* Version 0.5.0

  * Allows downloading using a insecure connection.
  * The temporarily download file-names now include the ticker type.

* Version 0.4.0

  * Warrant symbols can now be downloaded.
  * Bond symbols can now be downloaded.

* Version 0.3.0

  * Use https instead of http
  * Retry to fetch a page if it contains no symbols (A "fix" for issue #4)
  * Renamed all 'Curreny' to 'Currency'
  * Relative imports are used
  * Fix: .csv file it outputs is encoded in UTF-8 when using python2
  * Performance: Considerable reduced memory consumption
  * It now outputs .json, .yaml and .xls files in addition to .csv

.. _`https://finance.yahoo.com/lookup/`: https://finance.yahoo.com/lookup/
.. _ystockquote: https://pypi.python.org/pypi/ystockquote/

