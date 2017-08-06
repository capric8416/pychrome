# -*- coding: utf-8 -*-
# !/usr/bin/env python

import logging

from pychrome import Sniffer

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    sniffer = Sniffer()
    sniffer.open_url(url='https://shop34135992.m.taobao.com/#list?q=韩')
