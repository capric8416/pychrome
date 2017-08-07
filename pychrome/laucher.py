# -*- coding: utf-8 -*-
# !/usr/bin/env python

import inspect
import logging
import subprocess
import time
from multiprocessing.dummy import Pool as ThreadPool

import requests

logger = logging.getLogger(__name__)


class Launcher(object):
    def __init__(self, chrome_path='google-chrome', from_port=9222, count=1):
        self.ports = [port for port in range(from_port, from_port + count)]
        self.chrome_path = chrome_path

    def _open(self, port):
        process = subprocess.Popen(
            [
                self.chrome_path,
                '-incognito',
                '--headless',
                '--disable-gpu',
                '--disable-background-networking',
                '--disable-client-side-phishing-detection',
                '--disable-default-apps',
                '--disable-hang-monitor',
                '--disable-popup-blocking',
                '--disable-prompt-on-repost',
                '--disable-sync',
                '--disable-web-resources',
                '--enable-automation',
                '--enable-logging',
                # '--force-fieldtrials=SiteIsolationExtensions/Control',
                '--ignore-certificate-errors',
                # '--load-extension=/tmp/.org.chromium.Chromium.oBxInc/internal',
                '--log-level=0',
                '--metrics-recording-only',
                '--no-first-run',
                '--no-sandbox',
                '--password-store=basic',
                '--remote-debugging-port={}'.format(port),
                '--safebrowsing-disable-auto-update',
                '--use-mock-keychain',
                '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 '
                '(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
                '--user-data-dir=/tmp/.org.chromium.Chromium.{}'.format(port),
                '--window-size=375,667',
            ],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

        logger.info('{} chrome:{} {}'.format(inspect.currentframe().f_code.co_name, port, process.pid))

        for _ in range(10):
            try:
                requests.get('http://localhost:{}/json'.format(port), timeout=5, json=True)
            except requests.ConnectionError:
                time.sleep(1)
            else:
                break

    def _close(self, port):
        _ = self

        process = subprocess.Popen(
            ';'.join([
                "lsof -i :%s | grep -v PID | awk '{print $2}'" % port,
                "ps -ef | grep -E '\-\-remote-debugging-port=%s' | grep -v grep | awk '{print $2}'" % port
            ]),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        process.wait(3)

        for pid in {item for item in process.stdout.read().decode('utf-8').strip().split()}:
            logger.info('close chrome:{} {}'.format(port, pid))
            subprocess.Popen(
                'kill -9 {}'.format(pid), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait(3)

    def _reopen(self, port):
        self._close(port=port)
        self._close(port=port)

    def _run(self, func):
        pool = ThreadPool(processes=len(self.ports))
        pool.map(func, self.ports)
        pool.close()
        pool.join()

    def start(self):
        self._run(func=self._open)

    def stop(self):
        self._run(func=self._close)

    def restart(self):
        self._run(func=self._reopen)
