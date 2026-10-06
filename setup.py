# -*- coding: utf-8 -*-
from setuptools import find_namespace_packages
from setuptools import setup

version = '0.6.1.dev0'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CHANGES.rst').read(),
])

install_requires = [
    'Zope',
    'zope.processlifetime',
]

setup(
    name='haufe.requestmonitoring',
    version=version,
    description="Zope 2 request monitoring",
    long_description=long_description,
    # Get more strings from
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 6.1",
        "Framework :: Plone :: 6.2",
        "Framework :: Zope",
        "Framework :: Zope :: 5",
        "Framework :: Zope :: 6",
        "License :: OSI Approved :: Zope Public License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
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
    packages=find_namespace_packages(include=['haufe.*']),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.10',
    install_requires=install_requires,
    entry_points="""
    # -*- Entry points: -*-
    """,
)
