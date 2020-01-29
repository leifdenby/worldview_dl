#!/usr/bin/env python

"""The setup script."""
import sys

from distutils.version import LooseVersion
from setuptools import setup, find_packages
from setuptools import setup, Extension
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    def run_tests(self):
        import shlex
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(['tests/'])
        sys.exit(errno)

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    "pendulum", "requests", "pytz", "tqdm"
]

setup_requirements = [ ]

test_requirements = ["pytest",]

setup(
    author="Leif Denby",
    author_email='leif@denby.eu',
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
    description="Download utility for NASA WorldView",
    entry_points={
        'console_scripts': [
            'worldview_dl=worldview_dl.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='worldview_dl',
    name='worldview_dl',
    packages=find_packages(include=['worldview_dl', 'worldview_dl.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/leifdenby/worldview_dl',
    version='0.2.0',
    zip_safe=False,
    cmdclass=dict(test=PyTest),
)
