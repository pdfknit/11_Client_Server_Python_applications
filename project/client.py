import json
import sys
import time
import socket

from project.common.constants import *
from project.common.utils import send_message, get_message


def create_presence_message(account_name='Guest'):
    message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return message


def answer_from_server(message):
    try:
        if message[RESPONSE] == 200:
            return '200 : OK'
        else:
            # print(f'400 : {message[ERROR]}')
            return f'400 : {message[ERROR]}'

    except ValueError:
        raise ValueError('Wrong message[RESPONSE]')
        # print('Wrong message[RESPONSE]')


def main():
    try:
        # 192.168.2.161 7777
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
            sys.exit(1)
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT

    # Инициализация сокета и обмен

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = create_presence_message()
    send_message(transport, message_to_server)
    try:
        answer = answer_from_server(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
