import logging
import os
import sys

from project.common.constants import LOGGING_FORMATTER, PATH

logging_formatter = logging.Formatter(LOGGING_FORMATTER)

# Подготовка имени файла для логирования
path = os.path.join(PATH, 'logs','files', 'client.log')

log_file = logging.FileHandler(path, encoding='utf8')
log_file.setFormatter(logging_formatter)

logger = logging.getLogger('client_log')
logger.addHandler(log_file)
logger.setLevel(logging.DEBUG)


if __name__ == '__main__':

    logger.debug('Test debug ivent')
    logger.info('Test info ivent')
    logger.critical('Test critical event')
    logger.error('Test error ivent')
