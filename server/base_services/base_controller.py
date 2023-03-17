import inspect
from enum import Enum
from types import NoneType
import flask
from flask import jsonify
from server.constants import general_constants
from server.constants.error_constants import ErrorCode, ErrorConstant
from server.authentication.enums.authorization_level import AuthorizationLevel
from server.logger import logger_service
from server.models.response_dto import ResponseDto
from server.services import validator_service

convert_able = (int, str, bool, NoneType, dict)


def ok(*args, **kwargs):
    if kwargs or not args:
        kwargs.update(status=True)
    return jsonify(*args, **kwargs), 200


# use this for ok response withe data is instance ResponseDto
def ok_for_data(data: ResponseDto or any, included_status=False, status=200):
    if inspect.isclass(type(data)) and type(data) is not list:
        data = class_to_dict(data)
    if included_status:
        return jsonify(data=data, status=True), status
    else:
        return jsonify(data), status


def ok_code(code: Enum):
    return ok_for_data(ResponseDto(data=code.value))


def error_resp(code: Enum, message: Enum = None, status=400):
    data = ResponseDto(False, code=code, message=message)
    return error_for_data(data, status)


# user this for error response withe data is instance ResponseDto
def error_for_data(data: ResponseDto or any, status=400, included_status=False):
    if inspect.isclass(type(data)):
        data = class_to_dict(data)
    if included_status:
        return jsonify(data=data, status=False), status
    else:
        return jsonify(data), status


def custom_error_resp(status_code=400, *args, **kwargs):
    if kwargs or not args:
        kwargs.update(status=False)
    return jsonify(*args, **kwargs), status_code


def response_for_dto(dto: ResponseDto or any):
    response = class_to_dict(dto)
    if dto.status:
        return ok(response)
    else:
        return error_resp(response)


def validate(schema, data) -> ResponseDto:
    return validator_service.validate(schema, data)


def validate_file(files=None, file_name=None, accepted_file_list=general_constants.accepted_file_list()) -> ResponseDto:
    if files is None:
        files = flask.request.files
    return validator_service.validate_file(files, file_name, accepted_file_list)


def error_handler(ex):
    logger_service.critical(ex)
    return error_resp(code=ErrorCode.GenericError, status=400)


def unauthorized(ex, username):
    logger_service.info(ex, username)
    return error_resp(code=ErrorCode.Unauthorized, status=401)


def headers_not_accepted(headers, username, authorization: AuthorizationLevel):
    logger_service.warning(f'{authorization.name}: {ErrorConstant.StolenToken.value} {str(headers)}', username)
    return error_resp(code=ErrorCode.Unauthorized, status=401)


def class_to_dict(clss_instance):
    dict_class = {}
    for member in inspect.getmembers(clss_instance):
        if not member[0].startswith('_') and not inspect.ismethod(member[1]):
            if type(member[1]) is list:
                dict_class[member[0]] = convert_list(member[1])
            elif type(member[1]) in convert_able:
                dict_class[member[0]] = member[1]
            else:
                dict_class[member[0]] = class_to_dict(member[1])
    return dict_class


def convert_list(list_to_convert):
    new_list = []
    for item in list_to_convert:
        if inspect.isclass(type(item)) and type(item) not in convert_able:
            new_list.append(class_to_dict(item))
        else:
            new_list.append(item)
    return new_list
