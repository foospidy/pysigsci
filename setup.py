"""
pysigsci setup
"""
import os
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, 'README.rst')) as f:
    LONG_DESC = f.read()

setup(
    name="pysigsci",
    version="0.0.3",
    author="foospidy",
    description=("A python wrapper for the Signal Sciences API - "
                 "https://docs.signalsciences.net/api/"),
    license="MIT",
    keywords="wrapper library signal sciences sigsci pysigsci api cli",
    url="https://github.com/foospidy/pysigsci",
    download_url="https://github.com/foospidy/pysigsci",
    packages=['pysigsci', 'pysigsci.sigsciapi'],
    long_description=LONG_DESC,
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=['requests', 'pyopenssl'],
    scripts=['pysigsci/bin/pysigsci'],
)
