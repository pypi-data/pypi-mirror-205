#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='cgem',
    version='0.0.2',
    description='A library for Collaborative Generalized Effects Modeling (CGEM).',
    author='James Rolfsen',
    author_email='james.rolfsen@think.dev',
    url='https://www.linkedin.com/in/jamesrolfsen/', 
    packages=find_packages(),
    #packages=['cgem'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        # List your library dependencies here
    ],
) 



