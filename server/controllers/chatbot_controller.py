import flask
from flask import Blueprint
from werkzeug.datastructures import FileStorage

from server.authentication.enums.authorization_level import AuthorizationLevel
from server.constants import general_constants
from server.constants.error_constants import ErrorConstant
from server.base_services import base_controller
from server.services import chat_service
from server.authentication import auth

chatbot_controller = Blueprint('chatbot_controller', __name__)


@chatbot_controller.route('/startScholarshipSubmissionChat', methods=['POST'], endpoint='start_scholarship_submission_chat')
@auth.authorized(AuthorizationLevel.candidates)
async def start_scholarship_submission_chat():
    """
    :param json with the fields 'token' and 'scholarshipName'.
        token: the user token
        scholarshipName: the name of the required scholarship
    :return: json with the fields 'inProgress' and 'messages'
        inProgress: the status of the chatbot (True when the chatbot is still active).
        messages: Array with the messages for the user.
    """
    try:
        json_data = flask.request.json
        scholarships_names = json_data['scholarshipNames']
        return await chat_service.start_scholarship_submission_chat(scholarships_names)
    except Exception as ex:
        return base_controller.error_handler(ex)


@chatbot_controller.route('/scanAndNext', methods=['POST'], endpoint="scan_and_next")
@auth.authorized(AuthorizationLevel.candidates)
async def scan_and_next():
    """
    :param form-data with the fields 'token' and 'file'.
        token: the user token (use the identify the chat instances).
        file: the file that uploaded for scanning to the server.
    :return: json with the fields 'inProgress' and 'messages'
        inProgress: the status of the chatbot (True when the chatbot is still active).
        messages: Array with the messages for the user.
    """
    try:
        file: FileStorage = flask.request.files['file']
        if file.content_type == file.mimetype and file.mimetype in general_constants.accepted_file_list():
            return await chat_service.scholarship_submission_chat_scan_and_next(file)
        else:
            return base_controller.custom_error_resp(inProgress=True, messages=[ErrorConstant.InvalidFile.value])
    except Exception as ex:
        return base_controller.error_handler(ex)


@chatbot_controller.route('/closeScholarshipSubmissionChat', methods=['DELETE'], endpoint="close_scholarship_submission_chat")
@auth.authorized(AuthorizationLevel.candidates)
async def close_scholarship_submission_chat():
    try:
        await chat_service.close_scholarship_submission_chat()
        return base_controller.ok(inProgress=False, messages=[general_constants.DialogClose])
    except Exception as ex:
        return base_controller.error_handler(ex)