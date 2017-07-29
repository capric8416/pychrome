#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pychrome


chrome = pychrome.Chrome()

if len(chrome.list_tab()) == 0:
    chrome.new_tab()

tab = chrome.list_tab()[0]


def frame_stopped_loading(frameId):
    tab.stop()
    print("stop")


def request_will_be_sent(**kwargs):
    print("loading: %s" % kwargs.get('request').get('url'))


tab.Page.frameStoppedLoading = frame_stopped_loading
tab.Network.requestWillBeSent = request_will_be_sent

tab.Page.enable()
tab.Network.enable()

tab.Page.navigate(url="http://www.fatezero.org")

tab.wait()
