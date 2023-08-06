from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Python wrapper for Promptlytics'
LONG_DESCRIPTION = 'Promptlytics helps you find the best prompts for your use case'

# Setting up
setup(
    name="promptlytics",
    version=VERSION,
    author="Promptlytics (Scott Cilento)",
    author_email="scott@promptlytics.co",
    url="https://www.promptlytics.co",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests']
)