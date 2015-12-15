#!/usr/bin/env python
"""
Setup script
"""
import os
import sys

from setuptools import find_packages, setup

__version__='0.1.9'

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
