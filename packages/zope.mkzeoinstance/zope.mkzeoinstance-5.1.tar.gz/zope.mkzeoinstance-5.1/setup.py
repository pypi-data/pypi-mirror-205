##############################################################################
#
# Copyright (c) 2003, 2010 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

from setuptools import find_packages
from setuptools import setup


setup(
    name='zope.mkzeoinstance',
    version='5.1',
    url='https://github.com/zopefoundation/zope.mkzeoinstance',
    license='ZPL 2.1',
    description='Make standalone ZEO database server instances',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.dev',
    long_description=(open('README.rst').read() + "\n" +
                      open('CHANGES.rst').read()),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    keywords="ZEO ZODB instance script",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['zope'],
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=[
        'setuptools',
        'zdaemon',
        'ZODB',    # not imported, but generated instance requires it
        'ZEO',     # not imported, but generated instance requires it
    ],
    extras_require=dict(
        test=[
            'zope.testrunner',
        ],
    ),

    zip_safe=False,
    entry_points={
        'console_scripts': [
            'mkzeoinstance = zope.mkzeoinstance:main',
        ],
    },
)
