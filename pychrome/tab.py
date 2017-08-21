#! /usr/bin/env python
# -*- coding: utf-8 -*-


import functools
import json
import logging
import math
import queue
import threading
import time
import warnings

import websocket

from .exceptions import *

__all__ = ['Tab']

logger = logging.getLogger(__name__)


class GenericAttr(object):
    def __init__(self, name, tab):
        self.__dict__['name'] = name
        self.__dict__['tab'] = tab

    def __getattr__(self, item):
        method_name = f'{self.name}.{item}'
        event_listener = self.tab.get_listener(method_name)

        if event_listener:
            return event_listener

        return functools.partial(self.tab.call_method, method_name)

    def __setattr__(self, key, value):
        self.tab.add_listener(f'{self.name}.{key}', value)


class Tab(object):
    status_initial = 1
    status_started = 2
    status_stopped = 3

    def __init__(self, **kwargs):
        self._id = kwargs.get('id')
        self._url = kwargs.get('url')
        self._title = kwargs.get('title')
        self._type = kwargs.get('type')
        self._ws_url = kwargs.get('webSocketDebuggerUrl')
        self._description = kwargs.get('description')

        self._origin_kwargs = kwargs

        self._current_id = 1000

        self._event_handlers = {}
        self._method_results = {}

        self._event_queue = queue.Queue()

        self._ws = None
        self._ws_send_lock = threading.Lock()

        self._receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
        self._handle_event_thread = threading.Thread(target=self._handle_event_loop, daemon=True)

        self._stopped = threading.Event()
        self._started = threading.Event()

    def _init(self):
        if self._started.is_set():
            return

        if not self._ws_url:
            raise RuntimeException('Already has another client connect to this tab')

        self._started.set()
        self._stopped.clear()

        self._ws = websocket.create_connection(self._ws_url)

        self._receive_thread.start()
        self._handle_event_thread.start()

    def _send(self, message, timeout=None):
        if 'id' not in message:
            self._current_id += 1
            message['id'] = self._current_id

        logger.debug(f'[*] send message: {message["id"]} {message["method"]}')
        self._method_results[message['id']] = queue.Queue()

        with self._ws_send_lock:
            self._ws.send(json.dumps(message))

        if not isinstance(timeout, (int, float)) or timeout > 1:
            q_timeout = 1
        else:
            q_timeout = timeout / 2.0

        try:
            while not self._stopped.is_set():
                try:
                    if isinstance(timeout, (int, float)):
                        if timeout < q_timeout:
                            q_timeout = timeout

                        timeout -= q_timeout

                    return self._method_results[message['id']].get(timeout=q_timeout)
                except queue.Empty:
                    if isinstance(timeout, (int, float)) and timeout <= 0:
                        raise TimeoutException(f'Calling {message["method"]} timeout')

                    continue

            raise UserAbortException(f'User abort, call stop() when calling {message["method"]}')
        finally:
            self._method_results.pop(message['id'], None)

    def _receive_loop(self):
        while not self._stopped.is_set():
            try:
                self._ws.settimeout(1)
                message = json.loads(self._ws.recv())
            except websocket.WebSocketTimeoutException:
                continue
            except (websocket.WebSocketConnectionClosedException, OSError):
                return

            if 'method' in message:
                logger.debug(f'[*] receive event: {message["method"]}')
                self._event_queue.put(message)

            elif 'id' in message:
                logger.debug(f'[*] receive message: {message["id"]}')
                if message['id'] in self._method_results:
                    self._method_results[message['id']].put(message)
            else:
                logger.warning(f'[-] unknown message: {message}')

    def _handle_event_loop(self):
        while not self._stopped.is_set():
            try:
                event = self._event_queue.get(timeout=1)
            except queue.Empty:
                continue

            if event['method'] in self._event_handlers:
                try:
                    self._event_handlers[event['method']](**event['params'])
                except Exception as e:
                    logger.exception(f'[-] callback {event["method"]} error: {e}')

    def __getattr__(self, item):
        attr = GenericAttr(item, self)
        setattr(self, item, attr)
        return attr

    def call_method(self, _method, *args, **kwargs):
        if args:
            raise CallMethodException('the params should be key=value format')

        if self._stopped.is_set():
            raise RuntimeException('Tab has been stopped')

        self._init()
        timeout = kwargs.pop('_timeout', None)
        result = self._send({'method': _method, 'params': kwargs}, timeout=timeout)
        if 'result' not in result and 'error' in result:
            logger.error(f'[-] {_method} error: {result["error"]["message"]}')
            raise CallMethodException(f'calling method: {_method} error: {result["error"]["message"]}')

        return result['result']

    def add_listener(self, event, callback):
        if not callback:
            return self._event_handlers.pop(event, None)

        if not callable(callback):
            raise RuntimeException('callback should be callable')

        self._event_handlers[event] = callback
        return True

    def get_listener(self, event):
        return self._event_handlers.get(event, None)

    def remove_listener(self, event):
        try:
            del self._event_handlers[event]
        except KeyError:
            return False
        return True

    def remove_all_listeners(self):
        self._event_handlers = {}
        return True

    def status(self):
        if not self._started.is_set() and not self._stopped.is_set():
            return Tab.status_initial
        if self._started.is_set() and not self._stopped.is_set():
            return Tab.status_started
        if self._started.is_set() and self._stopped.is_set():
            return Tab.status_stopped
        else:
            raise RuntimeException('Tab Unknown status')

    def stop(self):
        if self._stopped.is_set():
            raise RuntimeException('Tab has been stopped')

        if not self._started.is_set():
            raise RuntimeException('Tab is not running')

        logger.debug(f'[*] stop tab {self._id}')

        self._stopped.set()
        self._ws.close()

    def calc_loops(self, sleep, timeout):
        """
        Calc loops
        :param sleep: [int|float], sleep seconds
        :param timeout: [int|float], timeout seconds
        :return: sleep seconds, loops
        """
        _ = self
        return sleep, math.ceil(timeout / sleep)

    def wait(self, selector='', expression=None, timeout=10):
        self._init()

        if selector or expression:
            seconds, loops = self.calc_loops(sleep=0.1, timeout=timeout)
            timeout = seconds

            for _ in range(loops):
                if selector:
                    self.DOM.getDocument()
                    ret = self.DOM.performSearch(query=selector, includeUserAgentShadowDOM=False)
                    if ret['resultCount']:
                        return True
                else:
                    ret = expression()
                    if ret:
                        return True

                time.sleep(seconds)

        return self._stopped.wait(timeout)

    def query(self, selector, timeout=10, limit=None):
        self._init()

        seconds, loops = self.calc_loops(sleep=0.1, timeout=timeout)

        nodes = []
        for _ in range(loops):
            self.DOM.getDocument()
            ret = self.DOM.performSearch(query=selector, includeUserAgentShadowDOM=False)
            if ret['resultCount']:
                to_index = ret['resultCount']
                if limit:
                    to_index = min(limit, to_index)

                nodes = self.DOM.getSearchResults(searchId=ret['searchId'], fromIndex=0, toIndex=to_index)['nodeIds']

                for index, node_id in enumerate(nodes):
                    nodes[index] = self.DOM.getOuterHTML(nodeId=node_id)['outerHTML']

                break

        if limit == 1:
            nodes = (nodes or [''])[0]

        return nodes

    def click(self, selector, limit_one=True):
        selector = selector.replace('"', "'")

        if limit_one:
            expression = f'''document.querySelector("{selector}").click()'''
        else:
            expression = f'''
                for(let element of document.querySelectorAll("{selector}")){{
                    element.click()
                }}
            '''

        ret = self.Runtime.evaluate(expression=expression)
        return ret['result'].get('subtype') != 'error'

    @property
    def url(self):
        return self.Runtime.evaluate(expression='window.location.href')['result']['value']

    def __str__(self):
        return f'<Tab [{self._id}] {self._url}>'

    __repr__ = __str__
