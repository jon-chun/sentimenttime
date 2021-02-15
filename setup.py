#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Jon Chun",
    author_email='jonchun@outlook.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python package to create and analyze text sentiment as a time series",
    entry_points={
        'console_scripts': [
            'sentimenttime=sentimenttime.__main__:main',
        ],
    },
    extras_require = { 
                      "dev": ["pytest>=3.7",],
                      },  # Development Dependencies (ver as specific as possible) update README.rst ```bash $pip install -e .[dev]```
    install_requires=requirements, # Production Dependencies (versions as relaxed as possible >3.0, <4.0)
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    # install_requires = ["blessings ~= 1.7",], # Library Dependencies
    keywords='sentimenttime',
    name='sentimenttime',
    packages=find_packages(include=['sentimenttime']), # 'sentimenttime.*']),
    # package_dir={'': 'sentimenttime'},
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jon_chun/sentimenttime',
    version='0.1.0',
    zip_safe=False,
)