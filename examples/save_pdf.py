#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import base64
import pychrome

import gevent.lock


urls = [
    "http://fatezero.org",
    "http://blog.fatezero.org",
    "http://github.com/fate0",
    "https://www.zhihu.com/people/fatez3r0",
]


class EventHandler(object):
    pdf_lock = gevent.lock.RLock()

    def __init__(self, chrome, tab):
        self.chrome = chrome
        self.tab = tab
        self.start_frame = None

    def frame_started_loading(self, frameId):
        if not self.start_frame:
            self.start_frame = frameId

    def frame_stopped_loading(self, frameId):
        if self.start_frame == frameId:
            self.tab.Page.stopLoading()

            with self.pdf_lock:
                # must activate current tab
                print(self.chrome.activate_tab(self.tab.id))

                try:
                    data = self.tab.Page.printToPDF()

                    with open("%s.pdf" % time.time(), "wb") as fd:
                        fd.write(base64.b64decode(data['data']))
                finally:
                    self.tab.stop()


def main():
    chrome = pychrome.Chrome()

    tabs = []
    for i in range(len(urls)):
        tabs.append(chrome.new_tab())

    for i, tab in enumerate(tabs):
        eh = EventHandler(chrome, tab)
        tab.Page.frameStartedLoading = eh.frame_started_loading
        tab.Page.frameStoppedLoading = eh.frame_stopped_loading

        tab.start()
        tab.Page.stopLoading()
        tab.Page.enable()
        tab.Page.navigate(url=urls[i])

    for tab in tabs:
        tab.wait(600)
        chrome.close_tab(tab.id)

    print('Done')


if __name__ == '__main__':
    main()
