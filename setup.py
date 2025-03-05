# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

import sys
import os.path

from codecs import open

from setuptools import setup, find_packages
from setuptools.command.install import install

cwd = os.path.abspath(os.path.dirname(__file__))

VERSION = "0.1.0"

with open('README.md', 'r', encoding='utf-8') as f:
    __readme__ = f.read()

with open('CHANGELOG.md', 'r', encoding='utf-8') as f:
    __changelog__ = f.read()

class VerifyVersionCommand(install):
    """Command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('GHACTION_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)

setup(
    version=VERSION,
    name='platformvalidator',
    description='Helper library for validating configuration files against PaaS schemas.',
    url='https://github.com/Jeck-ai/upsun_config_validator',
    author='Jeck.ai',
    author_email='rob@jeck.ai',
    license='MIT',
    long_description=__readme__ + '\n\n' + __changelog__,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    tests_require=['pytest'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.13'
    ],
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)