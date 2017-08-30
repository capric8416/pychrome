#! /usr/bin/env python
# -*- coding: utf-8 -*-

import inspect
import logging
import urllib.parse

from .browser import Browser

__all__ = ['Sniffer']

logger = logging.getLogger(__name__)


class Sniffer(Browser):
    def __init__(self, remote_debugging_url='http://localhost:9222'):
        super(Sniffer, self).__init__(remote_debugging_url=remote_debugging_url)

        self.tab = self.new_tab()
        for tab in self.get_all_tabs():
            if tab != self.tab:
                self.close_tab(tab)

        self.tab.Page.enable()
        self.tab.Network.enable()
        # self.tab.Network.setRequestInterceptionEnabled(enabled=True)

        # self.tab.Network.resourceChangedPriority = self.network_resource_changed_priority
        # self.tab.Network.requestWillBeSent = self.network_request_well_be_send
        # self.tab.Network.requestServedFromCache = self.network_request_served_from_cache
        self.tab.Network.responseReceived = self.network_response_received
        # self.tab.Network.dataReceived = self.network_data_received
        # self.tab.Network.loadingFinished = self.network_loading_finished
        # self.tab.Network.loadingFailed = self.network_loading_failed
        # self.tab.Network.webSocketWillSendHandshakeRequest = self.network_web_socket_will_send_handshake_request
        # self.tab.Network.webSocketHandshakeResponseReceived = self.network_web_socket_handshake_response_received
        # self.tab.Network.webSocketCreated = self.network_web_socket_created
        # self.tab.Network.webSocketClosed = self.network_web_socket_closed
        # self.tab.Network.webSocketFrameReceived = self.network_web_socket_frame_received
        # self.tab.Network.webSocketFrameError = self.network_web_socket_frame_error
        # self.tab.Network.webSocketFrameSent = self.network_web_socket_frame_sent
        # self.tab.Network.eventSourceMessageReceived = self.network_event_source_message_received
        # self.tab.Network.requestIntercepted = self.network_request_intercepted

    def network_resource_changed_priority(self, **kwargs):
        logger.debug(f'[*] {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {kwargs}')

    def network_request_well_be_send(self, **kwargs):
        logger.debug(f'[*] {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {kwargs}')

    def network_request_served_from_cache(self, **kwargs):
        logger.debug(f'[*] {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {kwargs}')

    def network_response_received(self, **kwargs):
        ret = self.tab.Network.getResponseBody(requestId=kwargs['requestId'])
        logger.debug(f'[*] {inspect.currentframe().f_code.co_name} {ret} {kwargs}')

    def network_data_received(self, **kwargs):
        logger.debug(f'[*] {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {kwargs}')

    def network_loading_finished(self, **kwargs):
        logger.debug(f'[*] {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {kwargs}')

    def network_loading_failed(self, **kwargs):
        logger.debug(f'[*] {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {kwargs}')

    def network_web_socket_will_send_handshake_request(self, **kwargs):
        logger.debug(f'[*] {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {kwargs}')

    def network_web_socket_handshake_response_received(self, **kwargs):
        logger.debug(f'[*] {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {kwargs}')

    def network_web_socket_created(self, **kwargs):
        logger.debug(f'[*] {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {kwargs}')

    def network_web_socket_closed(self, **kwargs):
        logger.debug(f'[*] {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {kwargs}')

    def network_web_socket_frame_received(self, **kwargs):
        logger.debug(f'[*] {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {kwargs}')

    def network_web_socket_frame_error(self, **kwargs):
        logger.debug(f'[*] {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {kwargs}')

    def network_web_socket_frame_sent(self, **kwargs):
        logger.debug(f'[*] {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {kwargs}')

    def network_event_source_message_received(self, **kwargs):
        logger.debug(f'[*] {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {kwargs}')

    def network_request_intercepted(self, **kwargs):
        logger.debug(f'[*] {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} {kwargs}')

        continue_kwargs = {'interceptionId': kwargs.get('interceptionId')}

        if kwargs.get('resourceType') in {'Image', 'Stylesheet'}:
            continue_kwargs['errorReason'] = 'AddressUnreachable'

        self.tab.Network.continueInterceptedRequest(**continue_kwargs)

    def open_url(self, url, selector='', timeout=10, new_tab=False):
        if not new_tab:
            self.tab.Page.navigate(url=url, _timeout=timeout)
            return self.tab.wait(selector=selector, timeout=timeout)
        else:
            tab = self.new_tab()
            tab.Page.navigate(url=url, _timeout=timeout)
            status = tab.wait(selector=selector, timeout=timeout)
            self.close_tab(tab)
            return status

    def batch_actions(self, image=None, stylesheet=None, browsing_data=None, proxy=None):
        query = {}
        if isinstance(image, bool):
            query['image'] = 'enable' if image else 'disable'
        if isinstance(stylesheet, bool):
            query['stylesheet'] = 'enable' if stylesheet else 'disable'
        if browsing_data:
            query['browsing_data'] = 'true'
        if isinstance(proxy, (tuple, list)) and proxy:
            query['proxy'] = '|'.join([str(item) for item in proxy])

        if not query:
            return False

        return self.open_url(
            selector='This site can’t be reached', new_tab=True,
            url='http://localhost/batch/actions/?' + urllib.parse.urlencode(query))

    def set_proxy(self, scheme='', host='', port='', scope=''):
        query = {'scheme': scheme, 'host': host, 'port': port, 'scope': scope}
        return self.open_url(
            selector='This site can’t be reached', new_tab=True,
            url='http://localhost/proxy/change/?' + urllib.parse.urlencode(query))

    def clear_browsing_data(self):
        return self.open_url(
            url='http://localhost/browsing_data/remove/', selector='This site can’t be reached', new_tab=True)

    def switch_image(self, action='disable'):
        assert action in ('disable', 'enable')
        return self.open_url(
            url=f'http://localhost/image/{action}/', selector='This site can’t be reached', new_tab=True)

    def switch_stylesheet(self, action='disable'):
        assert action in ('disable', 'enable')
        return self.open_url(
            url=f'http://localhost/stylesheet/{action}/', selector='This site can’t be reached', new_tab=True)
