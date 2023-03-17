import flask
from flask import Blueprint

from server.authentication.enums.authorization_level import AuthorizationLevel
from server.constants import general_constants
from server.base_services import base_controller
from server.services import scholarships_service
from server.authentication import auth

scholarships_controller = Blueprint('scholarships_controller', __name__)


@scholarships_controller.route('', methods=['GET'], endpoint='get_scholarships')
@auth.authorized(AuthorizationLevel.open_to_all)
async def get_scholarships():
    try:
        ret_val = await scholarships_service.get_scholarships()
        return ret_val
    except Exception as ex:
        return base_controller.error_handler(ex)


@scholarships_controller.route('add', methods=['POST'], endpoint='add_scholarships')
@auth.authorized(AuthorizationLevel.organizations, True)
async def add_scholarships():
    try:
        json_data = flask.request.json
        ret_val = await scholarships_service.add_scholarships(json_data)
        return ret_val
    except Exception as ex:
        return base_controller.error_handler(ex)


@scholarships_controller.route('/update', methods=['PUT'], endpoint='update_scholarships')
@auth.authorized(AuthorizationLevel.organizations, True)
async def update_scholarships():
    try:
        json_data = flask.request.json
        resp = await scholarships_service.update_scholarships(json_data)
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@scholarships_controller.route('/delete', methods=['DELETE'], endpoint='delete_scholarships')
@auth.authorized(AuthorizationLevel.organizations, True)
async def delete_scholarships():
    try:
        scholarship_id = flask.request.args.get("scholarshipName")
        resp = await scholarships_service.delete_scholarships(scholarship_id)
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@scholarships_controller.route('/getOrganizationScholarships', methods=['GET'], endpoint='get_organization_scholarships')
@auth.authorized(AuthorizationLevel.organizations)
async def get_organization_scholarships():
    try:
        included_submissions_str = flask.request.args.get("includedSubmissions", 'false')
        included_submissions = included_submissions_str.lower() in general_constants.true_string
        resp = await scholarships_service.get_organization_scholarships(included_submissions=included_submissions)
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)
