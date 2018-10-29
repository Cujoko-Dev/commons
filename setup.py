# -*- coding: utf-8 -*-
from __future__ import absolute_import

import codecs
import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with codecs.open(os.path.join(here, 'commons', '__about__.py'), 'r', 'utf-8') as f:
    exec (f.read(), about)

setup(
    name='commons',
    version=about['__version__'],
    description='Commons',
    author='Cujoko',
    author_email='cujoko@gmail.com',
    url='https://gitlab.com/Cujoko/commons',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ],
    keywords='commons',
    license='MIT',
    install_requires=[
        'appdirs>=1.4.3',
        'PyYAML>=3.12',
        'six>=1.11.0',
        'yodl>=1.0.0'
    ]
)
