
from logger.logger_adapter import LoggerAdapter
from logger.logger import LoggerMachine
basename = './'


def get_default_logger(basename, **kwargs):
    """Return a default logging handler."""
    logger = LoggerMachine(basename, **kwargs)
    return LoggerAdapter(logger=logger.get_logger())


LOG = get_default_logger(basename)