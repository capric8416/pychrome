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


def test_normal_callmethod():
    chrome = pychrome.Chrome()
    tab = chrome.new_tab()

    tab.start()
    result = tab.Page.navigate(url="http://www.fatezero.org")
    assert result['frameId']

    result = tab.Runtime.evaluate(expression="document.domain")

    time.sleep(1)
    assert result['result']['type'] == 'string'
    assert result['result']['value'] == 'www.fatezero.org'


def test_invalid_method():
    chrome = pychrome.Chrome()
    tab = chrome.new_tab()

    tab.start()
    try:
        tab.Page.NotExistMethod()
        assert 0, "should not run to this"
    except pychrome.ChromeCallMethodException as e:
        pass


def test_invalid_params():
    chrome = pychrome.Chrome()
    tab = chrome.new_tab()

    tab.start()
    try:
        tab.Page.navigate()
        assert 0, "should not run to this"
    except pychrome.ChromeCallMethodException as e:
        pass

    try:
        tab.Page.navigate("http://fatezero.org")
        assert 0, "should not run to this"
    except pychrome.ChromeCallMethodException as e:
        pass

    try:
        tab.Page.navigate(invalid_params="http://fatezero.org")
        assert 0, "should not run to this"
    except pychrome.ChromeCallMethodException as e:
        pass

    try:
        tab.Page.navigate(url="http://fatezero.org", invalid_params=123)
    except pychrome.ChromeCallMethodException as e:
        assert 0, "should not run to this"



