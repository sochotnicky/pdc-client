#!/usr/bin/env python
"""
Setup script
"""
import os
import sys
MAIN_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.insert(0, MAIN_DIR)

from setuptools import find_packages, setup
# this won't work because we'd import __init__.py and fail on import beanbag or
# other dependency. There are multiple ways to solve it, but leave it for
# later...
# from pdc_client.version import __version__

# TODO this is duplicated in pdc_client/version.py
__version__='0.1.8'

setup(
    name = 'pdc-client',
    description = 'Client library and console client for Product Definition Center',
    install_requires = [ 'beanbag > 1.9.0', 'requests-kerberos'],
    version = __version__,
    license = 'MIT',
    download_url = 'https://github.com/product-definition-center/pdc-client/releases',
    url = 'https://github.com/product-definition-center/pdc-client',
    packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*",
        "tests"]),
    scripts = ["bin/pdc", "bin/pdc_client"],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities'
    ]
)
