# pychrome

[![Build Status](https://travis-ci.org/fate0/pychrome.svg?branch=master)](https://travis-ci.org/fate0/pychrome)
[![Updates](https://pyup.io/repos/github/fate0/pychrome/shield.svg)](https://pyup.io/repos/github/fate0/pychrome/)
[![PyPI](https://img.shields.io/pypi/v/pychrome.svg)](https://pypi.python.org/pypi/pychrome)
[![PyPI](https://img.shields.io/pypi/pyversions/pychrome.svg)](https://pypi.python.org/pypi/pychrome)

A Python Package for the Google Chrome Dev Protocol


## Installation

To install pychrome, simply:

```
$ pip install -U git+https://github.com/fate0/pychrome.git
```

or from pypi:

```
$ pip install -U pychrome
```

or from source:

```
$ python setup.py install
```

## Getting Started

``` python
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

```


## Examples





## Ref

* [chrome-remote-interface](https://github.com/cyrus-and/chrome-remote-interface/)
* [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/tot/)
