from enum import IntEnum


class EContactUsStatus(IntEnum):
    open = 0,
    inner_mail_sent = 1,
    close = 10


class EContactUsOrigin(IntEnum):
    organization_registration = 0