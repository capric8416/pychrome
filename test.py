# -*- coding: utf-8 -*-
# !/usr/bin/env python

import logging

from pyquery import *

from pychrome import Sniffer, Launcher

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_sniffer():
    sniffer = Sniffer()

    status = sniffer.open_url(url='https://shop34135992.m.taobao.com/#list?q=韩', selector='h3.d-title')

    while True:
        html = sniffer.tab.query(selector='.goods-list-items', limit=1)
        for a in PyQuery(html)('a').items():
            print(a('h3.d-title').text())

        sniffer.tab.wait(timeout=2)

        status = sniffer.tab.click(selector='#gl-pagenav a.c-p-next:not(.c-btn-off)')
        if not status:
            break

        status = sniffer.tab.wait('h3.d-title')


def test_launcher():
    launcher = Launcher(
        chrome_path='/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary', count=1)
    launcher.start()
    launcher.stop()


def test_proxy():
    launcher = Launcher(
        chrome_path='/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary',
        extension_path='/Users/capric/pychrome/dynamic_proxy', incognito=False, headless=False, count=1)
    launcher.start()

    sniffer = Sniffer()
    status = sniffer.change_proxy(value='http://127.0.0.1:1080', scope='regular')
    status = sniffer.open_url(url='http://www.howtofindmyipaddress.com/')

    sniffer.tab.wait(timeout=1000)
    launcher.stop()



if __name__ == '__main__':
    # test_launcher()
    # test_sniffer()
    test_proxy()
