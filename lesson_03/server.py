"""Программа-сервер"""

import socket
import sys
import json
# from constants import *
from pprint import pprint
pprint(sys.path)
from lesson_03.functions import get_message, send_message
from lesson_03.constants import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_PORT, \
    DEFAULT_IP_ADDRESS, CONNECTIONS



def process_client_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError('Номер порта может быть указано только в диапазоне от 1024 до 65535.')

    except IndexError:
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)

    if '-a' in sys.argv:
        listen_address = sys.argv[sys.argv.index('-a') + 1]
    else:
        listen_address = DEFAULT_IP_ADDRESS

    # Готовим сокет
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))

    # Слушаем порт
    transport.listen(CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_message(client)
            print(message_from_client)
            response = process_client_message(message_from_client)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорректное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
