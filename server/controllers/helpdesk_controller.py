import flask
import pymongo as pymongo
from flask import Blueprint

from server.authentication.enums.authorization_level import AuthorizationLevel
from server.base_services import base_controller
from server.constants.fields_name.users.candidate_fields import CandidateFields
from server.schemas import helpdesk_schemas
from server.services import helpdesk_service
from server.authentication import auth

helpdesk_controller = Blueprint('helpdesk_controller', __name__)


@helpdesk_controller.route('/getStudents', methods=['GET'], endpoint='get_students')
@auth.authorized(AuthorizationLevel.help_desk_user)
async def get_students():
    try:
        validate_response = base_controller.validate(helpdesk_schemas.GetStudents, flask.request.args)
        if validate_response.status:
            arguments = validate_response.data
            resp = base_controller.ok(data=
                                      await helpdesk_service.get_students(int(arguments.get("skip")),
                                                                          int(arguments.get("take")),
                                                                          arguments.get("phoneNumber"),
                                                                          arguments.get("email"),
                                                                          arguments.get("firstName"),
                                                                          arguments.get("lastName"),
                                                                          arguments.get("id"),
                                                                          arguments.get("phrase"),
                                                                          arguments.get("onlyActive", True),
                                                                          arguments.get("orderBy",
                                                                                        CandidateFields.last_name),
                                                                          arguments.get("orderDirection",
                                                                                        pymongo.ASCENDING)))
        else:
            resp = base_controller.error_for_data(validate_response)
        return resp

    except Exception as ex:
        return base_controller.error_handler(ex)
