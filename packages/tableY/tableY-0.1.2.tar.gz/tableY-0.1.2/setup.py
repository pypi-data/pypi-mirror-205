
from __future__ import print_function
from setuptools import setup, find_packages
import sys
import io,os
here = os.path.abspath(os.path.dirname(__file__))

with open("readme.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

# def read_file(filename):
#     with open(filename) as fp:
#         return fp.read().strip()
#
# def read_requirements(filename):
#     return [line.strip() for line in read_file(filename).splitlines()
#             if not line.startswith('#')]

# REQUIRED = read_requirements('requirements.txt')
setup(
    name='tableY',
    version='0.1.2',
    author='White.tie',
    author_email='1042798703@qq.com',
    url='https://github.com/tyj-1995',
    description='Convert the columns of the table to json',
    long_description='将table中的列转成json',
    packages=['tableY'],
    install_requires=["pandas"],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 3.6",
        ],
)
