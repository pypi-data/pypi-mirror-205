#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['requests', 'fire']

test_requirements = ['pytest>=3', ]

setup(
    author="Hrishikesh Terdalkar",
    author_email='hrishikeshrt@linuxmail.org',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Games/Entertainment',
        'Topic :: Games/Entertainment :: Real Time Strategy'
    ],
    description="A python interface for <OPENDOTA/> API",
    entry_points={
        'console_scripts': [
            'opendota=opendota.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='opendota',
    name='pyopendota',
    packages=find_packages(include=['opendota', 'opendota.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/hrishikeshrt/pyopendota',
    version='0.2.9',
    zip_safe=False,
)
