#!/usr/bin/env python

from setuptools import setup

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
