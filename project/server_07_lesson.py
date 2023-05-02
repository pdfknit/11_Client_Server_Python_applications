import sys
import select
import logging
from socket import socket, AF_INET, SOCK_STREAM
from common.constants import DEFAULT_PORT, DEFAULT_IP_ADDRESS, TIMEOUT
from common.decos import Log

logger = logging.getLogger('server_log')


@Log(logger)
def read_requests(read_clients, all_clients):
    """Чтение запросов"""

    responses = {}

    for sock in read_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            responses[sock] = data
        except Exception:
            msg = f'Клиент {sock.fileno()} {sock.getpeername()} отключился'
            logger.info(msg)
            print(msg)
            all_clients.remove(sock)

    return responses


@Log(logger)
def write_responses(requests, clients_write, all_clients):
    """Ответ сервера"""

    for sock in clients_write:
        if sock in requests:
            try:
                resp = requests[sock].upper()
                logger.info(resp)
                sock.send(resp.encode('utf-8'))
            except Exception:
                msg = f"Клиент {sock.fileno()} {sock.getpeername()} отключился"
                # print(msg)
                logger.info(msg)
                sock.close()
                all_clients.remove(sock)


@Log(logger)
def main():
    """Обработка запросов клиентов"""

    all_clients = []
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            logger.critical(f'ValueError - Номер порта может быть указано только в диапазоне от 1024 до 65535.')

    except IndexError:
        logger.critical(f'IndexError - После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)

    if '-a' in sys.argv:
        listen_address = sys.argv[sys.argv.index('-a') + 1]
    else:
        listen_address = DEFAULT_IP_ADDRESS
    logger.info(f'listen_address = {listen_address}, listen_port = {listen_port}')

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((listen_address, listen_port))
    sock.listen(5)
    sock.settimeout(TIMEOUT)

    while True:
        try:
            conn, addr = sock.accept()
        except OSError as err:
            pass
        else:
            logger.info(f"Получен запрос на соединение от {str(addr)}")
            all_clients.append(conn)
        finally:
            wait = 0
            clients_read = []
            clients_write = []
            try:
                clients_read, clients_write, errors = select.select(all_clients, all_clients, [], wait)
                # logger.info(clients_read)
                # logger.info(clients_write)
            except Exception:
                pass



        requests = read_requests(clients_read, all_clients)
        logger.info(requests)

        if requests:
            logger.debug(requests)
            write_responses(requests, clients_write, all_clients)


logger.info('Server start')
main()
