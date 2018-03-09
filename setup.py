# -*- coding: utf-8 -*-
from setuptools import setup

import cujoko_commons

setup(
    name='cujoko_commons',

    version=cujoko_commons.__version__,

    description='Commons',

    url='https://github.com/Cujoko/cujoko-commons',

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

    keywords='cujoko-commons',

    install_requires=[
        'appdirs',
        'PyYAML',
        'yodl'
    ],

    py_modules=['cujoko-commons']
)
