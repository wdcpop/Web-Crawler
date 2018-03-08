#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import json
import re
import hashlib
import xmltodict
import urllib
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time
import dateparser
import requests
from pyquery import PyQuery as pq
from redis import StrictRedis, ConnectionPool

redis = StrictRedis(connection_pool=ConnectionPool())

ex = {"numNew":"0","html":u"\u003Cdiv class=\u0022noselect\u0022 onselectstart=\u0022return false;\u0022 oncopy=\u0022return false;\u0022 onpaste=\u0022return false;\u0022 oncut=\u0022return false;\u0022\u003E\t\t\t\t\u003Cdiv id=\u0022trades\u0022 class=\u0022t-notification\u0022\u003E\n\t\t\t\t\t\t\u003Cdiv data-item=\u00221\u0022 class=\u0022t-notification-row item\u0022\u003E\n\t\t\t\t\t\t\t\t\t\t\t\t\u003Cdiv class=\u0022t-col1\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003EJun 06\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col2\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003E12:32 PM\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col3\u0022\u003E\n\t\t\t\t\t\t\t\u003Cp class=\u0022t-normal\u0022\u003E\n\u003Ca href=\u0022https:\/\/plus.efxnews.com\/app.php\/orders?orders%5Btype%5D=cp\u0026orders%5Bselection%5D=EUR\/USD\u0022\u003EEUR\/USD\u003C\/a\u003E - Cr\u00e9dit Agricole - SHORT Stop Order - Canceled - Entry: 1.1130, Target: 1.0700, Stop: 1.1320 (M\/T)\n\t\t\t\t\t\t\t\u003C\/p\u003E\n\t\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\t\u003Cdiv data-item=\u00221\u0022 class=\u0022t-notification-row item\u0022\u003E\n\t\t\t\t\t\t\t\t\t\t\t\t\u003Cdiv class=\u0022t-col1\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003EJun 06\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col2\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003E10:06 AM\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col3\u0022\u003E\n\t\t\t\t\t\t\t\u003Cp class=\u0022t-normal\u0022\u003E\n\u003Ca href=\u0022https:\/\/plus.efxnews.com\/app.php\/orders?orders%5Btype%5D=cp\u0026orders%5Bselection%5D=EUR\/AUD\u0022\u003EEUR\/AUD\u003C\/a\u003E - Cr\u00e9dit Agricole - SHORT Position - Opened - Entry: 1.5095, Target: 1.4650, Stop: 1.5320 (M\/T)\n\t\t\t\t\t\t\t\u003C\/p\u003E\n\t\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\t\u003Cdiv data-item=\u00221\u0022 class=\u0022t-notification-row item\u0022\u003E\n\t\t\t\t\t\t\t\t\t\t\t\t\u003Cdiv class=\u0022t-col1\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003EJun 05\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col2\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003E10:19 PM\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col3\u0022\u003E\n\t\t\t\t\t\t\t\u003Cp class=\u0022t-normal\u0022\u003E\n\u003Ca href=\u0022https:\/\/plus.efxnews.com\/app.php\/orders?orders%5Btype%5D=cp\u0026orders%5Bselection%5D=USD\/JPY\u0022\u003EUSD\/JPY\u003C\/a\u003E - Citi - SHORT Stop Order - Filled - Entry: 110.45 - Target: 108.15, Stop: 111.70 (TOTW-M\/T)\n\t\t\t\t\t\t\t\u003C\/p\u003E\n\t\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\t\u003Cdiv data-item=\u00221\u0022 class=\u0022t-notification-row item\u0022\u003E\n\t\t\t\t\t\t\t\t\t\t\t\t\u003Cdiv class=\u0022t-col1\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003EJun 05\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col2\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003E08:41 PM\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col3\u0022\u003E\n\t\t\t\t\t\t\t\u003Cp class=\u0022t-normal\u0022\u003E\n\u003Ca href=\u0022https:\/\/plus.efxnews.com\/app.php\/orders?orders%5Btype%5D=cp\u0026orders%5Bselection%5D=USD\/JPY\u0022\u003EUSD\/JPY\u003C\/a\u003E - Citi - SHORT Stop Order - Placed - Entry: 110.45, Target: 108.15, Stop: 111.70 (TOTW-M\/T)\n\t\t\t\t\t\t\t\u003C\/p\u003E\n\t\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\t\u003Cdiv data-item=\u00221\u0022 class=\u0022t-notification-row item\u0022\u003E\n\t\t\t\t\t\t\t\t\t\t\t\t\u003Cdiv class=\u0022t-col1\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003EJun 05\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col2\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003E08:41 PM\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col3\u0022\u003E\n\t\t\t\t\t\t\t\u003Cp class=\u0022t-normal\u0022\u003E\n\u003Ca href=\u0022https:\/\/plus.efxnews.com\/app.php\/orders?orders%5Btype%5D=cp\u0026orders%5Bselection%5D=AUD\/CAD\u0022\u003EAUD\/CAD\u003C\/a\u003E - Morgan Stanley - SHORT Position - Opened - Entry: 1.0085, Target: 0.9750, Stop: 1.0170 (TOTW-S\/T)\n\t\t\t\t\t\t\t\u003C\/p\u003E\n\t\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\t\u003Cdiv data-item=\u00221\u0022 class=\u0022t-notification-row item\u0022\u003E\n\t\t\t\t\t\t\t\t\t\t\t\t\u003Cdiv class=\u0022t-col1\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003EJun 05\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col2\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003E12:31 PM\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col3\u0022\u003E\n\t\t\t\t\t\t\t\u003Cp class=\u0022t-normal\u0022\u003E\n\u003Ca href=\u0022https:\/\/plus.efxnews.com\/app.php\/orders?orders%5Btype%5D=cp\u0026orders%5Bselection%5D=EUR\/USD\u0022\u003EEUR\/USD\u003C\/a\u003E - Nomura - LONG  Position - From 1.0845 - Adjusted - Stop from 1.0950 to 1.1000, Target: unch.\n\t\t\t\t\t\t\t\u003C\/p\u003E\n\t\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\t\u003Cdiv data-item=\u00221\u0022 class=\u0022t-notification-row item\u0022\u003E\n\t\t\t\t\t\t\t\t\t\t\t\t\u003Cdiv class=\u0022t-col1\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003EJun 05\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col2\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003E10:10 AM\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col3\u0022\u003E\n\t\t\t\t\t\t\t\u003Cp class=\u0022t-normal\u0022\u003E\n\u003Ca href=\u0022https:\/\/plus.efxnews.com\/app.php\/orders?orders%5Btype%5D=cp\u0026orders%5Bselection%5D=AUD\/USD\u0022\u003EAUD\/USD\u003C\/a\u003E - UOB - SHORT Position - From 0.7385 - Stopped out at 0.7455 (S\/T)\n \u003Cspan class=\u0022textLoss\u0022\u003E-70 pips\u003C\/span\u003E\t\u003Ca href=\u0022\/app.php\/order_details?order=0d15b11b7c84e4bdee3e874c7c45b9b0\u0022 title=\u0022Trade Details\u0022\u003EDetails\u003C\/a\u003E\n\t\t\t\t\t\t\t\u003C\/p\u003E\n\t\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\t\u003Cdiv data-item=\u00221\u0022 class=\u0022t-notification-row item\u0022\u003E\n\t\t\t\t\t\t\t\t\t\t\t\t\u003Cdiv class=\u0022t-col1\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003EJun 03\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col2\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003E04:32 AM\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col3\u0022\u003E\n\t\t\t\t\t\t\t\u003Cp class=\u0022t-normal\u0022\u003E\n\u003Ca href=\u0022https:\/\/plus.efxnews.com\/app.php\/orders?orders%5Btype%5D=cp\u0026orders%5Bselection%5D=EUR\/JPY\u0022\u003EEUR\/JPY\u003C\/a\u003E - BNP Paribas - SHORT Limit Order - Placed - Entry: 125.00, Target: 120.00, Stop: 127.00 (M\/T)\n\t\t\t\t\t\t\t\u003C\/p\u003E\n\t\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\t\u003Cdiv data-item=\u00221\u0022 class=\u0022t-notification-row item\u0022\u003E\n\t\t\t\t\t\t\t\t\t\t\t\t\u003Cdiv class=\u0022t-col1\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003EJun 02\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col2\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003E11:19 AM\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col3\u0022\u003E\n\t\t\t\t\t\t\t\u003Cp class=\u0022t-normal\u0022\u003E\n\u003Ca href=\u0022https:\/\/plus.efxnews.com\/app.php\/orders?orders%5Btype%5D=cp\u0026orders%5Bselection%5D=AUD\/USD\u0022\u003EAUD\/USD\u003C\/a\u003E - UOB - SHORT Position - Opened - Entry: 0.7385, Target: 0.7260, Stop: 0.7455 (S\/T)\n\t\t\t\t\t\t\t\u003C\/p\u003E\n\t\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\t\u003Cdiv data-item=\u00221\u0022 class=\u0022t-notification-row item\u0022\u003E\n\t\t\t\t\t\t\t\t\t\t\t\t\u003Cdiv class=\u0022t-col1\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003EJun 02\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col2\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003E08:12 AM\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col3\u0022\u003E\n\t\t\t\t\t\t\t\u003Cp class=\u0022t-normal\u0022\u003E\n\u003Ca href=\u0022https:\/\/plus.efxnews.com\/app.php\/orders?orders%5Btype%5D=cp\u0026orders%5Bselection%5D=EUR\/JPY\u0022\u003EEUR\/JPY\u003C\/a\u003E - Morgan Stanley - LONG Position - From 125.15 - Closed at 125.15 (TOTW-M\/T)\n \u003Cspan class=\u0022textProfit\u0022\u003E\u0026plusmn;0 pips\u003C\/span\u003E\t\u003Ca href=\u0022\/app.php\/order_details?order=eed76230354b1c9263158a3ac8b8f948\u0022 title=\u0022Trade Details\u0022\u003EDetails\u003C\/a\u003E\n\t\t\t\t\t\t\t\u003C\/p\u003E\n\t\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\t\u003Cdiv data-item=\u00221\u0022 class=\u0022t-notification-row item\u0022\u003E\n\t\t\t\t\t\t\t\t\t\t\t\t\u003Cdiv class=\u0022t-col1\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003EJun 02\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col2\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003E12:12 AM\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col3\u0022\u003E\n\t\t\t\t\t\t\t\u003Cp class=\u0022t-normal\u0022\u003E\n\u003Ca href=\u0022https:\/\/plus.efxnews.com\/app.php\/orders?orders%5Btype%5D=cp\u0026orders%5Bselection%5D=AUD\/NZD\u0022\u003EAUD\/NZD\u003C\/a\u003E - Cr\u00e9dit Agricole - LONG Position - Opened - Entry: 1.0460, Target: 1.0800, Stop: 1.0290 (M\/T)\n\t\t\t\t\t\t\t\u003C\/p\u003E\n\t\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\t\u003Cdiv data-item=\u00221\u0022 class=\u0022t-notification-row item\u0022\u003E\n\t\t\t\t\t\t\t\t\t\t\t\t\u003Cdiv class=\u0022t-col1\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003EJun 01\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col2\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003E09:38 PM\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col3\u0022\u003E\n\t\t\t\t\t\t\t\u003Cp class=\u0022t-normal\u0022\u003E\n\u003Ca href=\u0022https:\/\/plus.efxnews.com\/app.php\/orders?orders%5Btype%5D=cp\u0026orders%5Bselection%5D=EUR\/GBP\u0022\u003EEUR\/GBP\u003C\/a\u003E - Barclays - SHORT Stop Order - Filled - Entry: 0.8710 - Target: 0.8314, Stop: 0.8854 (M\/T)\n\t\t\t\t\t\t\t\u003C\/p\u003E\n\t\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\t\u003Cdiv data-item=\u00221\u0022 class=\u0022t-notification-row item\u0022\u003E\n\t\t\t\t\t\t\t\t\t\t\t\t\u003Cdiv class=\u0022t-col1\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003EJun 01\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col2\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003E08:15 PM\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col3\u0022\u003E\n\t\t\t\t\t\t\t\u003Cp class=\u0022t-normal\u0022\u003E\n\u003Ca href=\u0022https:\/\/plus.efxnews.com\/app.php\/orders?orders%5Btype%5D=cp\u0026orders%5Bselection%5D=AUD\/USD\u0022\u003EAUD\/USD\u003C\/a\u003E - Credit Suisse - LONG Position - From 0.7435 - Stopped out at 0.7380 (S\/T)\n \u003Cspan class=\u0022textLoss\u0022\u003E-55 pips\u003C\/span\u003E\t\u003Ca href=\u0022\/app.php\/order_details?order=4b51a05fec90d7aa3c9fa6a261661d96\u0022 title=\u0022Trade Details\u0022\u003EDetails\u003C\/a\u003E\n\t\t\t\t\t\t\t\u003C\/p\u003E\n\t\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\t\u003Cdiv data-item=\u00221\u0022 class=\u0022t-notification-row item\u0022\u003E\n\t\t\t\t\t\t\t\t\t\t\t\t\u003Cdiv class=\u0022t-col1\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003EJun 01\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col2\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003E01:01 PM\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col3\u0022\u003E\n\t\t\t\t\t\t\t\u003Cp class=\u0022t-normal\u0022\u003E\n\u003Ca href=\u0022https:\/\/plus.efxnews.com\/app.php\/orders?orders%5Btype%5D=cp\u0026orders%5Bselection%5D=EUR\/GBP\u0022\u003EEUR\/GBP\u003C\/a\u003E - Barclays - SHORT Stop Order - Placed - Entry: 0.8710, Target: 0.8314, Stop: 0.8854 (M\/T)\n\t\t\t\t\t\t\t\u003C\/p\u003E\n\t\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\t\u003Cdiv data-item=\u00221\u0022 class=\u0022t-notification-row item\u0022\u003E\n\t\t\t\t\t\t\t\t\t\t\t\t\u003Cdiv class=\u0022t-col1\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003EMay 31\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col2\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003E11:39 PM\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col3\u0022\u003E\n\t\t\t\t\t\t\t\u003Cp class=\u0022t-normal\u0022\u003E\n\u003Ca href=\u0022https:\/\/plus.efxnews.com\/app.php\/orders?orders%5Btype%5D=cp\u0026orders%5Bselection%5D=EUR\/USD\u0022\u003EEUR\/USD\u003C\/a\u003E - Danske - SHORT Stop Order - Placed - Entry: 1.1167, Target: 1.0850, Stop: 1.1350 (M\/T)\n\t\t\t\t\t\t\t\u003C\/p\u003E\n\t\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\t\u003Cdiv data-item=\u00221\u0022 class=\u0022t-notification-row item\u0022\u003E\n\t\t\t\t\t\t\t\t\t\t\t\t\u003Cdiv class=\u0022t-col1\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003EMay 31\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col2\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003E09:50 PM\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col3\u0022\u003E\n\t\t\t\t\t\t\t\u003Cp class=\u0022t-normal\u0022\u003E\n\u003Ca href=\u0022https:\/\/plus.efxnews.com\/app.php\/orders?orders%5Btype%5D=cp\u0026orders%5Bselection%5D=USD\/CHF\u0022\u003EUSD\/CHF\u003C\/a\u003E - Credit Suisse - LONG Position - From 0.9735 - Stopped out at 0.9691 (S\/T)\n \u003Cspan class=\u0022textLoss\u0022\u003E-44 pips\u003C\/span\u003E\t\u003Ca href=\u0022\/app.php\/order_details?order=bc747b1d7aecedca51bb25831978e71d\u0022 title=\u0022Trade Details\u0022\u003EDetails\u003C\/a\u003E\n\t\t\t\t\t\t\t\u003C\/p\u003E\n\t\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\t\u003Cdiv data-item=\u00221\u0022 class=\u0022t-notification-row item\u0022\u003E\n\t\t\t\t\t\t\t\t\t\t\t\t\u003Cdiv class=\u0022t-col1\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003EMay 31\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col2\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003E12:02 PM\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col3\u0022\u003E\n\t\t\t\t\t\t\t\u003Cp class=\u0022t-normal\u0022\u003E\n\u003Ca href=\u0022https:\/\/plus.efxnews.com\/app.php\/orders?orders%5Btype%5D=cp\u0026orders%5Bselection%5D=EUR\/USD\u0022\u003EEUR\/USD\u003C\/a\u003E - Cr\u00e9dit Agricole - SHORT Stop Order - Placed - Entry: 1.1130, Target: 1.0700, Stop: 1.1320 (M\/T)\n\t\t\t\t\t\t\t\u003C\/p\u003E\n\t\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\t\u003Cdiv data-item=\u00221\u0022 class=\u0022t-notification-row item\u0022\u003E\n\t\t\t\t\t\t\t\t\t\t\t\t\u003Cdiv class=\u0022t-col1\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003EMay 31\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col2\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003E05:03 AM\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col3\u0022\u003E\n\t\t\t\t\t\t\t\u003Cp class=\u0022t-normal\u0022\u003E\n\u003Ca href=\u0022https:\/\/plus.efxnews.com\/app.php\/orders?orders%5Btype%5D=cp\u0026orders%5Bselection%5D=USD\/CAD\u0022\u003EUSD\/CAD\u003C\/a\u003E - TD Bank - SHORT  Position - From 1.3700 - Adjusted - Stop from 1.3700 to 1.3600, Target: unch. (M\/T)\n\t\t\t\t\t\t\t\u003C\/p\u003E\n\t\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\t\u003Cdiv data-item=\u00221\u0022 class=\u0022t-notification-row item\u0022\u003E\n\t\t\t\t\t\t\t\t\t\t\t\t\u003Cdiv class=\u0022t-col1\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003EMay 30\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col2\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003E11:25 PM\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col3\u0022\u003E\n\t\t\t\t\t\t\t\u003Cp class=\u0022t-normal\u0022\u003E\n\u003Ca href=\u0022https:\/\/plus.efxnews.com\/app.php\/orders?orders%5Btype%5D=cp\u0026orders%5Bselection%5D=NZD\/USD\u0022\u003ENZD\/USD\u003C\/a\u003E - UOB - LONG Position - From 0.7000 - Hit Target at 0.7090 (S\/T)\n \u003Cspan class=\u0022textProfit\u0022\u003E+90 pips\u003C\/span\u003E\t\u003Ca href=\u0022\/app.php\/order_details?order=900b85e195ea4450304fbb69776ae148\u0022 title=\u0022Trade Details\u0022\u003EDetails\u003C\/a\u003E\n\t\t\t\t\t\t\t\u003C\/p\u003E\n\t\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\t\u003Cdiv data-item=\u00221\u0022 class=\u0022t-notification-row item\u0022\u003E\n\t\t\t\t\t\t\t\t\t\t\t\t\u003Cdiv class=\u0022t-col1\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003EMay 30\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col2\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003E11:25 PM\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col3\u0022\u003E\n\t\t\t\t\t\t\t\u003Cp class=\u0022t-normal\u0022\u003E\n\u003Ca href=\u0022https:\/\/plus.efxnews.com\/app.php\/orders?orders%5Btype%5D=cp\u0026orders%5Bselection%5D=NZD\/USD\u0022\u003ENZD\/USD\u003C\/a\u003E - Credit Suisse - LONG Limit Order - Canceled - Entry: 0.6975, Target: 0.7090, Stop: 0.6918 (S\/T)\n\t\t\t\t\t\t\t\u003C\/p\u003E\n\t\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\t\u003Cdiv data-item=\u00221\u0022 class=\u0022t-notification-row item\u0022\u003E\n\t\t\t\t\t\t\t\t\t\t\t\t\u003Cdiv class=\u0022t-col1\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003EMay 30\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col2\u0022\u003E\u003Cspan class=\u0022t-date\u0022\u003E12:18 PM\u003C\/span\u003E\u003C\/div\u003E\u003Cdiv class=\u0022t-col3\u0022\u003E\n\t\t\t\t\t\t\t\u003Cp class=\u0022t-normal\u0022\u003E\n\u003Ca href=\u0022https:\/\/plus.efxnews.com\/app.php\/orders?orders%5Btype%5D=cp\u0026orders%5Bselection%5D=EUR\/JPY\u0022\u003EEUR\/JPY\u003C\/a\u003E - Morgan Stanley - LONG  Position - From 125.15 - Adjusted - Target from 130.00 to 125.15, Stop: unch. (TOTW-M\/T)\n\t\t\t\t\t\t\t\u003C\/p\u003E\n\t\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\t\u003C\/div\u003E\n\t\t\t\t\u003C\/div\u003E\n\u003C\/div\u003E","updateDate":"8:47:37 PM"}

tmap = [
    (u"ABN AMRO", u"荷兰银行"),
    (u"ABN-AMRO", u"荷兰银行"),
    (u"ANZ", u"澳新银行"),
    (u"Barclays", u"巴克莱银行"),
    (u"BMO", u"加拿大蒙特利尔银行"),
    (u"BNP Paribas", u"法国巴黎银行"),
    (u"BNZ", u"新西兰银行"),
    (u"BofAML", u"美银美林"),
    (u"BTMU", u"三菱东京日联银行"),
    (u"CIBC", u"加拿大帝国商业银行"),
    (u"Citi", u"花旗银行"),
    (u"Commerzbank", u"德国商业银行"),
    (u"Credit Suisse", u"瑞信银行"),
    (u"Crédit Agricole", u"法国农信银行"),
    (u"Crédit Agricole", u"法国农信银行"),
    (u"Danske", u"丹斯克银行"),
    (u"Deutsche Bank", u"德意志银行"),
    (u"Goldman Sachs", u"高盛集团"),
    (u"JP Morgan", u"摩根大通"),
    (u"Morgan Stanley", u"摩根士丹利"),
    (u"NAB", u"澳洲国民银行"),
    (u"National Bank (CA)", u"加拿大国民银行"),
    (u"Nomura", u"野村证券"),
    (u"Nordea", u"瑞典北欧联合银行"),
    (u"Scotiabank", u"加拿大丰业银行"),
    (u"SEB", u"瑞典北欧斯安银行"),
    (u"Société Générale", u"法国兴业银行"),
    (u"TD Bank", u"道明银行"),
    (u"UniCredit", u"意大利联合信贷银行"),
    (u"UOB", u"大华银行"),
    (u"Westpac", u"西太平洋银行"),
    (u"unch.", u"不变"),
    (u"Hit Target at", u"止盈于"),
    (u"Stopped out at", u"止损于"),
    (u"Closed at market at", u"平仓"),
    (u"Closed at", u"平仓"),
    (u"SHORT Limit Order", u"空单"),
    (u"SHORT Stop Order", u"空单"),
    (u"LONG Limit Order", u"多单"),
    (u"LONG Stop Order", u"多单"),
    (u"SHORT Position", u"空单"),
    (u"SHORT  Position", u"空单"),
    (u"LONG Position", u"多单"),
    (u"LONG  Position", u"多单"),
    (u"Opened", u"开仓"),
    (u"Entry", u"入场价"),
    (u"Target", u"止盈"),

    (u"(S/T)", u"短线"),
    (u"(M/T)", u"中线"),
    (u"(L/T)", u"长线"),
    (u"(TOTW-S/T)", u"短线"),
    (u"(TOTW-M/T)", u"中线"),
    (u"(TOTW-L/T)", u"长线"),
    (u"Placed", u"挂单"),
    (u"Canceled", u"挂单取消"),
    (u"Filled", u"挂单入场"),
    (u"Adjusted", u"调整"),
    (u"Stop from", u"止损"),
    (u"Target from", u"止盈"),
    (u" to ", u" 改为 "),
    (u" From ", u" 入场价 "),
    (u"Stop", u"止损"),
]


class EFXNEWS(CrawlerAbstract):
    def get_latest_session_id(self):
        r1 = requests.post("https://plus.efxnews.com/app.php/login_check",
                           data="_username=estelle.yanting%40gmail.com&_password=huaerjie%401",
                           headers={
                               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                               'cookie': "PHPSESSID=123",
                               'content-type': "application/x-www-form-urlencoded",
                           },
                           allow_redirects=False)
        session_id = requests.utils.dict_from_cookiejar(r1.cookies).get('PHPSESSID')
        return session_id

    def get_html(self, url, sid):
        r2 = requests.post(url,
                           data="refresh=0",
                           headers={
                               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                               'cookie': "PHPSESSID={}".format(sid),
                               'content-type': "application/x-www-form-urlencoded",
                           })
        if r2.text.startswith('{'):
            html = r2.json().get('html', '<div>No Content</div>')
        else:
            html = None
        return html

    def index_page(self, response):
        res_list = []
        for real_url in ["https://plus.efxnews.com/app.php/alerts/list/week",
                         "https://plus.efxnews.com/app.php/alerts/forecast/week"]:
            error = 'NO_ERROR'
            try:
                sid = redis.get('efxnews_session_id')
                if not sid:
                    sid = self.get_latest_session_id()
                    redis.set('efxnews_session_id', sid)

                html = self.get_html(real_url, sid)

                # 如果页面失效, 重新获取sid并再抓一次
                if not html:
                    sid = self.get_latest_session_id()
                    redis.set('efxnews_session_id', sid)
                    html = self.get_html(response.url, sid)
                if not html:
                    print u"模版失效"
                    error = u"模版失效"
            except Exception as e:
                html = None
                error = str(e)
                self.logger.exception(e)

            if not html:
                pass
                self.logger.error('NO HTML')
                r = requests.post("http://120.26.99.59:8087/baoer/wscn2_send_message/",
                                  data={"abc": "123", "qwe": "123"},

                                  timeout=10)
                return []

            for item in pq(html).find('.item').items():

                tex = item.find('p.t-normal').text()
                tex = tex.replace(u'[Details]', u'').replace(u'Details', u'').strip()

                fake_url = u'{}#{}'.format(real_url, hashlib.md5(tex.encode('utf-8')).hexdigest())
                if self.deduplicator.is_url_recorded(fake_url):
                    continue

                # 翻译
                t_tex = tex
                for pair in tmap:
                    t_tex = t_tex.replace(pair[0], pair[1])

                # 加上forecast尾巴
                for tr in item('.hiddenBlock table tr').items():
                    t_tex += u'\n' + tr.text()

                res_list.append({
                    "acknowledged": True,
                    "link": fake_url,
                    "title": t_tex,
                    "content": '',
                    "labels": []
                })

                self.deduplicator.record_url_good(fake_url)

                r = requests.post("http://120.26.99.59:8087/baoer/wscn2_send_message/",
                                  data=json.dumps({
                                      "msg_to": u"eFXplus抓取机器人",
                                      "msg_body": t_tex,
                                  }),
                                  json=True,
                                  timeout=10)

        return res_list





