#!/usr/bin/env python2

from setuptools import setup



setup(
    name='bouncer-plumbing',
    description='Glue scripts to integrate oonib with mlab-ns (simulator).',
    version='0.1.dev0',
    author='LeastAuthority',
    author_email='consultancy@leastauthority.com',
    license='FIXME',
    url='https://github.com/LeastAuthority/ooni-support',
    scripts = [
        './collector-to-mlab/getconfig.py',
        './mlab-to-bouncer/makeconfig.py',
        ],
    install_requires=[
        'PyYaml', # BUG: Put a version constraint.
        ],
    )
