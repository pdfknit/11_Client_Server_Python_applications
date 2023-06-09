import os

DEFAULT_PORT = 8888

DEFAULT_IP_ADDRESS = '127.0.0.1'
CONNECTIONS = 3
MAX_LENGTH = 256
ENCODING = 'utf-8'
TIMEOUT = 2

ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
LOGGING_FORMATTER = '%(asctime)8s  %(levelname)8s  %(filename)13s  %(message)s'
PATH = os.getcwd()

SENDER = 'from'
DESTINATION = 'to'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
EXIT = 'exit'
GET_CONTACTS = 'get_contacts'
LIST_INFO = 'data_list'
REMOVE_CONTACT = 'remove'
ADD_CONTACT = 'add'
USERS_REQUEST = 'get_users'

RESPONSE_200 = {RESPONSE: 200}
# 400
RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None
}

RESPONSE_202 = {
    RESPONSE: 202,
    LIST_INFO: None
}
# База данных для хранения данных сервера:
SERVER_DATABASE = 'sqlite:///server_base.db3'
