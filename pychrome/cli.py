# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import click
import pychrome


click.disable_unicode_literals_warning = True
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


shared_options = [
    click.option("--version", "-v", help="output usage information"),
    click.option("--host", "-t", type=click.STRING, help="HTTP frontend host"),
    click.option("--port", "-p", type=click.INT, help="HTTP frontend port"),
    click.option("--secure", "-s", help="HTTPS/WSS frontend")
]


def pass_cli_config(func):
    # add all the shared options to the command
    for option in shared_options:
        func = option(func)

    return func


class JSONTabEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pychrome.Tab):
            return obj.origin_json

        return super(JSONTabEncoder, self).default(self, obj)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(pychrome.__version__)
def main():
    pass


@main.command(context_settings=CONTEXT_SETTINGS)
@pass_cli_config
def list():
    """list all the available targets/tabs"""
    browser = pychrome.Browser()
    print(json.dumps(browser.list_tab(), cls=JSONTabEncoder, indent=4))


@main.command(context_settings=CONTEXT_SETTINGS)
@click.argument("url", required=False)
@pass_cli_config
def new(url="about:blank"):
    """create a new target/tab"""
    browser = pychrome.Browser()
    print(json.dumps(browser.new_tab(url), cls=JSONTabEncoder, indent=4))


@main.command(context_settings=CONTEXT_SETTINGS)
@click.argument("id")
@pass_cli_config
def activate(id):
    """activate a target/tab by id"""
    browser = pychrome.Browser()
    print(browser.activate_tab(id))


@main.command(context_settings=CONTEXT_SETTINGS)
@click.argument("id")
@pass_cli_config
def close(id):
    """close a target/tab by id"""
    browser = pychrome.Browser()
    print(browser.close_tab(id))


@main.command(context_settings=CONTEXT_SETTINGS)
@pass_cli_config
def version():
    """show the browser version"""
    browser = pychrome.Browser()
    print(json.dumps(browser.version(), indent=4))


if __name__ == '__main__':
    main()
