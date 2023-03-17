from enum import Enum
from server.base_services import base_controller
from server.constants.error_constants import ErrorConstant


def ok(*args, **kwargs):
    return base_controller.ok(*args, **kwargs)


def error(ex):
    return base_controller.unauthorized(ex, ErrorConstant.NoUserName.value)


def error_resp(code: Enum, message: Enum = None, status=400):
    return base_controller.error_resp(code, message, status)


def custom_error_resp(status,  *args, **kwargs):
    return base_controller.custom_error_resp(status,  *args, **kwargs)