import logging

# TODO: logs can have errors too
# TODO: file reaches max size


class Logger:
    """Text file logging class that all written modules implement for coverage.

    Args:
        source (str): The name of the parent module.

    Parameters:
        INFO: Workflow level messages.
        DEBUG: Debug level messages.
        WARNING: Warning level messages.
        ERROR: Non-critical error level messages.
        CRITICAL: Critical error level messages.
        source (str): The name of the parent module.
        keys (dict): Wrapper for logging library to parse source.
    """

    INFO = logging.INFO
    DEBUG = logging.DEBUG
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def __init__(self, source):
        self.source = source
        self.keys = {'source': self.source}
        logging.basicConfig(filename='gui_log.log',
                            level=logging.NOTSET,
                            format='%(asctime)s | %(source)-20s | %(levelname)-8s | %(message)s ',
                            datefmt='%H:%M:%S %d/%m/%Y')

    def log(self, message, severity):
        if severity == logging.INFO:
            logging.info(message, extra=self.keys)
        elif severity == logging.DEBUG:
            logging.debug(message, extra=self.keys)
            print(self.source + ': ' + message)
        elif severity == logging.WARNING:
            logging.warning(message, extra=self.keys)
            print(self.source + ': ' + message)
        elif severity == logging.ERROR:
            logging.error(message, extra=self.keys)
            print(self.source + ': ' + message)
        elif severity == logging.CRITICAL:
            logging.critical(message, extra=self.keys)
        else:
            print("Unknown log type received")
