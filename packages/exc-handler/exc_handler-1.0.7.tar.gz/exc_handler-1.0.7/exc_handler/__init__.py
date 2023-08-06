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


import sys
from datetime import datetime as dt
from traceback import StackSummary, extract_tb, extract_stack
from types import TracebackType

from termcolor import colored

def exc_hook(exc: Exception, value = None, tb: TracebackType | None = None) -> str:

    """
    A system exception hook that prints out the details of the exception and its traceback.

    Args:
        exc (Exception): The exception that needs to be handled.\n
        value (Optional[Any]): The exception error message. Defaults to None.\n
        tb (Optional[TracebackType]): The traceback object. Defaults to None.\n

    Raises:
        TypeError: If `exc` is not of type `Exception`.

    Returns:
        str: A string containing the current timestamp, the exception name and its error message.
    """

    current_time = dt.strftime(dt.now(), '%d.%m.%Y %H:%M:%S')

    if not value or not tb:
        exc_type = type(exc)

        if not issubclass(exc_type, Exception):
            raise TypeError(f"exc must be Exception, not {exc_type}")

        tb = extract_tb(exc.__traceback__)

        frame = exc.__traceback__.tb_frame
        tb = extract_stack(frame)[:-1] + tb
    
        exc = exc.__class__
        value = exc

    else:
        tb: StackSummary = extract_tb(tb)
    print()
    for frame in tb:
        raised = colored(f"file '{frame.filename}', line {frame.lineno} in {frame.name}:", 'dark_grey')
        print(raised, frame.line.strip(), '', sep='\n')

    message = current_time + ' > ' + colored(f'{exc.__name__}', 'blue') + ': ' + colored(f'{value}', 'red')
    print(message, '\n')
    return f"{exc.__name__}: {value}"


sys.excepthook = exc_hook
