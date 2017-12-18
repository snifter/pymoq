from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PyMoq',
    version='0.1.0',
    description='An API mocking tool',
    long_description=long_description,
    url='https://github.com/snifter/pymoq',
    author='Marek Podsiadły',
    author_email='marek@podsiadly.info',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='api testing mocking',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    extras_require={
        'test': ['requests'],
    },
)
