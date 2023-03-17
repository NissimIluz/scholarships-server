import math
import random
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
from server import configuration
from server.authentication import auth_helper, token_service
from server.constants import error_constants
from server.constants.database_constants.objnames import ObjNames
from server.constants.fields_name.general_fields import GeneralFields
from server.constants.fields_name.otp_fields import OtpFields
from server.constants.fields_name.users.candidate_fields import CandidateFields
from server.constants.fields_name.users.users_fields import UsersFields
from server.dal.dal_contracts.interface_users_dal import IUsersDal
from server.authentication.enums.enter_action_enum import EnterAction
from server.enums.registration_status import RegistrationStatus
from server.enums.update_user_login_data import UpdateUserLoginData
from server.injector.dependency_injector import get_singleton
from server.logger import logger_service
from server.authentication.schemas.login_schemas import LoginSchema, LoginByOtpStep1Schema, LoginByOtpStep2Schema
from server.models.users import authorized_user
from server.services import email_service

users_dal: IUsersDal = get_singleton(IUsersDal)


async def login(json_data, user_identity):
    validator = LoginSchema()
    validator_result = validator.validate(data=json_data)
    if len(validator_result) == 0:
        resp = await users_dal.get_user_information(json_data[UsersFields.username], user_identity,
                                                    action=EnterAction.login)
        ret_val = auth_helper.error_resp(code=error_constants.ErrorCode.UserLoginError, status=401)
        if resp is not None:
            user_blocked_response = await _check_if_user_blocked(resp, user_identity)
            if user_blocked_response is not None:
                ret_val = user_blocked_response
            else:  # user allow continuing (not blocked)
                if check_password_hash(resp[UsersFields.password], json_data[UsersFields.password]):
                    ret_val = await logged_in_user(resp, user_identity)
                else:
                    logger_service.warning(error_constants.ErrorConstant.Incorrect_password,
                                           json_data[UsersFields.username])
        else:
            logger_service.warning(error_constants.ErrorConstant.IncorrectUsername, json_data[UsersFields.username])
    else:
        logger_service.error(validator_result)
        ret_val = auth_helper.error_resp(validator_result)
    return ret_val


async def login_by_otp_step_1(json_data, user_identity):
    validator = LoginByOtpStep1Schema()
    validator_result = validator.validate(data=json_data)
    if len(validator_result) == 0:
        email = json_data.get(UsersFields.email, None)
        phone_number = json_data.get(UsersFields.phone_number, None)
        if email is not None and email != '':
            value = email
            key = UsersFields.email
        elif phone_number is not None and phone_number != '':
            value = phone_number
            key = UsersFields.phone_number
        resp = await users_dal.get_user_information(user_identity=value,
                                                    user_identity_collection=user_identity,
                                                    action=EnterAction.login,
                                                    get_by=key)
        if resp is not None:
            user_blocked_response = await _check_if_user_blocked(resp, user_identity)
            if user_blocked_response is not None:
                ret_val = user_blocked_response
            else:  # user allow continuing
                ret_val = await _send_otp(user_identity, resp[UsersFields.username], value, email, phone_number)

        elif user_identity == ObjNames.Candidates:
            ret_val = await _send_otp(user_identity, None, value, email, phone_number)
        else:
            logger_service.warning(
                str(email) + " or " + str(phone_number) + ": " + error_constants.ErrorConstant.NotFound.value
            )
            ret_val = auth_helper.error_resp(code=error_constants.ErrorCode.UserLoginError, status=401)
    else:
        logger_service.error(validator_result)
        ret_val = auth_helper.custom_error_resp(400, validator_result)
    return ret_val


async def login_by_otp_step_2(json_data):
    validator = LoginByOtpStep2Schema()
    validator_result = validator.validate(data=json_data)
    if len(validator_result) == 0:
        otp_code = json_data.get(OtpFields.otp, None)
        email = json_data.get(UsersFields.email, None)
        phone_number = json_data.get(UsersFields.phone_number, None)
        if otp_code is not None:
            if email is not None and email != '':
                otp_obj = await users_dal.get_user_last_otp(email)
                key_identity = UsersFields.email  # "email"
            elif phone_number is not None:
                otp_obj = await users_dal.get_user_last_otp(phone_number)
                key_identity = UsersFields.phone_number  # "phoneNumber"
        if otp_obj is not None:
            if otp_obj[OtpFields.attempts] < configuration.otp_max_attempt:
                if otp_obj[OtpFields.otp] == otp_code:
                    resp = await users_dal.get_user_information(
                        user_identity=otp_obj[OtpFields.username],
                        user_identity_collection=otp_obj[OtpFields.user_identity],
                        action=EnterAction.login,
                        get_by=UsersFields.id
                    )
                    if resp is not None:
                        if resp[UsersFields.last_login] < otp_obj[OtpFields.create_date]:
                            ret_val = await logged_in_user(resp, otp_obj[OtpFields.user_identity])
                        else:  # otp has been used
                            logger_service.info(otp_code + ": " + error_constants.ErrorConstant.UsedOtp.value,
                                                otp_obj[OtpFields.username])
                            ret_val = auth_helper.error_resp(code=error_constants.ErrorCode.UsedOtp, status=401)

                    # else (user not exit). Checking whether the access request is for candidate
                    elif otp_obj[OtpFields.user_identity] == ObjNames.Candidates:
                        ret_val = await _register_authorized_guest(email, phone_number, key_identity, otp_obj)

                    else:  # else (user not exit and the access request is not for candidate
                        logger_service.critical(otp_code + ": " + error_constants.ErrorConstant.OtpNotFound.value,
                                                otp_obj[OtpFields.username])
                        ret_val = auth_helper.error_resp(code=error_constants.ErrorCode.UserLoginError, status=401)
                else:  # incorrect otp code
                    logger_service.info(otp_code + ": " + error_constants.ErrorConstant.IncorrectOtp.value,
                                        otp_obj[OtpFields.username])
                    ret_val = auth_helper.error_resp(code=error_constants.ErrorCode.UserLoginError, status=401)
            else:  # otp login attempts is bigger than configuration.otp_max
                logger_service.info(otp_code + ": " + error_constants.ErrorConstant.OtpLoginAttempts.value,
                                    otp_obj[OtpFields.username])
                ret_val = auth_helper.error_resp(code=error_constants.ErrorCode.OtpLoginAttempts, status=401)
        else:  # this user doesn't have otp
            logger_service.warning(otp_code + ": " + error_constants.ErrorConstant.OtpNotFound.value,
                                   str(email) + " or " + str(phone_number))
            ret_val = auth_helper.error_resp(code=error_constants.ErrorCode.OtpNotFound,
                                             message=error_constants.ErrorConstant.OtpNotFound,
                                             status=401)
    else:  # invalid input
        logger_service.error(validator_result)
        ret_val = auth_helper.error_resp(validator_result)
    return ret_val


async def logged_in_user(user_data, user_identity):
    is_registered = True
    if user_identity == ObjNames.Candidates:
        if user_data[CandidateFields.registration_status] < RegistrationStatus.registered.value:
            is_registered = False
            if user_data[CandidateFields.registration_status] <= RegistrationStatus.registered.step3:
                user_identity = ObjNames.SignedUp
            else:
                user_identity = None
    token = token_service.create_token(user_data, is_registered, user_identity)
    resp = authorized_user.filter_user_data(user_data)
    resp[GeneralFields.token] = token
    resp[UsersFields.is_registered] = is_registered
    await users_dal.set_user_last_login(user_identity, resp[UsersFields.username])
    return auth_helper.ok(resp)


async def _register_authorized_guest(email, phone_number, key_identity, otp_data):
    user_data = await users_dal.insert_guests(email, phone_number, key_identity,
                                              otp_data[OtpFields.key])

    token = token_service.create_token(user_data, False, ObjNames.AuthorizedGuests,
                                       configuration.exp_token_for_guests)
    return auth_helper.ok({GeneralFields.token: token, UsersFields.is_registered: False})


async def _check_if_user_blocked(user_data, user_identity):
    ret_val = None
    if user_data[UsersFields.login_attempt] > configuration.max_login_attempt:
        logger_service.info(error_constants.ErrorConstant.UserPermanentlyBlocked,
                            user_data[UsersFields.username])
        ret_val = auth_helper.error_resp(error_constants.ErrorCode.UserPermanentlyBlocked, status=401)
    elif user_data[UsersFields.login_attempt] > 0 \
            and user_data[UsersFields.login_attempt] % configuration.block_after_login_attempt == 0 \
            and user_data[UsersFields.last_login_attempt] > datetime.now() - timedelta(
                minutes=configuration.block_user_for):
        await users_dal.reset_user_login_data(user_identity, user_data, UpdateUserLoginData.blocked_user)
        ret_val = auth_helper.custom_error_resp(401,
                                                code=error_constants.ErrorCode.UserTemporarilyBlocked.value,
                                                message=error_constants.ErrorConstant.UserTemporarilyBlocked.value,
                                                userBlockedUntil=user_data[UsersFields.last_login_attempt] + timedelta(
                                                    minutes=configuration.block_user_for)
                                                )
        logger_service.info(error_constants.ErrorConstant.UserTemporarilyBlocked,
                            user_data[UsersFields.username])
    return ret_val


async def _send_otp(user_identity, username, user_value, email, phone_number):
    otp = _generate_otp()
    sent_status = False
    await users_dal.set_user_otp(otp, username, user_value, user_identity)
    if configuration.print_otp:
        print('this otp is: ', otp)
    try:
        if configuration.send_otp_to_email and email is not None:
            sent_status = await email_service.send_otp_email(email, otp)
        elif configuration.send_otp_to_phone_number and phone_number is not None:
            x = 5
            # sent_status = await sms_service.send_otp_sms(email, otp)
    except Exception as ex:
        logger_service.critical(error_constants.ErrorConstant.OtpNotSend.value + ": " + str(ex))

    ''' in production most be removed'''
    if configuration.development_mode and configuration.return_otp:  # most to be removed in production
        logger_service.critical("otp sent to user in the response", username)
        return auth_helper.ok(sentStatus=sent_status, otp=otp,
                                  message="this otp will not be sent in production.The otp has been sent due to client side developer request for develop the otp mechanism. ",
                                  error="otp sent to user in the response " + str(username))

    '''until here - in production most be removed'''

    if sent_status:
        ret_val = auth_helper.ok(sentStatus=sent_status)
    else:
        ret_val = auth_helper.error_resp(code=error_constants.ErrorCode.OtpNotSent)
    return ret_val


def _generate_otp():
    digits = configuration.otp_digits
    n = len(digits)
    otp = ""
    # length of password can be changed
    for i in range(configuration.otp_length):
        otp += digits[math.floor(random.random() * n)]
    return otp
