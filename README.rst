Yahoo ticker downloader
=======================

Produces .csv, .xlsx, .json and .yaml files (All files contain same data but in a
different format) for stocks, ETF, futures, indexes, mutual funds, currency,
warrants and bonds. The ticker symbol, company name and exchange are saved for
all symbols.

It gets its data from `https://finance.yahoo.com/lookup/`_. Please note: it
is not possible to get all the symbols due to limitations set by Yahoo.

Requirements
---------------------

Python 2.7 or Python 3.5+

Install
---------------------

From python package manager (preferred):

.. code:: bash

    pip install Yahoo-ticker-downloader

From source:

.. code:: bash

    python setup.py install

Example Usage
---------------------

.. code::

    usage: YahooTickerDownloader.py [-h] [-i] [-e] [-E EXCHANGE] [-s SLEEP] [-p]
                                    [type]

    positional arguments:
      type                  The type to download, this can be: generic

    optional arguments:
      -h, --help            show this help message and exit
      -i, --insecure        use HTTP instead of HTTPS
      -e, --export          export immediately without downloading (Only useful if
                            you already downloaded something to the .pickle file)
      -E EXCHANGE, --Exchange EXCHANGE
                            Only export ticker symbols from this exchange (the
                            filtering is done during the export phase)
      -s SLEEP, --sleep SLEEP
                            The time to sleep in seconds between requests
      -p, --pandantic       Stop and warn the user if some rare assertion fails

For example to download all stock symbols you run it like:

.. code:: bash

    YahooTickerDownloader.py

The program takes a few weeks before it is finished.
The program supports suspending and resuming a download.
Press CTRL+C to suspend download. Restart the program
in the same working directory to resume downloading.
It is possible to export partially downloaded results using the -e flag.

Example of CSV output:

.. code::

    Ticker	Name	Exchange	exchangeDisplay	Type	TypeDisplay
    JNUG	Direxion Daily Jr Gld Mnrs Bull 3X ETF	ASE	NYSE MKT	E	ETF
    DWDP	DowDuPont Inc.	NYQ	NYSE	S	Equity
    E	Eni S.p.A.	NYQ	NYSE	S	Equity
    EQH	AXA Equitable Holdings, Inc.	NYS	NYSE	S	Equity
    XOM	Exxon Mobil Corporation	NYQ	NYSE	S	Equity
    ETP	Energy Transfer Partners, L.P.	NYQ	NYSE	S	Equity
    ES=F	E-mini S&P 500 Index Futures,Jufuture	CME	Chicago Mercantile Exchange	F	Futures
    NQ=F	E-mini Nasdaq 100 Index Futuresfuture	CME	Chicago Mercantile Exchange	F	Futures
    GE=F	Eurodollar Futures,Sep-2018future	CME	Chicago Mercantile Exchange	F	Futures
    ...ect

Depending on the type you are downloading, you will get between 3.000 and 100.000+
entries.

Further resources
---------------------

Download history for symbols: ystockquote_

Changelog
---------------------

* Version 3.0.1 (2018-12-01)

  * Removed reppy dependency

* Version 3.0.0 (2018-05-27)

  * Switched over to different JSON api (searchassist)

* Version 2.2.0 (2018-01-31)

  * Continue exporting to different formats if one export fails ( #41 )
  * Check robots.txt ( anti-feature )

* Version 2.1.1 (2017-08-02)

  * A too old requests dependency was listed ( #35 )

* Version 2.1.0 (2017-05-10)

  * Added market parameter ( pull request #33 )

* Version 2.0.1 (2017-05-07)

  * Fixed issue where all downloads except stock and currency stopped working.

* Version 2.0.0 (2017-05-05)

  * Switched over to JSON api

* Version 1.0.0 (2017-04-04)

  * Reverted some changes from 0.10.0. Bond is back. Reverted back to English site instead of German.
  * Resolved CSV issue again. Closes #23 and #16.
  * Merged #26 Workaround Y! b>2000 limit
  * Scraper now scrapes a lot more at the expense of runtime.
  * Support for python2 is back. Latest python 2 & 3 are supported.
  * Removed xls support
  * Added xlsx support (#29)

* Version 0.10.1 (2017-02-04)

  * More descriptive help message

* Version 0.10.0 (2017-02-02)

  * Removed bond downloading option.
  * Uses different yahoo source. Fixes #18
  * Removed python2 from classifiers. Related to #16

* Version 0.9.0 (unreleased)

  * Added a flag to restrict output to specific stock exchanges.

* Version 0.8.1 (2016-08-17)

  * Workaround for #7 : downloading interruption
  * Solution for #9 : UnicodeEncodeError

* Version 0.7.0 (2016-03-20)

  * Added --export option. It will transcode the .pickle file immediately to the desired output formats.

* Version 0.6.0 (unreleased)

  * Add 3 retries with an exponential back-off if HTTPError or ChunkedEncodingError is raised when processing _fetchHtml.

* Version 0.5.0 (2015-08-16)

  * Allows downloading using a insecure connection.
  * The temporarily download file-names now include the ticker type.

* Version 0.4.0 (2014-10-28)

  * Warrant symbols can now be downloaded.
  * Bond symbols can now be downloaded.

* Version 0.3.0 (2014-08-14)

  * Use HTTPS instead of HTTP
  * Retry to fetch a page if it contains no symbols (A "fix" for issue #4)
  * Renamed all 'Curreny' to 'Currency'
  * Relative imports are used
  * Fix: .csv file it outputs is encoded in UTF-8 when using python2
  * Performance: Considerable reduced memory consumption
  * It now outputs .json, .yaml and .xls files in addition to .csv

.. _`https://finance.yahoo.com/lookup/`: https://finance.yahoo.com/lookup/
.. _ystockquote: https://pypi.python.org/pypi/ystockquote/

