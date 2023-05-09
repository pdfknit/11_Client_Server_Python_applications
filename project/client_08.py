"""Программа-клиент"""

import sys
import json
import socket
import time
import argparse
import logging
import threading
import logs.config.client_log_config
from common.constants import DEFAULT_PORT, DEFAULT_IP_ADDRESS, ACTION, \
    TIME, USER, ACCOUNT_NAME, PRESENCE, RESPONSE, ERROR, MESSAGE, MESSAGE_TEXT, DESTINATION, EXIT, SENDER
from common.errors import IncorrectDataRecivedError, ServerError, ReqFieldMissingError
from common.utils import get_message, send_message
from common.decos import Log

# Инициализация клиентского логера
logger = logging.getLogger('client_log')


@Log(logger)
def create_exit_message(account_name):
    """Функция создаёт словарь с сообщением о выходе"""
    return {
        ACTION: EXIT,
        TIME: time.time(),
        ACCOUNT_NAME: account_name
    }


@Log(logger)
def message_from_server(sock, my_username):
    """Обработчик сообщений пользователей, поступающих с сервера"""
    while True:
        try:
            message = get_message(sock)
            if ACTION in message and message[ACTION] == MESSAGE and \
                    SENDER in message and DESTINATION in message \
                    and MESSAGE_TEXT in message and message[DESTINATION] == my_username:
                logger.info(f'Получено сообщение от {message[SENDER]}:'
                            f'\n{message[MESSAGE_TEXT]}')
            else:
                logger.error(f'Некорректное сообщение с сервера: {message}')
        except IncorrectDataRecivedError:
            logger.error('Принято некорректное сообщение от удалённого компьютера.')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            logger.critical(f'Нет соединения с сервером')
            break


@Log(logger)
def create_message(sock, account_name='Guest'):
    """Функция запрашивает сообщение и получателя, и отправляет его сервер"""

    to_user = input('Введите получателя: ')
    message = input('Введите сообщение: ')
    message_dict = {
        ACTION: MESSAGE,
        SENDER: account_name,
        DESTINATION: to_user,
        TIME: time.time(),
        MESSAGE_TEXT: message
    }
    logger.debug(f'Сформирован словарь сообщения: {message_dict}')
    try:
        send_message(sock, message_dict)
        logger.info(f'Отправлено сообщение пользователю: {to_user}')
    except:
        logger.critical('Потеряно соединение с сервером')
        sys.exit(1)


@Log(logger)
def user_interactive(sock, username):
    """Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения"""
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            send_message(sock, create_exit_message(username))
            print('Завершение соединения.')
            logger.info('Завершение работы по команде пользователя.')
            # Задержка неоходима, чтобы успело уйти сообщение о выходе
            time.sleep(0.5)
            break
        else:
            print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')


@Log(logger)
def create_presence(account_name):
    """Функция генерирует запрос о присутствии клиента"""
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    logger.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


def print_help():
    """Функция выводящяя справку по использованию"""
    print('Поддерживаемые команды:')
    print('message - отправить сообщение.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


@Log(logger)
def process_response_ans(message):
    """
    Функция разбирает ответ сервера, возращает 200 если все ОК или генерирует исключения"""
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            raise ServerError(f'400 : {message[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


@Log(logger)
def arg_parser():
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        logger.critical('Допустимы адреса с 1024 до 65535')
        sys.exit(1)

    return server_address, server_port, client_name


def main():
    """Сообщаем о запуске"""
    print('Клиент запущен')

    # Параметы командной строки
    server_address, server_port, client_name = arg_parser()
    if not client_name:
        client_name = input('Введите имя пользователя: ')

    logger.info(
        f'Запущен клиент адрес сервера: {server_address}, '
        f'порт: {server_port}, имя пользователя: {client_name}')

    # Инициализация сокета и сообщение серверу
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence(client_name))
        answer = process_response_ans(get_message(transport))
        logger.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        logger.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ServerError as error:
        logger.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        logger.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        sys.exit(1)
    except (ConnectionRefusedError, ConnectionError):
        logger.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        # запускаем клиенский процесс приёма сообщний
        receiver = threading.Thread(target=message_from_server, args=(transport, client_name))
        receiver.daemon = True
        receiver.start()

        # запускаем отправку сообщений
        user_interface = threading.Thread(target=user_interactive, args=(transport, client_name))
        user_interface.daemon = True
        user_interface.start()
        logger.debug('Запущены процессы')

        # основной цикл
        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
