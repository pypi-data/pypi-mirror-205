
from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.2'
DESCRIPTION = 'data visualization libraby'
LONG_DESCRIPTION = 'A package that allows to create data visualization.'

# Setting up
setup(
    name="data-visualize-lib",
    version=VERSION,
    author="AshRaut",
    author_email="<x21175748@student.ncirl.ie>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['docx'],
    keywords=['python', 'data', 'visualization'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)


