import flask
from flask import Blueprint
from server.authentication.enums.authorization_level import AuthorizationLevel
from server.base_services import base_controller
from server.base_services.base_controller import validate, error_for_data, validate_file
from server.constants.fields_name.users.candidate_fields import CandidateFields
from server.schemas import student_registration
from server.services import candidates_service
from server.authentication import auth

candidates_controller = Blueprint('candidates_controller', __name__)


@candidates_controller.route('/addCandidates', methods=['POST'], endpoint='add_candidates')
@auth.authorized(AuthorizationLevel.help_desk_user)
async def add_candidates():
    try:
        json_data = flask.request.json
        resp = await candidates_service.add_candidate(json_data)
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@candidates_controller.route('/registerStep1', methods=['POST'], endpoint='register_step1')
@auth.authorized(AuthorizationLevel.open_to_all)
async def register_step1():
    try:
        step1 = flask.request.form
        validate_data_response = validate(student_registration.RegistrationStep1, step1)
        if not validate_data_response.status:
            return error_for_data(validate_data_response)
        validate_file_response = validate_file(flask.request.files, CandidateFields.id_file)
        if not validate_file_response.status:
            return error_for_data(validate_file_response)
        return await candidates_service.register_step1(validate_data_response.data, validate_file_response.data)
    except Exception as ex:
        return base_controller.error_handler(ex)


@candidates_controller.route('/registerStep2', methods=['POST'], endpoint='register_step2')
@auth.authorized(AuthorizationLevel.signed_up)
async def register_step2():
    try:
        step2 = flask.request.form
        validate_data_response = validate(student_registration.RegistrationStep2, step2)
        if not validate_data_response.status:
            resp = error_for_data(validate_data_response)
        else:
            validate_file_response = validate_file(flask.request.files, CandidateFields.student_permit)
            if not validate_file_response.status:
                resp = error_for_data(validate_file_response)
            else:
                resp = await candidates_service.register_step2(validate_data_response.data, validate_file_response.data)
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@candidates_controller.route('/registerStep3', methods=['POST'], endpoint='register_step3')
@auth.authorized(AuthorizationLevel.signed_up)
async def register_step3():
    try:
        step3 = flask.request.form
        validate_response = validate(student_registration.RegistrationStep3, step3)
        if validate_response.status:
            resp = await candidates_service.register_step3(validate_response.data)
        else:
            resp = error_for_data(validate_response)
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@candidates_controller.route('/registerStep4', methods=['POST'], endpoint='register_step4')
@auth.authorized(AuthorizationLevel.signed_up)
async def register_step4():
    try:
        step4 = flask.request.form
        validate_response = validate(student_registration.RegistrationStep4, step4)
        if validate_response.status:
            resp = await candidates_service.register_step4(validate_response.data)
        else:
            resp = error_for_data(validate_response)
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@candidates_controller.route('/loginByOtpStep1', methods=['POST'], endpoint='login_by_otp_step_1')
@auth.authorized(AuthorizationLevel.open_to_all)
async def login_by_otp_step_1():
    """
    :param json with 'username' and 'password'.
    :return: json with encrypted token and identifier ("confident" or "organization")
    """
    try:
        json_data = flask.request.json
        resp = await candidates_service.login_by_otp_step_1(json_data)
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@candidates_controller.route('/loginByOtpStep2', methods=['POST'], endpoint='login_by_otp_step_2')
@auth.authorized(AuthorizationLevel.open_to_all)
async def login_by_otp_step_2():
    """
    :param json with 'otp'
    :return: json with encrypted token and identifier ("confident" or "organization")
    """
    try:
        json_data = flask.request.json
        resp = await candidates_service.login_by_otp_step_2(json_data)
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@candidates_controller.route('/updateCandidate', methods=['PUT'], endpoint='update_user')
@auth.authorized(AuthorizationLevel.registered_candidate, True)
async def update_user():
    try:
        json_data = flask.request.json
        resp = await candidates_service.update(json_data)
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@candidates_controller.route('/deleteCandidate', methods=['DELETE'], endpoint='delete_user')
@auth.authorized(AuthorizationLevel.registered_candidate, True)
async def delete_user():
    try:
        resp = await candidates_service.delete()
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)


@candidates_controller.route('/getUserData', methods=['GET'], endpoint='get_user_data')
@auth.authorized(AuthorizationLevel.registered_candidate, True)
async def get_user_data():
    try:
        resp = candidates_service.get_user_data()
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)
