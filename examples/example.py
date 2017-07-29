#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pychrome


# 1. create a browser instance
browser = pychrome.Browser(url="http://127.0.0.1:9222")

# 2. list all tabs (default has a blank tab)
tabs = browser.list_tab()

if not tabs:
    tab = browser.new_tab()
else:
    tab = tabs[0]


# 3. register callback if you want
def request_will_be_sent(**kwargs):
    print("loading: %s" % kwargs.get('request').get('url'))

tab.Network.requestWillBeSent = request_will_be_sent

# 4. start handle events and ready to call method
tab.start()

# 5. call methods
tab.Network.enable()
tab.Page.navigate(url="https://github.com/fate0/pychrome")

# 6. wait for loading
tab.wait(5)

# 7. stop tab (stop handle events and stop recv message from chrome)
tab.stop()

# 8. close tab
browser.close_tab(tab)
