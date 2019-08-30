#!/usr/local/bin/python


import os
import re

from setuptools import find_packages, setup

VERSIONFILE = "src/bootstrap4/_version.py"
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"

try:
    VERSION = re.search(VSRE, open(VERSIONFILE, "rt").read(), re.M).group(1)
except:  # noqa
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme_file:
    readme = readme_file.read()

with open(os.path.join(os.path.dirname(__file__), "HISTORY.rst")) as history_file:
    history = history_file.read().replace(".. :changelog:", "")

setup(
    name="django-bootstrap4",
    version=VERSION,
    url="https://github.com/zostera/django-bootstrap4",
    author="Dylan Verheul",
    author_email="dylan@dyve.net",
    description="""Bootstrap support for Django projects""",
    long_description=readme + "\n\n" + history,
    license="BSD",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=["beautifulsoup4"],
    zip_safe=False,
    keywords="django-bootstrap4",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],
)
