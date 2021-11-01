from typing import Dict
from random import randint, choice
from string import (ascii_lowercase, ascii_uppercase,
                    ascii_letters, digits, hexdigits,
                    printable, whitespace)


def get_random_key_value():
    keyword_data_key = [*ascii_lowercase, *ascii_uppercase]
    keyword_data_value = [*ascii_lowercase, *ascii_uppercase, *ascii_letters,
                    *digits, *hexdigits, *printable, *whitespace,
                    '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹', '۰', '-', '=',
                    'ض', 'ص', 'ث', 'ق', 'ف', 'غ', 'ع', 'ه', 'خ', 'ح', 'ج', 'چ', 'ش', 'س', 'ی', 'ب', 'ل', 'ا', 'ت', 'ن', 'م', 'ک', 'گ', 'ظ', 'ط', 'ز', 'ر', 'ر', 'ذ', 'د', 'پ', 'و', '.', '‍', '/', ''
                    ]
    key = ''
    value = ''

    for _ in range(randint(5, 20)):
        key = key+choice(keyword_data_key)

    for _ in range(randint(5, 20)):
        value = value+choice(keyword_data_value)

    return key, value


def dict_creator(max_deep: int = 5) -> Dict:
    random_dict = {}

    for _ in range(randint(1, 10)):
        first_key, first_value = get_random_key_value()
        random_dict[first_key] = first_value

        for _ in range(randint(0, max_deep)):
            new_key = get_random_key_value()[1]
            random_dict = {new_key: random_dict}

    return random_dict


if __name__ == '__main__':
    print(dict_creator())
