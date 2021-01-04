# 自定义log配置
import threading
from flask import g


class LoggerAdapter(object):
    """
    An adapter for loggers which makes it easier to specify contextual
    information in logging output.
    """
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(LoggerAdapter, "_instance"):
            with LoggerAdapter._instance_lock:
                if not hasattr(LoggerAdapter, "_instance"):
                    LoggerAdapter._instance = object.__new__(cls)
        return LoggerAdapter._instance

    def __init__(self, logger, extra=None):
        """Initial custom log parameters."""
        self.logger = logger
        self.extra = extra

    def process(self, msg, **kwargs):
        """
        Process the logging message and keyword arguments passed in to
        a logging call to insert contextual information.
        The request_id of the user corresponding to the request is automatically inserted.
        """
        try:
            self.request_id = g.request_id
        except Exception as e:
            self.request_id = ''
        kwargs["extra"] = {"request_id": self.request_id}
        if self.extra:
            kwargs.update(self.extra)
        return msg, kwargs

    def debug(self, msg, *args, **kwargs):
        msg, kwargs = self.process(msg, **kwargs)
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        msg, kwargs = self.process(msg, **kwargs)
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        msg, kwargs = self.process(msg, **kwargs)
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        msg, kwargs = self.process(msg, **kwargs)
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        msg, kwargs = self.process(msg, **kwargs)
        self.logger.critical(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        msg, kwargs = self.process(msg, **kwargs)
        self.logger.warning(msg, *args, **kwargs)

