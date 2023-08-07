from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.10'
DESCRIPTION = 'Inworld Wrapper for Python'
LONG_DESCRIPTION = 'A python package that allows a user to create chat apps using inworld.'

# Setting up
setup(
    name="inworld_python",
    version=VERSION,
    author="Edgelord (Lucky Robinson)",
    author_email="<luckstarsfilm@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['nodejs-bin'],
    keywords=['python', 'Inworld', 'NPC', 'Game Characters'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
