# pychrome

[![Build Status](https://travis-ci.org/fate0/pychrome.svg?branch=master)](https://travis-ci.org/fate0/pychrome)
[![Updates](https://pyup.io/repos/github/fate0/pychrome/shield.svg)](https://pyup.io/repos/github/fate0/pychrome/)
[![PyPI](https://img.shields.io/pypi/v/pychrome.svg)](https://pypi.python.org/pypi/pychrome)
[![PyPI](https://img.shields.io/pypi/pyversions/pychrome.svg)](https://pypi.python.org/pypi/pychrome)

A Python Package for the Google Chrome Dev Protocol

## Table of Contents

* [Installation](#installation)
* [Setup Chrome](#setup-chrome)
* [Getting Started](#getting-started)
* [API](#api)
* [Tab management](#tab-management)
* [Examples](#examples)
* [Ref](#ref)


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

## Setup Chrome

simply:

```
$ google-chrome --remote-debugging-port=9222
```

or headless mode (chrome version >= 59):

```
$ google-chrome --headless --disable-gpu --remote-debugging-port=9222
```

or use docker:

```
$ docker pull fate0/headless-chrome
$ docker run -it --rm --cap-add=SYS_ADMIN -p9222:9222 fate0/headless-chrome
```

## Getting Started

``` python
# create a browser instance
browser = pychrome.Browser(url="http://127.0.0.1:9222")

# list all tabs (default has a blank tab)
tabs = browser.list_tab()

if not tabs:
    tab = browser.new_tab()
else:
    tab = tabs[0]


# register callback if you want
def request_will_be_sent(**kwargs):
    print("loading: %s" % kwargs.get('request').get('url'))

tab.Network.requestWillBeSent = request_will_be_sent

# start handle events and ready to call method
tab.start()

# call method
tab.Network.enable()
# call method with timeout
tab.Page.navigate(url="https://github.com/fate0/pychrome", _timeout=5)

# 6. wait for loading
tab.wait(5)

# 7. stop tab (stop handle events and stop recv message from chrome)
tab.stop()

# 8. close tab
browser.close_tab(tab)

```

or (alternate syntax)

``` python
browser = pychrome.Browser(url="http://127.0.0.1:9222")

tabs = browser.list_tab()
if not tabs:
    tab = browser.new_tab()
else:
    tab = tabs[0]


def request_will_be_sent(**kwargs):
    print("loading: %s" % kwargs.get('request').get('url'))


tab.set_listener("Network.requestWillBeSent", request_will_be_sent)

tab.start()
tab.call_method("Network.enable")
tab.call_method("Page.navigate", url="https://github.com/fate0/pychrome", _timeout=5)

tab.wait(5)
tab.stop()

browser.close_tab(tab)
```

more methods or events could be found in
[Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/tot/)

## API

### Browser

``` python
Browser.new_tab(self, url=None, timeout=None)

Browser.list_tab(self, timeout=None)

Browser.activate_tab(self, tab_id, timeout=None)

Browser.close_tab(self, tab_id, timeout=None)

Browser.version(self, timeout=None):
```

### Tab

``` python

Tab.start()
"""
return None
raise RuntimeException
"""

Tab.stop()
"""
return None
raise RuntimeException
"""

# when you call Tab.Page.navigate or something else, actually you are calling Tab.call_method
Tab.call_method(self, _method, *args, **kwargs)
"""
return dict
raise CallMethodException, RuntimeException, TimeoutException, UserAbortException
"""

# when you set/del event listener, you are calling Tab.set_listener
Tab.set_listener(self, event, callback)
"""
return bool
raise RuntimeException
"""

Tab.get_listener(self, event)
"""
return func, None
"""

Tab.del_all_listeners(self)
"""
return None
"""

Tab.wait(self, timeout=None)
"""
return bool
"""
```

## Tab management

run `pychrome -h` for more info

example:
```
$ pychrome new http://www.fatezero.org
{
    "description": "",
    "url": "http://www.fatezero.org/",
    "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools/page/557d8315-e909-466c-bf20-f5a6133ebd89",
    "id": "557d8315-e909-466c-bf20-f5a6133ebd89",
    "type": "page",
    "devtoolsFrontendUrl": "/devtools/inspector.html?ws=127.0.0.1:9222/devtools/page/557d8315-e909-466c-bf20-f5a6133ebd89",
    "title": ""
}

$ pychrome close 557d8315-e909-466c-bf20-f5a6133ebd89
Target is closing
```

## Examples

please see the [examples](http://github.com/fate0/pychrome/blob/master/examples) directory for more examples


## Ref

* [chrome-remote-interface](https://github.com/cyrus-and/chrome-remote-interface/)
* [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/tot/)
