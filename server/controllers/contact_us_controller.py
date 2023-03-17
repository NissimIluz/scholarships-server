import flask
from flask import Blueprint

from server.authentication.enums.authorization_level import AuthorizationLevel
from server.base_services import base_controller
from server.base_services.base_controller import validate, error_for_data
from server.schemas import contact_us_schemas
from server.services import contact_us_service
from server.authentication import auth

contact_us_controller = Blueprint('contact_us_controller', __name__)


@contact_us_controller.route('/organizationRegistration', methods=['post'], endpoint='organization_registration')
@auth.authorized(AuthorizationLevel.open_to_all)
async def get_user_data():
    try:
        organization_data = flask.request.json
        validator_result = validate(contact_us_schemas.OrganizationRegistration, data=organization_data)
        if validator_result.status:
            resp = await contact_us_service.organization_registration(organization_data)
        else:
            resp = error_for_data(validator_result)
        return resp
    except Exception as ex:
        return base_controller.error_handler(ex)
