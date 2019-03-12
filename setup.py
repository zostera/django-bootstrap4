#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import re
import sys

from setuptools import setup

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Read version from app
with open("bootstrap4/__init__.py", "rb") as f:
    VERSION = str(re.search('__version__ = "(.+?)"', f.read().decode("utf-8")).group(1))

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme_file:
    readme = readme_file.read()

with open(os.path.join(os.path.dirname(__file__), "HISTORY.rst")) as history_file:
    history = history_file.read().replace(".. :changelog:", "")

if sys.argv[-1] == "tag":
    os.system("git tag -a v{} -m 'tagging v{}'".format(VERSION, VERSION))
    os.system("git push --tags && git push origin master")
    sys.exit()

if sys.argv[-1] == "publish":
    os.system("cd docs && make html")
    os.system("python setup.py sdist")
    os.system("twine upload dist/django-bootstrap4-{}.tar.gz".format(VERSION))

    message = "\nreleased [{version}](https://pypi.python.org/pypi/django-bootstrap4/{version})"
    print(message.format(version=VERSION))
    sys.exit()

if sys.argv[-1] == "test":
    print("Running tests only on current environment.")
    print("Use `tox` for testing multiple environments.")
    os.system("python manage.py test")
    sys.exit()

setup(
    name="django-bootstrap4",
    version=VERSION,
    description="""Bootstrap support for Django projects""",
    long_description=readme + "\n\n" + history,
    author="Dylan Verheul",
    author_email="dylan@dyve.net",
    url="https://github.com/zostera/django-bootstrap4",
    packages=["bootstrap4"],
    include_package_data=True,
    install_requires=[],
    license="Apache License 2.0",
    zip_safe=False,
    keywords="django-bootstrap4",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],
)
