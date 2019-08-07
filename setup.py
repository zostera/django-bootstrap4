#!/usr/local/bin/python


import os
import re

from setuptools import setup

VERSIONFILE = "bootstrap4/_version.py"
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"

try:
    VERSION = re.search(VSRE, open(VERSIONFILE, "rt").read(), re.M).group(1)
except:  # noqa
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme_file:
    readme = readme_file.read()

with open(os.path.join(os.path.dirname(__file__), "HISTORY.rst")) as history_file:
    history = history_file.read().replace(".. :changelog:", "")

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
