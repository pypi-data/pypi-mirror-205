from enum import Enum


class Verbosity(Enum):
    FORCE = 0
    ERROR = 1
    WARN = 2
    INFO = 3
    TRACE = 4


class Logger(object):
    def __init__(self, verbosity: Verbosity = Verbosity.INFO):
        # maximum verbosity of messages to print
        self.verbosity = verbosity

    def log(self, message: str, message_verbosity: Verbosity):
        # if the message verbosity is within the configured maximum verbosity
        if message_verbosity.value <= self.verbosity.value:
            # then print the message
            print(message)

    def trace(self, message: str):
        self.log(message, Verbosity.TRACE)

    def info(self, message: str):
        self.log(message, Verbosity.INFO)

    def warn(self, message: str):
        self.log(message, Verbosity.WARN)

    def error(self, message: str):
        self.log(message, Verbosity.ERROR)

    def force(self, message: str):
        self.log(message, Verbosity.FORCE)

    def log_only_when_quieter_than(self, message: str, compare_verbosity: Verbosity):
        if self.verbosity.value <= compare_verbosity.value:
            print(message)

    def is_quiet(self):
        return self.verbosity.value == Verbosity.ERROR.value

    def is_verbose(self):
        return self.verbosity.value == Verbosity.TRACE.value

    def be_quiet(self):
        self.verbosity = Verbosity.ERROR

    def be_verbose(self):
        self.verbosity = Verbosity.TRACE


logger = Logger()
