import flask

from server.authentication.enums.authorization_level import AuthorizationLevel
from server.base_services.base_controller import ok
from server.base_services import base_controller
from server.services import submissions_service
from server.authentication import auth

submissions_controller = flask.Blueprint('submissions_controller', __name__)


@submissions_controller.route('submit', methods=['POST'], endpoint='submit')
@auth.authorized(AuthorizationLevel.candidates, True)
async def submit():
    try:
        data = flask.request.json
        ret_val = await submissions_service.submit(data)
        return ret_val
    except Exception as ex:
        return base_controller.error_handler(ex)


@submissions_controller.route('getUserSubmissions', methods=['GET'], endpoint='get_user_submissions')
@auth.authorized(AuthorizationLevel.candidates)
async def get_user_submissions():
    try:
        ret_val = await submissions_service.get_user_submissions()
        return ok(ret_val)
    except Exception as ex:
        return base_controller.error_handler(ex)


@submissions_controller.route('responseToSubmission', methods=['PUT'], endpoint='response_to_submission')
@auth.authorized(AuthorizationLevel.organizations)
async def response_to_submission():
    try:
        data = flask.request.json
        ret_val = await submissions_service.response_to_submission(data)
        return ret_val
    except Exception as ex:
        return base_controller.error_handler(ex)


@submissions_controller.route('getAllSubmissionsToOrganization', methods=['GET'], endpoint='get_all_submissions_to_organization')
@auth.authorized(AuthorizationLevel.organizations)
async def get_all_submissions_to_organization():
    try:
        ret_val = await submissions_service.get_all_submissions_to_organization()
        return ok(ret_val)
    except Exception as ex:
        return base_controller.error_handler(ex)