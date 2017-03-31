# -*- coding: utf-8 -*-

import sys

is_py3 = (sys.version_info[0] > 2)

if is_py3:
    unicode = str
    import csv
else:
    unicode = unicode
    from backports import csv

