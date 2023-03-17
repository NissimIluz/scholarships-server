from abc import abstractmethod
from enum import Enum
from server.constants.error_constants import ErrorCode
from server.models.data_obj import Data


class ResponseDto:
    def __init__(self, status: bool = True, data: Data or any = None, code=None, message=None):
        self.status = status
        self.data = data
        self.message = self.get_message(message)
        self.code = self.get_code(code)

    def get_code(self, code):
        if code is None:
            if self.status:
                code = 200
            else:
                code = ErrorCode.GenericError
        code = code
        if isinstance(code, Enum):
            if self.message is None:
                self.message = code.name
            code = code.value
        else:
            code = code
        return code

    @abstractmethod
    def get_message(self, message):
        if isinstance(message, Enum):
            message = message.value
        else:
            message = message
        return message

