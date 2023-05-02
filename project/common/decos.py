import inspect
import logging
import os
import sys

sys.path.append('../')
import logs.config.client_log_config
import logs.config.server_log_config
from functools import wraps

class Log:
    def __init__(self, logger=None):
        self.logger = logger

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            parent_func_name = inspect.currentframe().f_back.f_code.co_name

            module_name = inspect.currentframe().f_back.f_code.co_filename.split("/")[-1]
            #или стоило оставить полный путь?
            if self.logger is None:
                logger_name = module_name.replace('.py', '')
                # print(logger_name)
                self.logger = logging.getLogger(logger_name)

            # self.logger.debug(f'{func.__name__} вызвана из {parent_func_name} '
            #                   f'в модуле {module_name.split(os.sep)[-1]} с аргументами: {args}; {kwargs}')



            result = func(*args, **kwargs)
            return result

        return wrapper
