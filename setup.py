import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.rst")) as f:
    README = f.read()

setup(
    name="colander_tools",
    version="0.7.0",
    description="Extensions to `colander`, particularly useful as part of REST API validation.",
    long_description=README,
    license="BSD",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        ],
    keywords="",
    author="Platform.sh",
    author_email="sayhello@platform.sh",
    url="https://github.com/platformsh/colander-tools",
    packages=find_packages(),
    install_requires=[
        "colander",
        "pytz",
        ],
    )
