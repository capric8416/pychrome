#! /usr/bin/env python
# -*- coding: utf-8 -*-


import time
import pychrome


class EventHandler(object):
    def __init__(self, chrome, tab):
        self.chrome = chrome
        self.tab = tab
        self.start_frame = None
        self.is_first_request = True
        self.html_content = None

    def frame_started_loading(self, frameId):
        if not self.start_frame:
            self.start_frame = frameId

    def request_intercepted(self, interceptionId, request, **kwargs):
        if self.is_first_request:
            headers = request.get('headers', {})
            headers['Test-key'] = 'test-value'
            self.tab.Network.continueInterceptedRequest(
                interceptionId=interceptionId,
                headers=headers,
                method='POST',
                postData="hello post data: %s" % time.time()
            )
        else:
            self.tab.Network.continueInterceptedRequest(
                interceptionId=interceptionId
            )

    def frame_stopped_loading(self, frameId):
        if self.start_frame == frameId:
            self.tab.Page.stopLoading()
            result = self.tab.Runtime.evaluate(expression="document.documentElement.outerHTML")
            self.html_content = result.get('result', {}).get('value', "")
            print(self.html_content)
            self.tab.stop()


def main():
    browser = pychrome.Browser()

    tabs = []
    for i in range(4):
        tabs.append(browser.new_tab())

    for i, tab in enumerate(tabs):
        eh = EventHandler(browser, tab)
        tab.Network.requestIntercepted = eh.request_intercepted
        tab.Page.frameStartedLoading = eh.frame_started_loading
        tab.Page.frameStoppedLoading = eh.frame_stopped_loading

        tab.start()
        tab.Page.stopLoading()
        tab.Page.enable()
        tab.Network.setRequestInterceptionEnabled(enabled=True)
        tab.Page.navigate(url="http://httpbin.org/post")

    for tab in tabs:
        tab.wait(60)
        browser.close_tab(tab.id)

    print('Done')


if __name__ == '__main__':
    main()
