from setuptools import setup, find_packages
from pathlib import Path
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.1'
DESCRIPTION = 'A modern python alternative of the ls binary!'
this_directory = Path(__file__).parent
LONG_DES = (this_directory / "README.md").read_text()
# Setting up
setup(
    name="pyaview",
    version=VERSION,
    author="Birdlinux (G. P.)",
    author_email="<prepakis.geo@gmail.com>",
    description=DESCRIPTION,
    long_description= LONG_DES,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    scripts=['bin/pyaview'],
    keywords=['python ls', 'python system Detection', 'python hex', 'python rgb', 'python hex', 'python loader', 'rich python', 'python rich', 'cutepy'],
    classifiers=[]
)
