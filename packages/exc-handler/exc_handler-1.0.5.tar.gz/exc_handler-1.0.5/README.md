# Exception Handling Module

This module provides an easy way to handle exceptions thrown by Python applications. It catches exceptions and prints out a stack trace with color-coded syntax for better readability. The date and time of the exception, and the exception name and value are also displayed.

## Functions

- `exc_handler()`: handles exceptions thrown by the application

## Dependencies

- `datetime`: for getting the date and time of the exception
- `sys`: for setting the excepthook
- `traceback`: for extracting the traceback info
- `types`: for `TracebackType`
- `termcolor`: for color-coding the stack trace

## Usage

Just import this module