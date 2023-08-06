from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.1'
DESCRIPTION = 'maja le liya'

# Setting up
setup(
    name="amrendras",
    version=VERSION,
    author="Prajwal",
    author_email="<prajwalupadhyay13@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
