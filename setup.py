#!/usr/bin/env python

from setuptools import setup, find_packages

import zester

setup(
    name='zester',
    version=zester.__version__,
    description='Easier Python client libraries',
    author='Steve Pulec',
    author_email='spulec@gmail',
    url='https://github.com/spulec/zester',
    packages=find_packages(),
    include_package_data=True,
    license=open('LICENSE').read(),
)
