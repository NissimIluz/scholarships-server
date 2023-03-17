from marshmallow import Schema
from werkzeug.datastructures import ImmutableMultiDict, FileStorage
from server import configuration
from server.constants import general_constants
from server.constants.error_constants import ErrorConstant, ErrorCode
from server.models.response_dto import ResponseDto


def validate(schema: Schema, data) -> ResponseDto:
    if configuration.validate_input:
        schema = schema()
        validator_result = schema.validate(data)
        if len(validator_result) == 0:
            data = schema.load(data)
            ret_val = ResponseDto(True, data)
        else:  # input is invalid
            ret_val = ResponseDto(False, validator_result, ErrorCode.invalidData, ErrorConstant.InvalidInput)
    else:  # configuration.validate_input = false
        ret_val = ResponseDto(True, data)
    return ret_val


def validate_file(files, file_name: str, accepted_file_list: []) -> ResponseDto:
    ret_val = ResponseDto(False, None, ErrorCode.invalidFile, ErrorConstant.InvalidFile)
    try:
        if type(files) is ImmutableMultiDict:
            if file_name:
                file = files[file_name]
                if file and file_valid(file, accepted_file_list):
                    ret_val = ResponseDto(True, file)
            else:
                result: [] = []
                for key in files:
                    if not result and file_valid(files[key], accepted_file_list):
                        result.append({"key": key, "result": ErrorConstant.InvalidFile.value})
                if result:
                    ret_val = ResponseDto(False, result, ErrorCode.invalidFile, ErrorConstant.InvalidFile)
                else:
                    ret_val = ResponseDto(True, files[file_name])
    except:
        pass
    return ret_val


def file_valid(file, accepted_file_list):
    return file.content_type == file.mimetype and file.mimetype in general_constants.accepted_file_list()
