#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import gevent
import gevent.lock
import gevent.queue
import gevent.monkey

gevent.monkey.patch_socket()

import logging
import functools

import requests
import websocket

try:
    import simplejson as json
except ImportError:
    import json


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


__all__ = ["Chrome", "Tab"]


class ChromeException(Exception):
    pass


class GenericAttr(object):
    def __init__(self, name, tab):
        self.__dict__['name'] = name
        self.__dict__['tab'] = tab

    def __getattr__(self, item):
        return functools.partial(self.tab.call_method, _method="%s.%s" % (self.name, item))

    def __setattr__(self, key, value):
        self.tab.events["%s.%s" % (self.name, key)] = value


class Tab(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.url = kwargs.get("url")
        self.title = kwargs.get("title")
        self.type = kwargs.get("type")
        self.websocket_url = kwargs.get("webSocketDebuggerUrl")
        self.desc = kwargs.get("description")

        self.timeout = kwargs.pop("timeout", 5)

        self.cur_id = 1000
        self.events = {}
        self.method_results = {}
        self.event_queue = gevent.queue.Queue()
        self.ws = None
        self.ws_send_lock = gevent.lock.RLock()

        self.recv_gr = None
        self.handle_event_gr = None

    def _send(self, message):
        if 'id' not in message:
            self.cur_id += 1
            message['id'] = self.cur_id

        logger.debug("[*] send message: %s %s" % (message["id"], message['method']))
        self.method_results[message['id']] = gevent.queue.Queue()

        with self.ws_send_lock:
            self.ws.send(json.dumps(message))

        try:
            return self.method_results[message['id']].get()
        finally:
            self.method_results.pop(message['id'])

    def _recv_loop(self):
        while True:
            try:
                message = json.loads(self.ws.recv())
            except websocket.WebSocketTimeoutException:
                continue

            if "method" in message:
                logger.debug("[*] recv event: %s" % message["method"])
                self.event_queue.put(message)

            elif "id" in message:
                logger.debug("[*] recv message: %s" % message["id"])
                if message["id"] in self.method_results:
                    self.method_results[message['id']].put(message)
            else:
                logger.warning("[-] unknown message: %s" % message)

    def _handle_event_loop(self):
        while True:
            try:
                event = self.event_queue.get(timeout=self.timeout)
            except gevent.queue.Empty:
                continue

            if event['method'] in self.events:
                try:
                    self.events[event['method']](**event['params'])
                except Exception as e:
                    logger.error("[-] callback %s error: %s" % (event['method'], str(e)))

    def __getattr__(self, item):
        attr = GenericAttr(item, self)
        setattr(self, item, attr)
        return attr

    def call_method(self, _method, **kwargs):
        result = self._send({"method": _method, "params": kwargs})
        if 'result' not in result and 'error' in result:
            logger.error("[-] %s error: %s" % (_method, result['error']['message']))
            raise ChromeException(result['error']['message'])

        return result['result']

    def set_listener(self, event, callback):
        if not callback:
            return self.events.pop(event, None)

        self.events[event] = callback
        return True

    def start(self):
        assert self.websocket_url, "has another client connect to this tab"

        self.ws = websocket.create_connection(self.websocket_url)
        self.ws.settimeout(self.timeout)
        self.recv_gr = gevent.spawn(self._recv_loop)
        self.handle_event_gr = gevent.spawn(self._handle_event_loop)

    def stop(self):
        self.recv_gr.kill()
        self.handle_event_gr.kill()
        self.ws.close()

    def wait(self, timeout=None):
        gevent.wait([self.recv_gr, self.handle_event_gr], timeout=timeout)


class Chrome(object):
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
        rp = requests.get("%s/json/activate/%s" % (self.dev_url, tab_id))
        return rp.text

    def close_tab(self, tab_id):
        rp = requests.get("%s/json/close/%s" % (self.dev_url, tab_id))
        self.tabs.pop(tab_id, None)
        return rp.text

    def inspect_tab(self, tab_id):
        pass

    def version(self):
        pass
