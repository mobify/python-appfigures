# -*- coding: utf-8 -*-
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

requires = ['python-dateutil',
            'purl',
            'six',
            'requests']

tests_requires = ['pytest==2.8.1',
                  'pytest-pep8==1.0.6',
                  'pytest-cache==1.0',
                  'pytest-cov==2.1.0',
                  'betamax==0.5.0']

development_requires = ['bumpversion'] + tests_requires


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name="python-appfigures",
    version='0.0.0',
    description="",
    long_description="\n\n".join([open("README.rst").read()]),
    license=open('LICENSE').read(),
    author="Sebastian Vetter",
    author_email="sebastian@mobify.com",
    url="https://python-appfigures.readthedocs.org",
    package=['appfigures'],
    install_requires=requires,
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython'],
    extras_require={'test': tests_requires,
                    'development': development_requires},
    cmdclass={'test': PyTest})
