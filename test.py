# -*- coding: utf-8 -*-
# !/usr/bin/env python

import logging

from pyquery import *

from pychrome import Sniffer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    sniffer = Sniffer()

    status = sniffer.open_url(url='https://shop34135992.m.taobao.com/#list?q=韩', selector='h3.d-title')

    while True:
        html = sniffer.tab.query(selector='.goods-list-items', limit=1)
        for a in PyQuery(html)('a').items():
            print(a('h3.d-title').text())

        status = sniffer.tab.click(selector='#gl-pagenav a.c-p-next:not(.c-btn-off)')
        if not status:
            break

        status = sniffer.tab.wait('h3.d-title')
