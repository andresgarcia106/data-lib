from setuptools import setup
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
# get requiments
in_reqs = open("requirements.txt", "r").read()
requirements = in_reqs.split("\n")


setup(
    name='data-lib',
    version='0.0.1',
    url='https://github.com/jgarciaf106/dataLib',
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
            "c_notebook=data_lib.scripts.new_notebook:main",
            "c-config=data_lib.scripts.new_config:main",
            "c-project=data_lib.scripts.new_project:main",
        ],
    },
    install_requires=requirements
)