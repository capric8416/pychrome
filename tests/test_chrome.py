# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
import pychrome


def test_chome_version():
    chrome = pychrome.Chrome()
    chrome.version()


def test_chrome_list():
    chrome = pychrome.Chrome()
    chrome.list_tab()


def test_chrome_new():
    chrome = pychrome.Chrome()
    chrome.new_tab()