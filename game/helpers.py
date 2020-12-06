from django.conf import settings
import re


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
        encoded_list.append(encode(settings.ENCRYPTION_KEY, var))
    return encoded_list


def return_decoded_list(array):
    decoded_list = []
    for var in array:
        decoded_list.append(decode(settings.ENCRYPTION_KEY, var))
    return decoded_list


def is_valid_answer(answer):
    string_check = re.compile('[@_#$%^&*()<>?/\|}{~:]')
    if string_check.search(answer) is None:
        return True
    return False


def is_correct_answer(question, answer):
    decoded_answers = return_decoded_list(question.answer)
    if answer.lower() in map(lambda x: x.lower(), decoded_answers):
        return True
    return False


def is_close_answer(question, answer):
    decoded_answers = return_decoded_list(question.close_answers)
    if answer.lower() in map(lambda x: x.lower(), decoded_answers):
        return True
    return False


def calculate_points(solves, hint_used):
    if hint_used:
        hint_cost = 10
    else:
        hint_cost = 0

    if solves <= 10:
        points = 100 - hint_cost
    elif solves > 10 and solves <= 20:
        points = 90 - hint_cost
    elif solves > 20 and solves <= 30:
        points = 85 - hint_cost
    else:
        points = 75 - hint_cost
    return points
