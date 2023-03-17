from flask_login import current_user
from werkzeug.security import generate_password_hash
from server.base_services.base_controller import ok, error_resp, ok_code
from server.constants import error_constants
from server.constants.database_constants.objnames import ObjNames
from server.constants.fields_name.organization_fields import OrganizationFields
from server.constants.fields_name.users.users_fields import UsersFields
from server.dal.dal_contracts.interface_organizations_dal import IOrganizationsDal
from server.dal.dal_contracts.interface_scholarships_dal import IScholarshipsDal
from server.dal.dal_contracts.interface_users_dal import IUsersDal
from server.injector.dependency_injector import get_singleton
from server.logger import logger_service
from server.models.responses import DatabaseResponse
from server.authentication import auth, token_service
from server.models.users.authorized_user import filter_user_data

organization_dal: IOrganizationsDal = get_singleton(IOrganizationsDal)
user_dal: IUsersDal = get_singleton(IUsersDal)
scholarship_dal: IScholarshipsDal = get_singleton(IScholarshipsDal)


async def add_contacts(contacts, new_organization=False, organization_name=None, organization_id=None):
    for contact in contacts:
        contact[UsersFields.password] = generate_password_hash(contact[UsersFields.password])
    resp: DatabaseResponse = await user_dal.add_contacts(contacts, new_organization, organization_name, organization_id)
    if resp.status:
        token = token_service.create_token(contacts[0], True, ObjNames.Contact)
        ret_val = ok(token=token)
    else:
        ret_val = error_resp(code=resp.message)
    return ret_val


async def add_organization(data):
    contacts = data.pop("contacts")
    if len(contacts) > 0:
        resp: DatabaseResponse = await organization_dal.add_organization(data)
        if resp.status:
            ret_val = await add_contacts(contacts, new_organization=True, organization_name=data[OrganizationFields.organization_name], organization_id=resp.information)
            if not ret_val[0].json["status"]:
                await organization_dal.remove_organization(data[OrganizationFields.organization_name])
                ret_val = error_resp(code=error_constants.ErrorCode.ContactExists)
        else:
            ret_val = error_resp(code=resp.message)
    else:
        ret_val = error_resp(code=error_constants.ErrorCode.AtLeastOneContactIsRequired)
    return ret_val


def login(json_data):
    return auth.login(json_data, ObjNames.Contact)


def login_by_otp_step_1(json_data):
    return auth.login_by_otp_step_1(json_data, ObjNames.Contact)


def login_by_otp_step_2(json_data):
    return auth.login_by_otp_step_2(json_data)


async def delete_contact(username_to_delete):
    number_of_organization_contact: DatabaseResponse = await organization_dal.number_of_organization_contact()
    if number_of_organization_contact > 1:
        resp: DatabaseResponse = await user_dal.delete_user(username_to_delete)
        if resp.status:
            ret_val = ok_code(code=resp.message)
        else:
            ret_val = error_resp(code=resp.message)
    else:
        ret_val = error_resp(code=error_constants.ErrorCode.AtLeastOneContactIsRequired)
    return ret_val


async def update_contact(new_data):
    data_to_update = current_user.get_user_data(all_included=True)

    def update_field(field, allow_none=False):
        new_value = new_data.get(field, None)
        if allow_none or new_value is not None:
            data_to_update[field] = new_value

    update_field(UsersFields.email, allow_none=False)
    update_field(UsersFields.phone_number, allow_none=False)

    new_password = new_data.get(UsersFields.password, None)
    if new_password is not None:
        data_to_update[UsersFields.password] = generate_password_hash(new_password)

    resp: DatabaseResponse = await user_dal.update_user(data_to_update)
    if resp.status:
        if new_password is not None:
            token = token_service.create_token(data_to_update)
            ret_val = ok(code=resp.message, token=token)
        else:
            ret_val = ok_code(code=resp.message)
    else:
        ret_val = error_resp(code=resp.message)
    return ret_val


async def delete_organization():
    resp: DatabaseResponse = await organization_dal.delete_organization()
    if resp.status:
        await organization_dal.delete_organization_contacts()
        await scholarship_dal.delete_organization_scholarships()
        ret_val = ok_code(code=resp.message)
    else:
        ret_val = error_resp(code=resp.message)
    return ret_val


async def update_organization(new_data):
    data_to_update = await organization_dal.get_organization_data()

    def update_field(field, allow_none=False):
        new_value = new_data.get(field, None)
        if allow_none or new_value is not None:
            data_to_update[field] = new_value

    update_field(OrganizationFields.address, allow_none=True)
    update_field(OrganizationFields.office_phone, allow_none=True)
    update_field(OrganizationFields.facebook, allow_none=True)
    update_field(OrganizationFields.linkedin, allow_none=True)
    update_field(OrganizationFields.website, allow_none=True)
    update_field(OrganizationFields.lego, allow_none=True)

    resp: DatabaseResponse = await organization_dal.update_organization(data_to_update)
    if resp.status:
        ret_val = ok_code(code=resp.message)
    else:
        ret_val = error_resp(code=resp.message)
    return ret_val


async def get_contacts():
    resp = await organization_dal.get_organization_contact()
    if resp is not None:
        for contact in resp:
            contact.pop(UsersFields.password)
            users_models.filter_user_data(contact)
        ret_val = ok(resp)
    else:
        logger_service.critical(error_constants.ErrorConstant.GenericError)
        ret_val = error_resp(code=error_constants.ErrorCode.UnknownError)
    return ret_val


async def get_organization_data():
    data = await organization_dal.get_organization_data()
    if data is not None:
        data.pop(OrganizationFields.is_active)
        ret_val = ok(data)
    else:
        logger_service.critical(error_constants.ErrorConstant.GenericError)
        ret_val = error_resp(code=error_constants.ErrorCode.UnknownError)
    return ret_val


async def get_user_data(username):
    if not username:  # empty or None
        ret_val = ok(current_user.get_user_data())  # get this user data
    else:
        resp = await organization_dal.get_organization_contact(username)
        if resp is not None and len(resp) > 0:
            ret_val = ok(filter_user_data(resp[0]))
        else:
            ret_val = error_resp(code=error_constants.ErrorCode.UserNotFound)
    return ret_val
