#! /usr/bin/env python
# -*- coding: utf-8 -*-

import inspect
import logging

from .browser import Browser

__all__ = ['Sniffer']

logger = logging.getLogger(__name__)


class Sniffer(Browser):
    def __init__(self, chrome_remote_debugging_url='http://localhost:9222'):
        super(Sniffer, self).__init__(chrome_remote_debugging_url=chrome_remote_debugging_url)

        self.tab = self.get_one_tab()

        self.tab.Page.enable()
        self.tab.Network.enable()
        self.tab.Network.setRequestInterceptionEnabled(enabled=True)

        # self.tab.Network.resourceChangedPriority = self.network_resource_changed_priority
        self.tab.Network.requestWillBeSent = self.network_request_well_be_send
        self.tab.Network.requestServedFromCache = self.network_request_served_from_cache
        self.tab.Network.responseReceived = self.network_response_received
        # self.tab.Network.dataReceived = self.network_data_received
        self.tab.Network.loadingFinished = self.network_loading_finished
        self.tab.Network.loadingFailed = self.network_loading_failed
        # self.tab.Network.webSocketWillSendHandshakeRequest = self.network_web_socket_will_send_handshake_request
        # self.tab.Network.webSocketHandshakeResponseReceived = self.network_web_socket_handshake_response_received
        # self.tab.Network.webSocketCreated = self.network_web_socket_created
        # self.tab.Network.webSocketClosed = self.network_web_socket_closed
        # self.tab.Network.webSocketFrameReceived = self.network_web_socket_frame_received
        # self.tab.Network.webSocketFrameError = self.network_web_socket_frame_error
        # self.tab.Network.webSocketFrameSent = self.network_web_socket_frame_sent
        # self.tab.Network.eventSourceMessageReceived = self.network_event_source_message_received
        self.tab.Network.requestIntercepted = self.network_request_intercepted

    def network_resource_changed_priority(self, **kwargs):
        logger.debug('[*] {} {}'.format(inspect.currentframe().f_code.co_name, kwargs))

    def network_request_well_be_send(self, **kwargs):
        logger.debug('[*] {} {}'.format(inspect.currentframe().f_code.co_name, kwargs))

    def network_request_served_from_cache(self, **kwargs):
        logger.debug('[*] {} {}'.format(inspect.currentframe().f_code.co_name, kwargs))

    def network_response_received(self, **kwargs):
        logger.debug('[*] {} {}'.format(inspect.currentframe().f_code.co_name, kwargs))

    def network_data_received(self, **kwargs):
        logger.debug('[*] {} {}'.format(inspect.currentframe().f_code.co_name, kwargs))

    def network_loading_finished(self, **kwargs):
        logger.debug('[*] {} {}'.format(inspect.currentframe().f_code.co_name, kwargs))

    def network_loading_failed(self, **kwargs):
        logger.debug('[*] {} {}'.format(inspect.currentframe().f_code.co_name, kwargs))

    def network_web_socket_will_send_handshake_request(self, **kwargs):
        logger.debug('[*] {} {}'.format(inspect.currentframe().f_code.co_name, kwargs))

    def network_web_socket_handshake_response_received(self, **kwargs):
        logger.debug('[*] {} {}'.format(inspect.currentframe().f_code.co_name, kwargs))

    def network_web_socket_created(self, **kwargs):
        logger.debug('[*] {} {}'.format(inspect.currentframe().f_code.co_name, kwargs))

    def network_web_socket_closed(self, **kwargs):
        logger.debug('[*] {} {}'.format(inspect.currentframe().f_code.co_name, kwargs))

    def network_web_socket_frame_received(self, **kwargs):
        logger.debug('[*] {} {}'.format(inspect.currentframe().f_code.co_name, kwargs))

    def network_web_socket_frame_error(self, **kwargs):
        logger.debug('[*] {} {}'.format(inspect.currentframe().f_code.co_name, kwargs))

    def network_web_socket_frame_sent(self, **kwargs):
        logger.debug('[*] {} {}'.format(inspect.currentframe().f_code.co_name, kwargs))

    def network_event_source_message_received(self, **kwargs):
        logger.debug('[*] {} {}'.format(inspect.currentframe().f_code.co_name, kwargs))

    def network_request_intercepted(self, **kwargs):
        continue_kwargs = {'interceptionId': kwargs.get('interceptionId')}

        if kwargs.get('resourceType') in {'Image', 'Stylesheet'}:
            continue_kwargs['errorReason'] = 'AddressUnreachable'

        self.tab.Network.continueInterceptedRequest(**continue_kwargs)

    def open_url(self, url, selector='', timeout=10):
        self.tab.Page.navigate(url=url, _timeout=timeout)
        return self.tab.wait(selector=selector, timeout=timeout)
