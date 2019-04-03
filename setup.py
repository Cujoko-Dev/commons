# -*- coding: utf-8 -*-
from pathlib import Path

from setuptools import setup

here = Path(__file__).parent

about = {}
with Path(here, 'cjk_commons', '__about__.py').open() as f:
    exec(f.read(), about)

setup(
    name='cjk-commons',
    version=about['__version__'],
    description='Commons',
    author='Cujoko',
    author_email='cujoko@gmail.com',
    url='https://github.com/Cujoko/commons',
    packages=['cjk_commons'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ],
    keywords='commons',
    license='MIT',
    install_requires=[
        'appdirs>=1.4.3',
        'PyYAML>=3.12',
        'yodl>=1.0.0'
    ]
)
