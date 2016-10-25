# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import codecs
import os.path
from setuptools import setup, find_packages, Command


# metadata

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'belogging/__version__.py'), encoding='utf-8') as f:
    # this adds __version__ to setup.py
    exec(f.read())


class VersionCommand(Command):
    description = 'Show library version'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(__version__)  # NOQA


with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n{}'.format(f.read())

with codecs.open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    changes = f.read()
    long_description += '\n\nChangelog:\n----------\n\n{}'.format(changes)


# Requirements

# Unduplicated tests_requirements and requirements/test.txt
tests_requirements = ['pytest', 'pytest-cov', 'coveralls']
install_requirements = []


# setup

setup(
    name='belogging',
    version=__version__,  # NOQA
    description='Belogging',
    long_description=long_description,
    url='https://github.com/georgeyk/belogging/',
    download_url='https://github.com/georgeyk/belogging/releases',
    license='MIT',
    author='George Y. Kussumoto',
    author_email='contato@georgeyk.com.br',
    packages=find_packages(exclude=['docs', 'tests', 'tests.*', 'requirements*']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Logging',
        ],
    keywords='logging',
    setup_requires=['pytest-runner'],
    install_requires=install_requirements,
    tests_require=tests_requirements,
    cmdclass={'version': VersionCommand},
)
