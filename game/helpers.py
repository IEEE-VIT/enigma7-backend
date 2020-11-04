from django.conf import settings


def encode(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string


def decode(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string


def return_encoded_list(array):
    encoded_list = []
    for var in array:
        encoded_list.append(encode(settings.ENCRYPTION_KEY , var))
    return encoded_list


def return_decoded_list(array):
    decoded_list = []
    for var in array:
        decoded_list.append(decode(settings.ENCRYPTION_KEY , var))
    return decoded_list


