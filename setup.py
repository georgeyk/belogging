import codecs
import os.path
import re

from setuptools import Command, find_packages, setup

# metadata

here = os.path.abspath(os.path.dirname(__file__))
version = "0.0.0"
changes = os.path.join(here, "CHANGES.rst")
pattern = r'^(?P<version>[0-9]+.[0-9]+(.[0-9]+)?)'
with codecs.open(changes, encoding='utf-8') as changes:
    for line in changes:
        match = re.match(pattern, line)
        if match:
            version = match.group("version")
            break


class VersionCommand(Command):
    description = 'Show library version'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(version)


with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n{}'.format(f.read())

with codecs.open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    changes = f.read()
    long_description += '\n\nChangelog:\n----------\n\n{}'.format(changes)


# Requirements

# Unduplicated tests_requirements and requirements/test.txt
tests_requirements = ['pytest', 'pytest-cov', 'coveralls', 'tox']
install_requirements = ['python-json-logger>=0.1.5']


# setup

setup(
    name='belogging',
    version=version,
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: System :: Logging',
    ],
    keywords='logging',
    setup_requires=['pytest-runner'],
    install_requires=install_requirements,
    tests_require=tests_requirements,
    cmdclass={'version': VersionCommand},
)
