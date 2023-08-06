# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    lic = f.read()

setup(
    name='routescan',
    version='0.1.1-alpha',
    description='Automatically scans and adds routes to app',
    long_description=readme,
    author='wangyandong01',
    author_email='wangyandong01@inspur.com',
    url='https://git.iec.io/ai/routescan',
    license=lic,
    packages=find_packages(include=['routescan', 'routescan.*']),
    # packages=['routescan']
    # packages=find_packages(exclude=('tests', 'docs'))
)
