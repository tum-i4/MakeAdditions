#!/usr/bin/env python

from setuptools import setup
import sys

if sys.version_info[0] == 3 and sys.version_info[1] < 4:
    sys.exit('Sorry, Python < 3.4 is not supported')

setup(
    name='MakeAdditions',
    version='0.1-alpha',
    packages=['makeadditions'],
    url="https://github.com/tum-i22/",
    author="Thomas Hutzelmann",
    author_email="t.hutzelmann@tum.de",
    license="Apache Software License",
    entry_points={
        'console_scripts': [
            'make+llvm = makeadditions.__main__:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
