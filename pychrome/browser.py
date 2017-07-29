#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, with_statement

import logging
import requests

from pychrome.tab import Tab

try:
    import Queue as queue
except ImportError:
    import queue


__all__ = ["Browser"]


logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)


class Browser(object):
    def __init__(self, url="http://127.0.0.1:9222"):
        self.dev_url = url
        self.tabs = {}

    def new_tab(self, url=None):
        url = url or ''
        rp = requests.get("%s/json/new?%s" % (self.dev_url, url), json=True)
        tab = Tab(**rp.json())
        self.tabs[tab.id] = tab
        return tab

    def list_tab(self):
        rp = requests.get("%s/json" % self.dev_url, json=True)
        tabs_map = {}
        for tab_json in rp.json():
            if tab_json['type'] != 'page':
                continue

            if tab_json['id'] in self.tabs:
                tabs_map[tab_json['id']] = self.tabs[tab_json['id']]
            else:
                tabs_map[tab_json['id']] = Tab(**tab_json)

        self.tabs = tabs_map
        return list(self.tabs.values())

    def activate_tab(self, tab_id):
        if isinstance(tab_id, Tab):
            tab_id = tab_id.id

        rp = requests.get("%s/json/activate/%s" % (self.dev_url, tab_id))
        return rp.text

    def close_tab(self, tab_id):
        if isinstance(tab_id, Tab):
            tab_id = tab_id.id

        rp = requests.get("%s/json/close/%s" % (self.dev_url, tab_id))
        self.tabs.pop(tab_id, None)
        return rp.text

    def version(self):
        rp = requests.get("%s/json/version" % self.dev_url, json=True)
        return rp.json()

    def __str__(self):
        return '<Browser %s>' % self.dev_url

    __repr__ = __str__
