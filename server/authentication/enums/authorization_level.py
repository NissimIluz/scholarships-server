from enum import IntEnum


class AuthorizationLevel(IntEnum):
    open_to_all = 0,
    authorized = 1
    registered_candidate = 2,
    candidates = 3,
    signed_up = 7,
    organizations = 10,
    help_desk = 50
    help_desk_user = 51



