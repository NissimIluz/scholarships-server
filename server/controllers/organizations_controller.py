import flask
from flask import Blueprint

from server.authentication.enums.authorization_level import AuthorizationLevel
from server.base_services import base_controller
from server.services import organizations_service
from server.authentication import auth

organizations_controller = Blueprint('organizations_controller', __name__)


@organizations_controller.route('/addOrganization', methods=['POST'], endpoint='add_organization')
@auth.authorized(AuthorizationLevel.help_desk_user)
async def add_organization():
    try:
        json_data = flask.request.json
        resp = await organizations_service.add_organization(json_data)
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@organizations_controller.route('/login', methods=['POST'], endpoint='login')
@auth.authorized(AuthorizationLevel.open_to_all)
async def login():
    try:
        json_data = flask.request.json
        resp = await organizations_service.login(json_data)
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@organizations_controller.route('/loginByOtpStep1', methods=['POST'], endpoint='login_by_otp_step_1')
@auth.authorized(AuthorizationLevel.open_to_all)
async def login_by_otp_step_1():
    """
    :param json with 'username' and 'password'.
    :return: status
    """
    try:
        json_data = flask.request.json
        resp = await organizations_service.login_by_otp_step_1(json_data)
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@organizations_controller.route('/loginByOtpStep2', methods=['POST'], endpoint='login_by_otp_step_2')
@auth.authorized(AuthorizationLevel.open_to_all)
async def login_by_otp_step_2():
    """
    :param json with 'otp'
    :return: json with encrypted token and user date
    """
    try:
        json_data = flask.request.json
        resp = await organizations_service.login_by_otp_step_2(json_data)
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@organizations_controller.route('/addContacts', methods=['POST'], endpoint='add_contacts')
@auth.authorized(AuthorizationLevel.organizations, True)
async def add_contacts():
    try:
        json_data = flask.request.json
        resp = await organizations_service.add_contacts(json_data)
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@organizations_controller.route('/updateContact', methods=['PUT'], endpoint='update_contact')
@auth.authorized(AuthorizationLevel.organizations, True)
async def update_contact():
    try:
        json_data = flask.request.json
        resp = await organizations_service.update_contact(json_data)
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@organizations_controller.route('/deleteContact', methods=['DELETE'], endpoint='delete_contact')
@auth.authorized(AuthorizationLevel.organizations, True)
async def delete_contact():
    try:
        username_to_delete = flask.request.args.get("usernameToDelete", None)
        resp = await organizations_service.delete_contact(username_to_delete)
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@organizations_controller.route('/updateOrganization', methods=['PUT'], endpoint='update_organization')
@auth.authorized(AuthorizationLevel.organizations, True)
async def update_organization():
    try:
        json_data = flask.request.json
        resp = await organizations_service.update_organization(json_data)
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@organizations_controller.route('/deleteOrganization', methods=['DELETE'], endpoint='delete_organization')
@auth.authorized(AuthorizationLevel.organizations, True)
async def delete_organization():
    try:
        resp = await organizations_service.delete_organization()
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@organizations_controller.route('/getOrganizationContacts', methods=['GET'], endpoint='get_organization_contact')
@auth.authorized(AuthorizationLevel.organizations, True)
async def get_organization_contact():
    try:
        resp = await organizations_service.get_contacts()
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@organizations_controller.route('/getOrganizationData', methods=['GET'], endpoint='get_organization_data')
@auth.authorized(AuthorizationLevel.organizations)
async def get_organization_data():
    try:
        resp = await organizations_service.get_organization_data()
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@organizations_controller.route('/getUserData', methods=['GET'], endpoint='get_user_data')
@auth.authorized(AuthorizationLevel.organizations, True)
async def get_user_data():
    try:
        username_to_delete = flask.request.args.get("usernameToGet", None)
        resp = await organizations_service.get_user_data(username_to_delete)
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)