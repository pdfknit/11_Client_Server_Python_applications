import json
import sys

from lesson_03.constants import MAX_LENGTH, ENCODING


def get_message(client):
    encoded_response = client.recv(MAX_LENGTH)
    if isinstance(encoded_response, bytes):
        try:
            json_response = encoded_response.decode(ENCODING)
            response = json.loads(json_response)
            return response
        except ValueError:
            print('ValueError')



def send_message(sock, message):
    try:
        js_message = json.dumps(message)
        encoded_message = js_message.encode(ENCODING)
        sock.send(encoded_message)
    except TypeError:
        print('TypeError')
