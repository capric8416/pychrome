# -*- coding: utf-8 -*-

import time
import pychrome


def close_all_tabs(chrome):
    for tab in chrome.list_tab():
        chrome.close_tab(tab.id)

    time.sleep(1)
    assert len(chrome.list_tab()) == 0


def setup_function(function):
    chrome = pychrome.Chrome()
    close_all_tabs(chrome)


def test_xxx():
    chrome = pychrome.Chrome()
    tab = chrome.new_tab()

    tab.start()
    tab.Page.navigate(url="http://httpbin.org/post")
    tab.wait(1)

    assert 1 == 0