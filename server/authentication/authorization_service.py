import flask
from flask_login import login_user, UserMixin
from server import configuration
from server.authentication import token_service, auth_helper
from server.authentication.constants.dictionaries import collection_names_dictionary, usr_model_dictionary
from server.base_services.base_controller import error_resp
from server.constants import error_constants
from server.constants.fields_name.users.users_fields import UsersFields
from server.authentication.enums.authorization_level import AuthorizationLevel
from server.constants.database_constants.objnames import ObjNames
from server.constants.error_constants import ErrorConstant
from server.base_services import base_controller
from server.dal.dal_contracts.interface_users_dal import IUsersDal
from server.injector.dependency_injector import get_singleton
from server.logger import logger_service
from server.models.users.authorized_user import AuthorizedUser


async def get_authorization_error(authorization_level: AuthorizationLevel, authenticate_vs_db):
    try:

        if authorization_level != AuthorizationLevel.open_to_all:
            token = _get_token_from_request()
            user_data = token_service.decode_token(token)
        else:
            user_data = None

        headers = flask.request.headers

        # Checking whether the headers from the client are valid
        if not check_headers(headers, user_data):
            return base_controller.headers_not_accepted(headers, user_data[UsersFields.username],
                                                        AuthorizationLevel.authorized)
        # for helpDesk authorization check helpDesk conformation
        if authorization_level == AuthorizationLevel.help_desk_user or \
                authorization_level == AuthorizationLevel.help_desk_user:
            if not _valid_help_desk_client(headers):
                return base_controller.headers_not_accepted(headers, None, AuthorizationLevel.authorized)
        # If authorization_level is open to all - no additional validations are required
        elif authorization_level == AuthorizationLevel.open_to_all:
            return None

        # When the access request is for an authorized_candidates check if the authorized JWT is Candidate or
        # AuthorizedGuest
        if authorization_level == AuthorizationLevel.candidates:
            if user_data[UsersFields.user_identity] not in [ObjNames.Candidates,
                                                            ObjNames.AuthorizedGuests]:
                return base_controller.unauthorized(ErrorConstant.Unauthorized,
                                                    user_data[UsersFields.username])

        # else (the access request is not for an authorized_candidates) check whether the request is compatible to
        # JWT authorization level.
        elif collection_names_dictionary[authorization_level] != user_data[UsersFields.user_identity]:
            return base_controller.unauthorized(ErrorConstant.Unauthorized,
                                                user_data[UsersFields.username])

        # else (the access request is not for candidate and the request level is compatible to JWT
        # authorization level),
        # if authenticate_vs_db Checking whether the requested access authorization is for a registered candidate or
        # an organization contact. if true Checking the user against the DB. and then if all true load the user date
        # from DB to user_data
        elif authenticate_vs_db and collection_names_dictionary[authorization_level] in [ObjNames.Candidates,
                                                                  ObjNames.Contact]:

            db_error = await get_authorization_error_from_db(user_data, authorization_level)
            if db_error[0] is not None:
                return db_error[0]
            user_data = db_error[1]

        # else (all god - access request is compatible to JWT and DB authorization)
        else:
            '''do nothing here'''
        user = _get_usr_model(authorization_level)(user_data)
        login_user(user)
        return None
    except Exception as ex:
        return auth_helper.error(ex)


async def get_authorization_error_from_db(decoded_token, authorization_level: AuthorizationLevel):
    users_dal: IUsersDal = get_singleton(IUsersDal)
    try:
        user_details = await users_dal.get_user_information(decoded_token[UsersFields.username],
                                                            collection_names_dictionary[authorization_level],
                                                            get_by=UsersFields.username)
        if user_details is None:  # user not exist on DB
            logger_service.info(ErrorConstant.UserNotFound, decoded_token[UsersFields.username])
            return error_resp(error_constants.ErrorCode.Unauthorized, ErrorConstant.UserNotFound, 401), None

        # else all god
        else:
            return None, user_details

    except Exception as ex:
        return auth_helper.error(ex), None


def check_headers(headers, decoded_token=None):
    ret_val = True
    try:
        if configuration.development_mode:  # for development mode
            required_headers = ["User-Agent"]

        for required_header in required_headers:
            value = headers.get(required_header, None)
            if value is None:
                ret_val = False
            elif decoded_token is not None and value != decoded_token[required_header]:
                ret_val = False
    except Exception as ex:
        ret_val = False
        logger_service.warning(ex)
    return ret_val


def _get_usr_model(authorization_level: AuthorizationLevel) -> UserMixin:
    # default AuthorizedUser
    return usr_model_dictionary.get(authorization_level, AuthorizedUser)


def _get_token_from_request():
    brear = flask.request.headers.get('Authorization')
    if brear is not None and len(brear) > 1:
        return brear.split(' ')[1]
    else:
        return None


def _valid_help_desk_client(headers):
    return True