from setuptools import setup
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='data-lib',
    version='0.0.9',
    url='https://github.com/andresgarcia106/data-lib/',
    license='',
    author='Andres Garcia',
    author_email='andres_garcia@hakkoda.io',
    description='Analytics and Reporting',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['data_lib'],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "crnotebook=data_lib.scripts.new_notebook:main",
            "crconfig=data_lib.scripts.new_config:main",
            "crproject=data_lib.scripts.new_project:main",
        ],
    },
    install_requires=[
        "setuptools>=67.7.2",
        "wheel>=0.40.0",
        "pyodbc>=4.0.39",
        "pandas>=2.0.1",
        "numpy>=1.24.3",
        "xlwings>=0.30.4",
        "openpyxl>=3.1.2",
        "matplotlib>=3.7.1",
        "seaborn>=0.12.2",
        "pymongo>=4.3.3",
        "teradataml>=17.20.0.2",
        "sqlalchemy>=1.4.0, <2.0.0",
        "pytest>=7.3.1",
        "black>=23.3.0",
        "pyxlsb>=1.0.10",
        "plotly==5.14.1",
        "nbconvert>=7.3.1",
        "snowflake-sqlalchemy>=1.4.7",
        "snowflake-snowpark-python>=1.3.0",
        "keyring>=23.13.1",
    ])