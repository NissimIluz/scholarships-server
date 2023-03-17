import string

from server import configuration

'''  Blocks  '''
default_length = '{5,50}'
en_letters = string.ascii_letters
printable = string.printable
he_letters = 'א-ת'
digits = string.digits
basic_character = '!@#$%&*().,_"\' '
all_non_letters = '.,!?:;_|+\*\\/=%°@&#§$"\'^ˇ()\[\]<>{}'

'''  Regular Expression   '''


class RegularExpression:
    en_regex = f'^[{en_letters + digits + basic_character}]{default_length}$'
    en_letters_only_regex = f'^[{en_letters}]{default_length}$'
    he_regex = f'^[{he_letters + digits + basic_character}]{default_length}$'
    he_letters_only_regex = f'^[{he_letters}]{default_length}$'

    password = en_regex
    phone = f'^[+][{digits}]{{10,15}}$'
    otp = f'^[{configuration.otp_digits}]' + '{' + str(configuration.otp_length) + '}$'
    username = f'^[{en_letters + digits}@.#*]{default_length}$'
    name = f'^((?![{all_non_letters}]).)+$'
    field_name = f'^[{en_letters + "_"}]' + '{2,25}$'
    number = f'^[{string.digits}]{{5,15}}$'
    id_umber = f'^[{string.digits}]{{8,9}}$'
    street_number = f'^[{string.digits}]{{1,5}}$'
    zip_code = f'^[{string.digits}]{{5,8}}$'

    @classmethod
    def get_child_dict(cls):
        return {k: v for k, v in cls.__dict__.items() if not k.startswith('_')}


# ^((?![.,!?:;_|+\\*\/=%°@&#§$\"'^ˇ()\\[\\]<>{}])[\\S])+$
