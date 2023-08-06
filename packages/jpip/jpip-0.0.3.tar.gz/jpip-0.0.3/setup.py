from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = 'basic hello package'
LONG_DESCRIPTION = 'basic hello pacakge'

# Setting up
setup(
    name="jpip",
    version=VERSION,
    author="Junichi Shimizu",
    author_email="jun.shimi51@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=[''],
    keywords=[''],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)