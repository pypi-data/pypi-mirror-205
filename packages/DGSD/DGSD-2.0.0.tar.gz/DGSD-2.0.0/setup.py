# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='DGSD',
    version='v2.0.0',
    author='Anwar Said',
    author_email='anwar.said@itu.edu.pk',
    description='DGSD: Distributed Graph Representation via Graph Statistical Properties',
    long_description='long_description',
    packages=['dgsd',],
    url='https://github.com/Anwar-Said/DGSD',
    download_url = 'https://github.com/Anwar-Said/DGSD/releases/download/v2.0.0/DGSD.tar.gz',
    license='MIT',
    install_requires=[
        'numpy',
        'networkx'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)