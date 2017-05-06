# -*- coding: utf-8 -*-

import sys

is_py3 = (sys.version_info[0] > 2)

if is_py3:
    text = str
    import csv
    from urllib.parse import quote
else:
    text = unicode
    from backports import csv
    from urllib import quote
