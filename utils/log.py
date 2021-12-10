'''
Author : hupeng
Time : 2021/11/5 14:56 
Description: 
'''
import os
import json
import logging
import datetime
from logging import FileHandler

import flask
from flask import g


class RequestId():
    def __init__(self):
        self.requestid = None


rd = RequestId()


class Formatter(logging.Formatter):
    def format(self, record):
        record.requestid = rd.requestid
        _ctx = flask.globals._request_ctx_stack.top
        if rd.requestid is None and _ctx is not None:
            record.requestid = getattr(g, 'requestid', None)
        result = super(Formatter, self).format(record)
        return result


class SafeFileHandler(logging.FileHandler):

    def __init__(self, filename, mode="a", encoding="utf-8", delay=0, suffix="%Y-%m-%d"):
        self.mode = mode
        self.encoding = encoding
        self.suffix = suffix
        self.suffix_time = self._today()
        self.filename = os.fspath(filename)
        self.filepath = os.path.abspath(self.filename) + '.' + self.suffix_time
        FileHandler.__init__(self, self.filepath, mode, encoding, delay)

    def emit(self, record):
        try:
            if self.check_base_filename():
                self.build_base_filename()
            FileHandler.emit(self, record)
        except(KeyboardInterrupt, SystemExit):
            raise
        except BaseException:
            self.handleError(record)

    def check_base_filename(self):
        if self.suffix_time != self._today() or \
                not os.path.exists(self.filepath):
            return True
        return False

    def build_base_filename(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        self.suffix_time = self._today()
        self.baseFilename = os.path.abspath(self.filename) + '.' + self.suffix_time
        if not self.delay:
            self.stream = open(self.baseFilename, self.mode, encoding=self.encoding)

    def _today(self):
        return datetime.date.today().strftime(self.suffix)


class MyLogging(object):
    def __init__(self, name, log_dir, handler_names=None, stdout=False):
        self.name = name
        self.log_dir = log_dir
        self.logger = logging.getLogger(name)
        self.formatter = Formatter(
            '[%(asctime)s] |%(levelname)s|[line:%(lineno)d][requestid:%(requestid)s] %(message)s'
        )
        self.logger.setLevel(logging.INFO)
        if stdout:
            self.add_stream_handler()

        if handler_names is not None:
            for handler_name, level in handler_names.items():
                handler = self.get_file_handler(handler_name, level)
                self.logger.addHandler(handler)

    def add_stream_handler(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.formatter)
        stream_handler.setLevel(logging.INFO)
        self.logger.addHandler(stream_handler)
        # return stream_handler

    def get_file_handler(self, file, level=logging.INFO):
        filename = os.path.join(self.log_dir, file + '.log')
        file_handler = SafeFileHandler(filename=filename)
        file_handler.setFormatter(self.formatter)
        file_handler.setLevel(level)
        return file_handler


class LoggerStorage(object):
    def __init__(self):
        self.loggers = []

    def __setattr__(self, key, value):
        if hasattr(self, key):
            raise FileExistsError(f'already exist logger {key}')
        object.__setattr__(self, key, value)
        self.loggers.append(value)


_logger_storage = None


def logger_init(loggers: dict, stdout: bool = False):
    '''
    {
    log_name:
        {
            'log_dir': '',
            'handlers': {handler_name: log_level, ...}
        },
    ...
    }
    :param loggers:
    :return:
    '''
    global _logger_storage
    if _logger_storage is not None:
        return _logger_storage

    _logger_storage = LoggerStorage()
    for name, info in loggers.items():
        log_dir = info['log_dir']
        handlers = info['handlers']
        _logger = MyLogging(name, log_dir, handlers, stdout).logger
        if not isinstance(_logger, logging.Logger):
            raise TypeError(f'logger {name} must be logging.Logger')
        if hasattr(_logger_storage, name):
            raise FileExistsError(f'already exist logger {name}')
        setattr(_logger_storage, name, _logger)
    print(_logger_storage.loggers)


def get_logger(name='main') -> logging.Logger:
    if _logger_storage is None:
        raise ('logger not init')
    if hasattr(_logger_storage, name):
        return getattr(_logger_storage, name, None)
