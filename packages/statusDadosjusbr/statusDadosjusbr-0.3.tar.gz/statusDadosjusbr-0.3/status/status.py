import logging
import sys

logging.basicConfig(format='%(message)s', level=logging.INFO)

# Custom type to represent ints
Code = int

OK = 0
InvalidParameters = 1
SystemError = 2
ConnectionError = 3
DataUnavailable = 4
InvalidFile = 5
Unknown = 6
InvalidInput = 7
OutputError = 8
DeadlineExceeded = 9

statusText = {
    OK: "OK",
    InvalidParameters: "Invalid Parameters",
    SystemError: "System Error",
    ConnectionError: "Connection Error",
    DataUnavailable: "Data Unavailable",
    InvalidFile: "Invalid File",
    Unknown: "Unknown",
    InvalidInput: "Invalid Input",
    OutputError: "Output Error",
    DeadlineExceeded: "Context Deadline Exceeded",
}

# Text returns a text for a status code. It returns the empty
# string if the code is unknown.
def text(code: Code) -> str:
    return statusText.get(code, '')

# Error wraps a code and a error messager
class Error(Exception):

    def __init__(self, code: Code, err: Exception):
        self.code = code
        self.err = err

    def error(self):
        return f'Error {self.code}: {self.error}'

# exit_from_error logs the error message and call sys.Exit
# passing the code if err is of type Error
def exit_from_error(err: Error):
    if isinstance(err, Error):
        logging.error(err.err)
        sys.exit(err.code)
    logging.error(str(err))
    sys.exit(Unknown)
