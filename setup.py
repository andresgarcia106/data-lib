from setuptools import setup
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dataLib',
    version='0.1',
    url='https://github.com/jgarciaf106/dataLib',
    license='',
    author='Andres Garcia',
    author_email='jgarciaf106@gmail.com',
    description='Analytics and Reporting',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['dataLib'],
    include_package_data=True,
    install_requires=["numpy"]
)
