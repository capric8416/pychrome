# pychrome

A Python Package for the Google Chrome DevTools Protocol


## Table of Contents

* [Installation](#installation)
* [Launch Chrome](#launch-chrome)
* [References](#references)


## Installation

```bash
# from github
pip install --upgrade git+https://github.com/capric8416/pychrome.git

# or from source
python setup.py install
```


## Launch Chrome

```bash
# normal mode
google-chrome --remote-debugging-port=9222

# or headless mode (chrome version >= 61)
google-chrome --remote-debugging-port=9222 --headless --disable-gpu
```


## References
* [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/tot/)
* [chrome-remote-interface](https://github.com/cyrus-and/chrome-remote-interface/)

