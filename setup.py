# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


setup(
    name='transforms',
    version='0.0.1',
    provides=['transofrms'],
    author='sroberts',
    url='https://github.com/sroberts/transforms',
    setup_requires='setuptools',
    license='Apache License v 2.0',
    author_email='scott.roberts@gmail.com',
    description='Super useful Maltego transforms for CND justice.',
    packages=find_packages(),
    install_requires=[
        'argparse==1.3.0',
        'requests==2.6.2'
    ],
    entry_points={
        'console_scripts': [
            'transforms=transforms.transforms:main',
        ],
    },
)
