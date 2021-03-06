#! /usr/bin/env python
# -*- coding: utf-8 -*-


import logging

import requests

from .tab import Tab

__all__ = ['Browser']

logger = logging.getLogger(__name__)


class Browser(object):
    _all_tabs = {}

    def __init__(self, remote_debugging_url='http://localhost:9222'):
        self.remote_debugging_url = remote_debugging_url

        if self.remote_debugging_url not in self._all_tabs:
            self._tabs = self._all_tabs[self.remote_debugging_url] = {}
        else:
            self._tabs = self._all_tabs[self.remote_debugging_url]

    def new_tab(self, url=None, timeout=None):
        url = url or ''
        resp = requests.get(f'{self.remote_debugging_url}/json/new?{url}', json=True, timeout=timeout)
        tab = Tab(**resp.json())
        self._tabs[tab._id] = tab
        return tab

    def activate_tab(self, tab_id, timeout=None):
        _ = self

        if isinstance(tab_id, Tab):
            tab_id = tab_id._id

        resp = requests.get(f'{self.remote_debugging_url}/json/activate/{tab_id}', timeout=timeout)
        return resp.text

    def close_tab(self, tab_id, timeout=None):
        if isinstance(tab_id, Tab):
            tab_id = tab_id._id

        resp = requests.get(f'{self.remote_debugging_url}/json/close/{tab_id}', timeout=timeout)
        self._tabs.pop(tab_id, None)
        return resp.text

    def get_all_tabs(self, timeout=None):
        resp = requests.get(f'{self.remote_debugging_url}/json', json=True, timeout=timeout)
        tabs_map = {}
        for tab_json in resp.json():
            if tab_json['type'] != 'page':
                continue

            if tab_json['id'] in self._tabs and self._tabs[tab_json['id']].status() != Tab.status_stopped:
                tabs_map[tab_json['id']] = self._tabs[tab_json['id']]
            else:
                tabs_map[tab_json['id']] = Tab(**tab_json)

        self._tabs = tabs_map
        return list(self._tabs.values())

    def get_one_tab(self):
        tabs = self.get_all_tabs()

        if not tabs:
            tab = self.new_tab()
        else:
            tab = tabs[0]

        return tab

    def version(self, timeout=None):
        _ = self

        resp = requests.get(f'{self.remote_debugging_url}/json/version', json=True, timeout=timeout)
        return resp.json()

    def __str__(self):
        return f'<Browser {self.remote_debugging_url}>'

    __repr__ = __str__
