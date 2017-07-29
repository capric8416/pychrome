# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import click
import pychrome


click.disable_unicode_literals_warning = True


shared_options = [
    click.option("--version", "-v", help="output usage information"),
    click.option("--host", "-t", help="HTTP frontend host"),
    click.option("--port", "-p", help="HTTP frontend port"),
    click.option("--secure", "-s", help="HTTPS/WSS frontend")
]


@click.group()
@click.version_option("1.1")
def main():
    pass


@main.command()
@click.option("--web-socket", "-w", help="interpret <target> as a WebSocket URL instead of a target id")
def inspect():
    """inspect a target (defaults to the first available target)"""
    browser = pychrome.Browser()


@main.command()
def list():
    """list all the available targets/tabs"""
    browser = pychrome.Browser()
    print(browser.list_tab())


@main.command()
@click.argument("url", default=None)
def new(url):
    """create a new target/tab"""
    browser = pychrome.Browser()
    print(browser.new_tab(url))


@main.command()
@click.argument("id")
def activate(id):
    """activate a target/tab by id"""
    browser = pychrome.Browser()
    print(browser.activate_tab(id))


@main.command()
@click.argument("id")
def close(id):
    """close a target/tab by id"""
    browser = pychrome.Browser()
    print(browser.close_tab(id))


@main.command()
def version():
    """show the browser version"""
    browser = pychrome.Browser()
    print(browser.version())


if __name__ == '__main__':
    main()
