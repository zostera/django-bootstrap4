#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import bootstrap4

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = bootstrap4.__version__

if sys.argv[-1] == 'publish':
    os.system('cd docs && make html')
    os.system('python setup.py sdist')
    os.system('twine upload dist/django-bootstrap4-{}.tar.gz'.format(VERSION))

    message = '\nreleased [{version}](https://pypi.python.org/pypi/django-bootstrap4/{version})'
    print(message.format(version=VERSION))
    sys.exit()

if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'tagging version %s'" % (VERSION, VERSION))
    os.system('git push --tags')
    sys.exit()

if sys.argv[-1] == 'test':
    print("Running tests only on current environment.")
    print("Use `tox` for testing multiple environments.")
    os.system('python manage.py test')
    sys.exit()

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

setup(
    name='django-bootstrap4',
    version=VERSION,
    description="""Bootstrap support for Django projects""",
    long_description=readme + '\n\n' + history,
    author='Dylan Verheul',
    author_email='dylan@dyve.net',
    url='https://github.com/zostera/django-bootstrap4',
    packages=[
        'bootstrap4',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="Apache License 2.0",
    zip_safe=False,
    keywords='django-bootstrap4',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
