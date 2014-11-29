#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from setuptools import setup


addthis_init = open("addthis/__init__.py").read()
author = re.search("__author__ = '([^']+)'", addthis_init).group(1)
author_email = re.search("__email__ = '([^']+)'", addthis_init).group(1)
version = re.search("__version__ = '([^']+)'", addthis_init).group(1)


setup(
    name='addthis',
    version=version,
    description='A Python wrapper for the AddThis Analytics API',
    long_description=open('README.rst').read(),
    author=author,
    author_email=author_email,
    url='https://github.com/creafz/python-addthis',
    download_url=
    'https://github.com/creafz/python-addthis/tarball/{0}'.format(version),
    packages=['addthis'],
    package_data={'': ['LICENSE']},
    include_package_data=True,
    install_requires=["requests"],
    license='MIT License',
    test_suite='addthis.tests',
    tests_require=["coverage", "mock"],
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy'
    ),
)