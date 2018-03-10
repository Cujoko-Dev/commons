# -*- coding: utf-8 -*-
from setuptools import setup

import commons

setup(
    name='commons',

    version=commons.__version__,

    description='Commons',

    url='https://github.com/Cujoko/commons',

    author='Cujoko',
    author_email='cujoko@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Natural Language :: Russian',

        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

        'Topic :: Software Development',
        'Topic :: Utilities'
    ],

    keywords='commons',

    install_requires=[
        'appdirs',
        'PyYAML',
        'yodl'
    ],

    py_modules=['commons']
)
