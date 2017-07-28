#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import functools
import threading

import requests
import websocket

try:
    import Queue as queue
except ImportError:
    import queue

try:
    import simplejson as json
except ImportError:
    import json


logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)


__all__ = ["Chrome", "Tab"]


class ChromeCallMethodException(Exception):
    pass


class ChromeTimeoutException(Exception):
    pass


class GenericAttr(object):
    def __init__(self, name, tab):
        self.__dict__['name'] = name
        self.__dict__['tab'] = tab

    def __getattr__(self, item):
        return functools.partial(self.tab.call_method, _method="%s.%s" % (self.name, item))

    def __setattr__(self, key, value):
        self.tab.event_handlers["%s.%s" % (self.name, key)] = value


class Tab(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.url = kwargs.get("url")
        self.title = kwargs.get("title")
        self.type = kwargs.get("type")
        self.websocket_url = kwargs.get("webSocketDebuggerUrl")
        self.desc = kwargs.get("description")

        self.cur_id = 1000
        self.event_handlers = {}
        self.method_results = {}
        self.event_queue = queue.Queue()

        self.ws = None
        self.ws_send_lock = threading.RLock()

        self.recv_th = None
        self.handle_event_th = None

        self.is_stop = False

    def _send(self, message):
        timeout = message.pop('_timeout', None)

        if 'id' not in message:
            self.cur_id += 1
            message['id'] = self.cur_id

        logger.debug("[*] send message: %s %s" % (message["id"], message['method']))
        self.method_results[message['id']] = queue.Queue()

        with self.ws_send_lock:
            self.ws.send(json.dumps(message))

        try:
            return self.method_results[message['id']].get(timeout=timeout)
        except queue.Empty:
            raise ChromeTimeoutException("Send command %s timeout" % message['method'])
        finally:
            self.method_results.pop(message['id'])

    def _recv_loop(self):
        while not self.is_stop:
            try:
                self.ws.settimeout(1)
                message = json.loads(self.ws.recv())
            except websocket.WebSocketTimeoutException:
                continue
            except websocket.WebSocketConnectionClosedException:
                return

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
        while not self.is_stop:
            try:
                event = self.event_queue.get(timeout=1)
            except queue.Empty:
                continue

            if event['method'] in self.event_handlers:
                try:
                    self.event_handlers[event['method']](**event['params'])
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
            raise ChromeCallMethodException("calling method: %s error: %s" % (_method, result['error']['message']))

        return result['result']

    def set_listener(self, event, callback):
        if not callback:
            return self.event_handlers.pop(event, None)

        self.event_handlers[event] = callback
        return True

    def start(self):
        assert self.websocket_url, "has another client connect to this tab"
        assert not self.is_stop, "This tab has been working"

        self.ws = websocket.create_connection(self.websocket_url)
        self.is_stop = False

        self.recv_th = threading.Thread(target=self._recv_loop, daemon=True)
        self.handle_event_th = threading.Thread(target=self._handle_event_loop, daemon=True)
        self.recv_th.start()
        self.handle_event_th.start()

    def stop(self):
        self.is_stop = True
        self.ws.close()

    def wait(self, timeout=None):
        # TODO
        self.recv_th.join(timeout)
        self.handle_event_th.join(timeout)

    def __str__(self):
        return "<Tab [%s] %s>" % (self.id, self.url)

    __repr__ = __str__


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

    def version(self):
        rp = requests.get("%s/json/version" % self.dev_url, json=True)
        return rp.json()

    def inspect_tab(self, tab_id):
        pass

    def __str__(self):
        return '<Chrome %s>' % self.dev_url

    __repr__ = __str__
