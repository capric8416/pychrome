#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals


__all__ = ["ChromeTabConnectionException", "ChromeCallMethodException", "ChromeTimeoutException"]


class ChromeTabConnectionException(Exception):
    pass


class ChromeCallMethodException(Exception):
    pass


class ChromeTimeoutException(Exception):
    pass
