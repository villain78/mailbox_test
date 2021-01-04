# 自定义log配置

import os
import io
import traceback
import logging
from logging.handlers import DatagramHandler
from logging.handlers import DEFAULT_UDP_LOGGING_PORT
from logging import RootLogger, _levelToName, _nameToLevel, _acquireLock, PlaceHolder, _releaseLock, \
    Logger, currentframe, Manager


def addLevelName(level, levelName):
    """
    Associate 'levelName' with 'level'.

    This is used when converting levels to text during message formatting.
    """
    _acquireLock()
    try:
        _levelToName[level] = levelName
        _nameToLevel[levelName] = level
    finally:
        _releaseLock()


_srcfile = os.path.normcase(addLevelName.__code__.co_filename)


class PrivateManager(Manager):

    def getLogger(self, name):
        """Get a logger with the specified name (channel name), creating it."""
        if not isinstance(name, str):
            raise TypeError('A logger name must be a string')
        _acquireLock()
        try:
            if name in self.loggerDict:
                rv = self.loggerDict[name]
                if isinstance(rv, PlaceHolder):
                    ph = rv
                    rv = (self.loggerClass or _loggerClass)(name)
                    rv.manager = self
                    self.loggerDict[name] = rv
                    self._fixupChildren(ph, rv)
                    self._fixupParents(rv)
            else:
                rv = (self.loggerClass or _loggerClass)(name)
                rv.manager = self
                self.loggerDict[name] = rv
                self._fixupParents(rv)
        finally:
            _releaseLock()
        return rv

    def _fixupParents(self, alogger):
        """
        Ensure that there are either loggers or placeholders all the way
        from the specified logger to the root of the logger hierarchy.
        """
        name = alogger.name
        i = name.rfind(".")
        rv = None
        while (i > 0) and not rv:
            substr = name[:i]
            if substr not in self.loggerDict:
                self.loggerDict[substr] = PlaceHolder(alogger)
            else:
                obj = self.loggerDict[substr]
                if isinstance(obj, Logger):
                    rv = obj
                else:
                    assert isinstance(obj, PlaceHolder)
                    obj.append(alogger)
            i = name.rfind(".", 0, i - 1)
        if not rv:
            rv = self.root
        alogger.parent = rv

    def _fixupChildren(self, ph, alogger):
        """
        Ensure that children of the placeholder ph are connected to the
        specified logger.
        """
        name = alogger.name
        namelen = len(name)
        for c in ph.loggerMap.keys():
            if c.parent.name[:namelen] != name:
                alogger.parent = c.parent
                c.parent = alogger


class PrivateLogger(Logger):

    def findCaller(self, stack_info=False):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe()
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv


_loggerClass = PrivateLogger


class LoggerMachine(object):
    """Manage log transaction for machine."""
    LOG_DIC = {}

    def __init__(self, basename, **kwargs):
        """Initializes the parameters for creating the log."""
        self.basename = basename
        self.kwargs = kwargs

    def new_logger(self):
        """Create default logs"""
        logger = logging.getLogger(self.basename)
        handler = DatagramHandler('localhost', DEFAULT_UDP_LOGGING_PORT)
        logger.addHandler(handler)
        _level = (self.kwargs.get("level") or "INFO").upper()
        if _level == "DEBUG" or _level == "INFO":
            logger.setLevel(logging.INFO)
        elif _level == "WARNING":
            logger.setLevel(logging.WARNING)
        elif _level == "ERROR":
            logger.setLevel(logging.ERROR)
        elif _level == "CRITICAL":
            logger.setLevel(logging.CRITICAL)
        else:
            logger.setLevel(logging.ERROR)
        return logger

    def get_logger(self):
        """Return a default logging handler."""
        if self.basename not in LoggerMachine.LOG_DIC:
            LoggerMachine.LOG_DIC[self.basename] = self.new_logger()
        return LoggerMachine.LOG_DIC[self.basename]


Logger.manager = PrivateManager(RootLogger(logging.WARNING))
