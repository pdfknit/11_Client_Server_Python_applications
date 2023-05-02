"""Программа клиента, отправляющего/читающего простые текстовые сообщения на сервер"""
import logging
import sys
from socket import socket, AF_INET, SOCK_STREAM

from common.constants import DEFAULT_PORT, DEFAULT_IP_ADDRESS

logger = logging.getLogger('client_log')


def echo_client():
    #порт и адрес
    try:
        client_address = sys.argv[1]
        client_port = int(sys.argv[2])
        if client_port < 1024 or client_port > 65535:
            logger.critical(
                f'answer_from_server - ValueError - '
                f'В качестве порта может быть указано только число в диапазоне от 1024 до 65535')
            sys.exit(1)
    except IndexError:
        logger.warning(f'IndexError - used server_address = {DEFAULT_IP_ADDRESS} server_port = {DEFAULT_PORT}')
        client_address = DEFAULT_IP_ADDRESS
        client_port = DEFAULT_PORT

    ADDRESS = (client_address, client_port)

    """Общение с сервером"""
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(ADDRESS)
        while True:
            msg = input('Ваше сообщение: ')
            if msg == 'exit':
                break
            sock.send(msg.encode('utf-8'))
            data = sock.recv(1024).decode('utf-8')
            print(f"Ответ: {data}")


if __name__ == '__main__':
    echo_client()
