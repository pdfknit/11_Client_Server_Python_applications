import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys

from project.common.constants import LOGGING_FORMATTER, PATH

logging_formatter = logging.Formatter(LOGGING_FORMATTER)

# Подготовка имени файла для логирования
path = os.path.join(PATH, 'logs', 'files', 'server.log')

log_file = logging.handlers.TimedRotatingFileHandler(path, encoding='utf-8', interval=7, when='midnight')
log_file.setFormatter(logging_formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging_formatter)

logger = logging.getLogger('server_log')
logger.addHandler(log_file)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    logger.debug('DEBUG')
    logger.info('INFO')
    logger.critical('CRITICAL')
    logger.error('ERROR')
