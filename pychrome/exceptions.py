#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class ChromeTabConnectionException(Exception):
    pass


class ChromeCallMethodException(Exception):
    pass


class ChromeTimeoutException(Exception):
    pass


class ChromeRuntimeException(Exception):
    pass
