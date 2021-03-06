# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

import sys

version = '0.5.2.dev0'

long_description = ('\n\n'.join([
    open('README.rst').read(),
    open('CHANGES.rst').read(),
]))

install_requires = [
    'setuptools',
    'Zope2',
    'zope.app.appsetup',
]

if sys.version_info < (2, 5):
    install_requires.append('threadframe')

setup(
    name='haufe.requestmonitoring',
    version=version,
    description="Zope 2 request monitoring",
    long_description=long_description,
    # Get more strings from
    # http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Framework :: Zope2",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Logging",
    ],
    keywords='zope long-running-request monitor logging',
    author='Haufe-Lexware',
    author_email='info@zopyx.com',
    maintainer='Andreas Jung',
    maintainer_email='info@zopyx.com',
    license='ZPL',
    url='http://github.com/collective/haufe.requestmonitoring',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['haufe'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points="""
    # -*- Entry points: -*-
    """,
)
