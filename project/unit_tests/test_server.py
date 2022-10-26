import sys
sys.path.append('..')

import unittest

from common.constants import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, RESPONSE, ERROR
from server import process_client_message



# from common.constants import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, RESPONSE, ERROR
# from server import process_client_message


class TestServer(unittest.TestCase):
    dict_200 = {RESPONSE: 200}
    dict_400 = {RESPONSE: 400, ERROR: 'Bad Request'}

    def test_process_client_message_ok(self):
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 0, USER: {ACCOUNT_NAME: 'Guest'}}), self.dict_200)

    def test_process_client_message_no_actions(self):
        self.assertEqual(process_client_message(
            {TIME: 0, USER: {ACCOUNT_NAME: 'Guest'}}), self.dict_400)

    def test_process_client_message_no_time(self):
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.dict_400)

    def test_process_client_message_no_user(self):
        self.assertEqual(process_client_message({ACTION: PRESENCE, TIME: 0}), self.dict_400)

    def test_process_client_message_no_guest(self):
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 0, USER: {ACCOUNT_NAME: 'Igor'}}), self.dict_400)


if __name__ == '__main__':
    unittest.main()
