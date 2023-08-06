import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "securepasswordgenerator",
    version = "1.0.0",
    author = "Ali Fayaz (Quill)",
    author_email = "fayaz.quill@gmail.com",
    description = ("SecurePasswordGenerator is a tool for generating random passwords. It provides both command line utility and underlying python module."),
    license = "MIT",
    keywords = "password generator",
    url = "https://github.com/quillfires/SecurePasswordGenerator",
    packages=["securepasswordgenerator"],
    include_package_data=True,
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable"
    ],
    entry_points = {
        'console_scripts': ['securepasswordgenerator=securepasswordgenerator.securepasswordgenerator:main'],
    }
)