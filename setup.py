#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'websocket-client>=0.44.0',
    'requests>=2.13.0',
]

setup(
    name='pychrome',
    version='0.0.1',
    description="A Python Package for the Google Chrome Dev Protocol",
    long_description=readme,
    author="fate0",
    author_email='fate0@fatezero.org',
    url='https://github.com/fate0/pychrome',
    packages=find_packages(),
    package_dir={},
    entry_points={
        'console_scripts': [
            'pychrome=pychrome.cli:main'
        ]
    },
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
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)