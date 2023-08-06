# Copyright (C) 2023 twyleg
import os
from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="ausbildungsnachweise_utils",
    version=read("VERSION.txt"),
    author="Torsten Wylegala",
    author_email="mail@twyleg.de",
    description="Utilities to generate Ausbildungsnachweise PDFs from human readable input formats.",
    license="GPL 3.0",
    keywords="ausbildungsnachweis ausbildungsnachweise pdf",
    url="https://github.com/twyleg/ausbildungsnachweis_utils",
    packages=find_packages(),
    include_package_data=True,
    long_description=read('README.md'),
    install_requires=[
        "PyMuPDF",
        "python-docx"
    ],
    entry_points={
        'console_scripts': [
            'ausbildungsnachweise_utils = ausbildungsnachweise_utils.starter:start',
        ]
    }
)
