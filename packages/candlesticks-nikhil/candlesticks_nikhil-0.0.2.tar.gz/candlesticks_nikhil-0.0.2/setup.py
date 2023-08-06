from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'candlestick patterns'
LONG_DESCRIPTION = 'Identifying candlestick patterns in python'

# Setting up
setup(
    name="candlesticks_nikhil",
    version=VERSION,
    author="Nikhil",
    author_email="cnikhil247@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['candlesticks', 'patterns', 'reversals','nikhil','trading'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)