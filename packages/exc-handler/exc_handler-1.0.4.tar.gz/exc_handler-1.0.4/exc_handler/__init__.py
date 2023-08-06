"""
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

from datetime import datetime as dt
import sys
from traceback import extract_tb, StackSummary
from types import TracebackType
from termcolor import colored

def exc_handler(exc: Exception, value, tb: TracebackType):

	current_time = dt.strftime(dt.now(), '%d.%m.%Y %H:%M:%S')

	tb: StackSummary = extract_tb(tb)

	print()
	for frame in tb:
		raised = colored(f"file '{frame.filename}', line {frame.lineno}:", 'dark_grey')
		print(raised, frame.line)

	message = current_time + ' > ' + colored(f'{exc.__name__}', 'blue') + ': ' + colored(f'{value}', 'red')
	print(message)
	return f"{exc.__class__.__name__}: {exc}"

sys.excepthook = exc_handler
