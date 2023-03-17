import flask
from flask import Blueprint

from server.authentication.enums.authorization_level import AuthorizationLevel
from server.base_services import base_controller
from server.base_services.base_controller import ok_for_data, validate, error_for_data, ok
from server.constants.database_constants.data_type import DataType
from server.schemas import data_schemas
from server.services import data_service
from server.authentication import auth

data_controller = Blueprint('data_controller', __name__)


@data_controller.route('/regexPattern', methods=['GET'], endpoint='get_regex_pattern')
@auth.authorized(AuthorizationLevel.open_to_all)
async def get_regex_pattern():
    try:
        resp = data_service.get_regex_pattern()
        return ok_for_data(resp, True)
    except Exception as ex:
        return base_controller.error_handler(ex)


@data_controller.route('/regexPatternByName', methods=['GET'], endpoint='get_regex_pattern_by_name')
@auth.authorized(AuthorizationLevel.open_to_all)
async def get_regex_pattern_by_name():
    try:
        validate_response = validate(data_schemas.RegexPatternByName, flask.request.args)
        if validate_response.status:
            regex_name = flask.request.args.get("regexName", None)
            resp = ok(**data_service.get_regex_pattern_by_name(regex_name))
        else:
            resp = error_for_data(validate_response)

        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@data_controller.route('/filesType', methods=['GET'], endpoint='files_type')
@auth.authorized(AuthorizationLevel.open_to_all)
async def files_type():
    try:
        resp = await data_service.get_data_by_id(DataType.FilesType)
        return ok_for_data(resp, True)
    except Exception as ex:
        return base_controller.error_handler(ex)


@data_controller.route('/areaCode', methods=['GET'], endpoint='area_code')
@auth.authorized(AuthorizationLevel.open_to_all)
async def area_code():
    try:
        resp = await data_service.get_data_by_id("AreaCode")
        return ok_for_data(resp, True)
    except Exception as ex:
        return base_controller.error_handler(ex)


@data_controller.route('/getDataById', methods=['GET'], endpoint='get_data_by_id')
@auth.authorized(AuthorizationLevel.open_to_all)
async def get_data_by_id():
    try:
        validate_response = validate(data_schemas.GetDataById, flask.request.args)
        if validate_response.status:
            data_id = validate_response.data.get("dataId")
            resp = await data_service.get_data_by_id(data_id)
            return ok_for_data(resp, True)
        else:
            return error_for_data(validate_response)

    except Exception as ex:
        return base_controller.error_handler(ex)
