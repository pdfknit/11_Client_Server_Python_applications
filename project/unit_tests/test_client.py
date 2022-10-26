import sys
sys.path.append('..')

import unittest

from client import create_presence_message, answer_from_server
from common.constants import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, RESPONSE, ERROR


class TestClient(unittest.TestCase):
    def test_create_presence_message(self):
        test_function = create_presence_message()
        self.assertEqual(test_function, {ACTION: PRESENCE, TIME: test_function[TIME],
                                         USER: {ACCOUNT_NAME: 'Guest'}})

    def test_answer_from_server_200(self):
        self.assertEqual(answer_from_server({RESPONSE: 200}), '200 : OK')

    def test_answer_from_server_400(self):
        self.assertEqual(answer_from_server({RESPONSE: 400, ERROR: 'Bad Request'}),
                         '400 : Bad Request')

    def test_no_response(self):
        self.assertRaises(KeyError, answer_from_server, {})


if __name__ == '__main__':
    unittest.main()
