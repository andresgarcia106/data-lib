from setuptools import setup
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ag-data-lib',
    version='0.2',
    url='https://github.com/jgarciaf106/dataLib',
    license='',
    author='Andres Garcia',
    author_email='jgarciaf106@gmail.com',
    description='Analytics and Reporting',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['data_lib'],
    include_package_data=True,
    install_requires=[
        "setuptools>=62.0.0",
        "pyodbc>=4.0.32",
        "pandas>=1.4.2",
        "numpy>=1.21.5",
        "xlwings>=0.27.4",
        "openpyxl>=3.0.9",
        "matplotlib>=3.5.1",
        "seaborn>=0.11.2",
        "fiscalyear>=0.4.0",
        "pymongo>=4.0.2",
        "sqlalchemy>=1.4.34",
        "python-pptx>=0.6.21",
        "pytest>=7.1.1",
        "black>=22.3.0"
    ]
)
