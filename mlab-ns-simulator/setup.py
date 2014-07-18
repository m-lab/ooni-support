#!/usr/bin/env python

from setuptools import setup, find_packages


# Note: We follow PEP-0440 versioning:
# http://legacy.python.org/dev/peps/pep-0440/

VERSION = '0.1.dev0'


setup(
    # Humanish metadata:
    name='mlab-ns-simulator',
    description='A simulator for the mlab-ns service which provides features Ooni needs.',
    version=VERSION,
    author='LeastAuthority',
    author_email='consultancy@leastauthority.com',
    license='FIXME',
    url='https://github.com/LeastAuthority/ooni-support',

    # Python structure for this package:
    packages=find_packages(),
    entry_points = {
        'console_scripts': [
            'mlabsim = mlabsim.main:main',
            ],
        },
    test_suite='mlabsim.tests',

    # Dependencies:
    # Note: The dependency versions are chosen to match ooni-backend where they overlap:
    install_requires=[
        'twisted == 13.0',
        ]
    )
