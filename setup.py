#!/usr/bin/env python3

"""
A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

import setup_commands

__author__ = 'Christof Pieloth'

install_requires = [
    'requests==2.20.*'
]


# development environment dependencies
dev_requires = [
    'coverage',
    'pep257',
    'pycodestyle',
    'pylint==1.9.*',
    'recommonmark',
    'Sphinx==1.7.*'
]


setup(
    cmdclass=dict(setup_commands.custom_commands),

    name=setup_commands.project_name,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=setup_commands.version,

    description='BackBacker is a light backup tool '
                'with a "declarative" job file based on simple commands with arguments.',

    author='Christof Pieloth',
    url='https://github.com/cpieloth',

    # Choose a license: https://choosealicense.com
    license='GPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],

    packages=find_packages(exclude=['build*', 'docs', 'tests*', 'tools*', 'venv*']),

    install_requires=install_requires,

    tests_require=dev_requires,

    extras_require={
        'dev': dev_requires,
    },

    test_suite='tests',

    include_package_data=True,

    entry_points={
        'console_scripts': [
            '{} = {}.{}:main'.format(setup_commands.api_name, setup_commands.api_name, setup_commands.api_name)
        ],
    },
)
