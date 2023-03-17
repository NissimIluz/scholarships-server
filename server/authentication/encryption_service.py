from cryptography.fernet import Fernet
from server import configuration

_key = configuration.encryption_key
cipher_suite = Fernet(_key)


def decode(value):
    decoded_value = cipher_suite.decrypt(value)
    return decoded_value.decode()


def encrypt(value):
    encoded_value = cipher_suite.encrypt(value.encode())
    return encoded_value

