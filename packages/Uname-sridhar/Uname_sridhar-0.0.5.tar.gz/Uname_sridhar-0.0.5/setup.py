from setuptools import setup, find_packages
import os

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='Uname_sridhar',
    version='0.0.5',
    author='Sridhar',
    author_email='dcsvsridhar@gmail.com',
    description='Get Information About  Linux Kernel with the help of  Python',
    packages=find_packages(),
    url='https://git.selfmade.ninja/SRIDHARDSCV/package_uname_command',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'Uname_cli=main.main:main',
        ],
    },
)