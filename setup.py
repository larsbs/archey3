import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="Archey3",
    version="0.4",
    author="Laurie Clark-Michalek",
    author_email="bluepeppers@archlinux.us",
    description="A simple python scrip to display an Archlinux logo in ASCII art along with basic system information.",
    license="GPL",
    url="http://bluepeppers.github.com/archey3",
    long_description=read("README.md"),
    scripts=["archey3"]
)
