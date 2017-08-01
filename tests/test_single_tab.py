# -*- coding: utf-8 -*-

import time
import logging
import pychrome

logging.basicConfig(level=logging.DEBUG)


def close_all_tabs(browser):
    if len(browser.list_tab()) == 0:
        return

    logging.debug("[*] recycle")
    for tab in browser.list_tab():
        try:
            tab.stop()
        except pychrome.RuntimeException:
            pass

        browser.close_tab(tab)

    time.sleep(1)
    assert len(browser.list_tab()) == 0


def setup_function(function):
    browser = pychrome.Browser()
    close_all_tabs(browser)


def teardown_function(function):
    browser = pychrome.Browser()
    close_all_tabs(browser)


def test_normal_callmethod():
    browser = pychrome.Browser()
    tab = browser.new_tab()

    result = tab.Page.navigate(url="http://www.fatezero.org")
    assert result['frameId']

    time.sleep(1)
    result = tab.Runtime.evaluate(expression="document.domain")

    assert result['result']['type'] == 'string'
    assert result['result']['value'] == 'www.fatezero.org'


def test_invalid_method():
    browser = pychrome.Browser()
    tab = browser.new_tab()

    try:
        tab.Page.NotExistMethod()
        assert False, "never get here"
    except pychrome.CallMethodException:
        pass


def test_invalid_params():
    browser = pychrome.Browser()
    tab = browser.new_tab()

    try:
        tab.Page.navigate()
        assert False, "never get here"
    except pychrome.CallMethodException:
        pass

    try:
        tab.Page.navigate("http://www.fatezero.org")
        assert False, "never get here"
    except pychrome.CallMethodException:
        pass

    try:
        tab.Page.navigate(invalid_params="http://www.fatezero.org")
        assert False, "never get here"
    except pychrome.CallMethodException:
        pass

    try:
        tab.Page.navigate(url="http://www.fatezero.org", invalid_params=123)
    except pychrome.CallMethodException:
        assert False, "never get here"


def test_set_event_listener():
    browser = pychrome.Browser()
    tab = browser.new_tab()

    def request_will_be_sent(**kwargs):
        tab.stop()

    tab.Network.requestWillBeSent = request_will_be_sent
    tab.Network.enable()
    try:
        tab.Page.navigate(url="chrome://newtab/")
    except pychrome.UserAbortException:
        pass

    if not tab.wait(timeout=5):
        assert False, "never get here"


def test_get_event_listener():
    browser = pychrome.Browser()
    tab = browser.new_tab()

    def request_will_be_sent(**kwargs):
        tab.stop()

    tab.Network.requestWillBeSent = request_will_be_sent
    tab.Network.enable()
    try:
        tab.Page.navigate(url="chrome://newtab/")
    except pychrome.UserAbortException:
        pass

    if not tab.wait(timeout=5):
        assert False, "never get here"

    assert tab.Network.requestWillBeSent == request_will_be_sent
    tab.Network.requestWillBeSent = None

    assert not tab.get_listener("Network.requestWillBeSent")
    # notice this
    assert tab.Network.requestWillBeSent != tab.get_listener("Network.requestWillBeSent")


def test_reuse_tab():
    browser = pychrome.Browser()
    tab = browser.new_tab()

    def request_will_be_sent(**kwargs):
        tab.stop()

    tab.Network.requestWillBeSent = request_will_be_sent
    tab.Network.enable()
    try:
        tab.Page.navigate(url="chrome://newtab/")
    except pychrome.UserAbortException:
        pass

    if not tab.wait(timeout=5):
        assert False, "never get here"

    tab = browser.list_tab()[0]
    tab.Network.enable()
    try:
        tab.Page.navigate(url="http://www.fatezero.org")
    except pychrome.UserAbortException:
        pass

    if not tab.wait(timeout=5):
        assert False, "never get here"


def test_del_event_listener():
    browser = pychrome.Browser()
    tab = browser.new_tab()

    def request_will_be_sent(**kwargs):
        tab.stop()

    tab.Network.requestWillBeSent = request_will_be_sent
    tab.Network.enable()
    try:
        tab.Page.navigate(url="chrome://newtab/")
    except pychrome.UserAbortException:
        pass

    if not tab.wait(timeout=5):
        assert False, "never get here"

    tab = browser.list_tab()[0]
    # simply set None
    tab.Network.requestWillBeSent = None
    tab.Network.enable()
    tab.Page.navigate(url="http://www.fatezero.org")

    if tab.wait(timeout=5):
        assert False, "never get here"


def test_del_all_event_listener():
    browser = pychrome.Browser()
    tab = browser.new_tab()

    def request_will_be_sent(**kwargs):
        tab.stop()

    tab.Network.requestWillBeSent = request_will_be_sent
    tab.Network.enable()
    try:
        tab.Page.navigate(url="chrome://newtab/")
    except pychrome.UserAbortException:
        pass

    if not tab.wait(timeout=5):
        assert False, "never get here"

    tab = browser.list_tab()[0]
    # delete all listener
    tab.del_all_listeners()
    tab.Network.enable()
    tab.Page.navigate(url="http://www.fatezero.org")

    if tab.wait(timeout=5):
        assert False, "never get here"


class CallableClass(object):
    def __init__(self, tab):
        self.tab = tab

    def __call__(self, *args, **kwargs):
        self.tab.stop()


def test_use_callable_class_event_listener():
    browser = pychrome.Browser()
    tab = browser.new_tab()

    tab.Network.requestWillBeSent = CallableClass(tab)
    tab.Network.enable()
    try:
        tab.Page.navigate(url="chrome://newtab/")
    except pychrome.UserAbortException:
        pass

    if not tab.wait(timeout=5):
        assert False, "never get here"

    tab = browser.list_tab()[0]
    # delete all listener
    tab.del_all_listeners()
    tab.Network.enable()
    tab.Page.navigate(url="http://www.fatezero.org")

    if tab.wait(timeout=5):
        assert False, "never get here"
