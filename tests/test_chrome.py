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


def teardown_function(function):
    chrome = pychrome.Chrome()
    close_all_tabs(chrome)


def test_chome_version():
    chrome = pychrome.Chrome()
    chrome_version = chrome.version()


def test_chrome_list():
    chrome = pychrome.Chrome()
    chrome.list_tab()


def test_chrome_new():
    chrome = pychrome.Chrome()
    tab = chrome.new_tab()


def test_chrome_new_10_tabs():
    chrome = pychrome.Chrome()
    tabs = []
    for i in range(10):
        tabs.append(chrome.new_tab())

    time.sleep(1)
    assert len(chrome.list_tab()) == 10

    for tab in tabs:
        chrome.close_tab(tab.id)

    time.sleep(1)
    assert len(chrome.list_tab()) == 0


def test_chrome_new_100_tabs():
    chrome = pychrome.Chrome()
    tabs = []
    for i in range(100):
        tabs.append(chrome.new_tab())

    time.sleep(1)
    assert len(chrome.list_tab()) == 100

    for tab in tabs:
        chrome.close_tab(tab.id)

    time.sleep(1)
    assert len(chrome.list_tab()) == 0
