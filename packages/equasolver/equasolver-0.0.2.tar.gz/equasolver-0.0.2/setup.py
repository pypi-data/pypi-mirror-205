# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='equasolver',
    version='0.0.2',
    description='A simple package to solve linear and quadratic equations',
    long_description=readme,
    author='Snehashish Laskar',
    author_email='snehashish.laskar@gmail.com',
    url='https://github.com/snehashish090/equasolver',
    license=license,
)
