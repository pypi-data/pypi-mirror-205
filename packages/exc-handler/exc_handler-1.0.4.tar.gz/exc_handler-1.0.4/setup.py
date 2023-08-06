from setuptools import setup
doc = """
This module handles exception handling for Python applications. It catches exceptions thrown by the application and prints out a stack trace with color-coded syntax for better readability.\n
It also displays the date and time the exception occurred, the exception name and value.

Functions:
    - exc_handler(): handles exception thrown by the application

Dependencies:
    - datetime: for getting the date and time of the exception
    - sys: for setting the excepthook
    - traceback: for extracting the traceback info
    - types: for the TracebackType
    - termcolor: for color-coding the stack trace

Usage:
    - Just import this module
"""

setup(
    name="exc_handler",
    version="1.0.4",
    description=doc,
    author="iineolineii",
    packages=["exc_handler"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
	]
)
