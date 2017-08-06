#! /usr/bin/env python
# -*- coding: utf-8 -*-


class PyChromeException(Exception):
    pass


class UserAbortException(PyChromeException):
    pass


class TabConnectionException(PyChromeException):
    pass


class CallMethodException(PyChromeException):
    pass


class TimeoutException(PyChromeException):
    pass


class RuntimeException(PyChromeException):
    pass
