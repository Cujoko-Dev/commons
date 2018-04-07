# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

import commons

setup(
    name='commons',
    version=commons.__version__,
    description='Commons',
    author='Cujoko',
    author_email='cujoko@gmail.com',
    url='https://github.com/Cujoko/commons',
    packages=find_packages(),
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
    license='MIT'
)
