import random
import string


def get_random_string() -> str:
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for _ in range(8))
    return result_str
