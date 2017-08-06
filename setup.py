#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import ast
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()


_version_re = re.compile(r'__version__\s+=\s+(.*)')


with open('pychrome/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


requirements = [
    'websocket-client>=0.44.0',
    'requests>=2.18.3',
]

setup(
    name='pychrome',
    version=version,
    description="A Python Package for the Google Chrome DevTools Protocol",
    long_description=readme,
    author="fate0,capric",
    author_email='fate0@fatezero.org, capric8416@gmail.com',
    url='https://github.com/fate0/pychrome, https://github.com/capric8416/pychrome',
    packages=find_packages(),
    package_dir={},
    entry_points={},
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='pychrome',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
