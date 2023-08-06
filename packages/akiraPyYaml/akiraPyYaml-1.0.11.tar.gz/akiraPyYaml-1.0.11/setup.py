import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
VERSION = '1.0.11'
PACKAGE_NAME = 'akiraPyYaml'
AUTHOR = 'Marc Jose Rubio'
AUTHOR_EMAIL = 'joserubiomarc@gmail.com'
URL = 'https://github.com/toshuomj'

LICENSE = 'MIT'
DESCRIPTION = 'Library for interacting with files and data in yaml format'
with open(HERE / "READMEPyYaml.md") as f:
    LONG_DESCRIPTION = f.read()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'pyyaml'
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)