#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='MOMORING',
    version='1.4.1',
    author='Masgils',
    author_email='masgils@foxmail.com',
    description=u'A simple, graceful tool for developer',
    packages=find_packages(),
    install_requires=['click'],
    entry_points={
        'console_scripts': ['momo=MOMORING.applications.cmd:run']
    }
)
