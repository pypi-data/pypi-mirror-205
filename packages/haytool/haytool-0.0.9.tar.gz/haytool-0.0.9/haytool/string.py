import secrets
import string
import random


def generate_random_string(string_length=None, words=1, freestyle=False):
    gen_words = []
    words = random.randint(3, 20) if freestyle else 1
    for word in range(words):
        string_length = random.randint(2, 12) if string_length is None else string_length
        rando_word = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(string_length))
        gen_words.append(rando_word)
        string_length = None
    return ' '.join(gen_words)


def generate_random_numbers(num_length, start_zero=False):
    return ''.join([str(random.randint(0 if start_zero else 1, 9)) for x in range(num_length)])
