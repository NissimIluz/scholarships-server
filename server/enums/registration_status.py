from enum import IntEnum


class RegistrationStatus(IntEnum):
    step1 = 1  # step1 completed
    step2 = 2  # step3 completed
    step3 = 3  # step2 completed
    blocked = 44
    # registered 200 or higher
    registered = 200
