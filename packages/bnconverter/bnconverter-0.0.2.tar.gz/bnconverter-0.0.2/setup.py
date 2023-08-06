from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Python converting Bangla <=> Unicode (UTF-8) for Bengali to Bangla.'
LONG_DESCRIPTION = 'Python converting Bangla <=> Unicode (UTF-8) for Bengali to Bangla.'

# Setting up
setup(
    name="bnconverter",
    version=VERSION,
    author="Nazrul Islam (Nadeem)",
    author_email="<nazrul.devs@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['regex'],
    keywords=['python', 'converting', 'Unicode', 'Bengali to Bangla'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)