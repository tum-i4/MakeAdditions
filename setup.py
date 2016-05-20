#!/usr/bin/env python

from setuptools import setup
import sys

if sys.version_info[0] == 3 and sys.version_info[1] < 4:
    sys.exit('Sorry, Python < 3.4 is not supported')

setup(
    name='MakeLogic',
    version='0.0.1',
    packages=['makelogic'],
    entry_points={
        'console_scripts': [
            'makelogic = makelogic.__main__:main'
        ]
    },
)
