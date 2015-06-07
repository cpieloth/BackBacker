__author__ = 'Christof Pieloth'

import re
from setuptools import find_packages, setup
import sys


version = re.search('^__version__\s*=\s*"(.*)"', open('backbacker/backbacker.py').read(), re.M).group(1)

if sys.version_info < (3,):
    print('Python 2 is not supported!')
    sys.exit(1)

setup(
    name='BackBacker',
    version=version,
    description='BackBacker is a light backup tool '
                'with a "declarative" job file based on simple commands with arguments.',
    license='GPL v3',
    author='Christof Pieloth',
    url='https://github.com/cpieloth',

    packages=find_packages(),
    entry_points={
        'console_scripts': ['backbacker = backbacker.backbacker:main']
    },
)
