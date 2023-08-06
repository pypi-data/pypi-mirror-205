"""
This file is the setup script for the ASCIIcli module.
This module provides a command line tool for converting images to ASCII art.

For manual uploading:
`py -m build`
`twine upload dist/*`
`pyinstaller --onefile path/to/__main__.py`
"""

from setuptools import setup

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="ASCIIcli",
    author="mrq-andras",
    version="0.1.0",
    # needs to be wherever __init__.py is
    packages=['src'],
    install_requires=["Pillow"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            # needs to be wherever __init__.py is
            "asciicli=src.__main__:main"
        ]
    },
    python_requires=">=3.6",
    url="https://github.com/mrq-andras/asciicli",
    license="MIT",
    description="A command-line tool that converts images to ASCII art.",
    readme="README.md"
)
