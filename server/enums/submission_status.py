from enum import IntEnum


class SubmissionStatusEnum(IntEnum):
    submitted = 0,
    approved = 10,
    denied = 20

    @classmethod
    def has_value(cls, value) -> bool:
        return value in cls._value2member_map_


