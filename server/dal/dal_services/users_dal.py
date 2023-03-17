import dictionary as dictionary
from datetime import datetime, timedelta
import pymongo
from flask_login import current_user
from server import configuration
from server.constants.database_constants.database_responses import Responses
from server.constants.fields_name.users.contact_fields import ContactFields
from server.constants.database_constants.objnames import ObjNames
from server.constants.fields_name.dialogue_fields import DialogueFields
from server.constants.fields_name.otp_fields import OtpFields
from server.constants.fields_name.users.users_fields import UsersFields
from server.authentication.enums.enter_action_enum import EnterAction
from server.enums.registration_status import RegistrationStatus
from server.enums.update_user_login_data import UpdateUserLoginData
from server.constants.general_constants import generate_guid
from server.dal.infra_dal.interface_database import IDal
from server.dal.dal_contracts.interface_users_dal import IUsersDal
from server.models.responses import DatabaseResponse
from pymongo import ReturnDocument


class UsersDal(IUsersDal):

    def __init__(self, dal: IDal):
        self.dal: IDal = dal

    def add_candidate(self, documents: dictionary) -> DatabaseResponse:
        self.add_user_fields(documents)
        result = self.dal.insert_async(ObjNames.Candidates, documents)
        return result

    def add_contacts(self, documents: dictionary, new_organization=False, organization_name=None,
                     organization_id=None) -> DatabaseResponse:
        for contact in documents:
            if new_organization:
                contact[ContactFields.organization_name] = organization_name
                contact[ContactFields.organization_id] = organization_id
                contact[ContactFields.create_by] = None
            else:
                contact[ContactFields.organization_name] = current_user.get_organization_name()
                contact[ContactFields.organization_id] = current_user.get_organization_id()
                contact[ContactFields.create_by] = current_user.get_user_name()
            contact[ContactFields.registration_status] = RegistrationStatus.registered.value
            self.add_user_fields(contact)
        result = self.dal.insert_async(ObjNames.Contact, documents)
        return result

    def get_user_information(self, user_identity, user_identity_collection, action=EnterAction.session,
                             get_by=UsersFields.id):
        filter_by = {get_by: user_identity}
        if action == EnterAction.login:
            update = {
                "$set": {UsersFields.last_login_attempt: datetime.now()},
                "$inc": {UsersFields.login_attempt: 1}
            }
        elif action == EnterAction.session:
            filter_by[UsersFields.last_session] = {
                "$gte": datetime.now() - timedelta(minutes=configuration.exp_session)
            }
            filter_by[UsersFields.registration_status] = {"$gte": RegistrationStatus.registered.value}
            update = {
                "$set": {UsersFields.last_session: datetime.now()}
            }
        else:
            update = {"$set": {}}
        resp = self.dal.find_one_and_update_async(user_identity_collection, filter_by, update_command=update)
        return resp

    def set_user_last_login(self, user_identity, username):
        filter_by = {UsersFields.id: username}
        set_data = {
            UsersFields.last_session: datetime.now(),
            UsersFields.last_login: datetime.now(),
            UsersFields.login_attempt: 0
        }
        return self.dal.update_async(user_identity, filter_by, set_data, update_last_update_date=False)

    async def get_user_last_otp(self, get_by_key):
        filter_by = {
            OtpFields.create_date: {'$gte': datetime.now() - timedelta(minutes=configuration.exp_otp)},
            OtpFields.key: get_by_key
        }
        sort = [(OtpFields.create_date, pymongo.DESCENDING)]
        update = {"$inc": {OtpFields.attempts: 1}}
        otp_obj = await self.dal.find_one_and_update_async(ObjNames.OTP, filter_by, update_command=update, sort=sort)
        return otp_obj

    def get_user_by_otp(self, otp, get_by_key, get_by_value):
        aggregate_array = [
            {'$match': {OtpFields.otp: otp}},
            {'$match': {OtpFields.key: get_by_value}},
            {'$match': {OtpFields.create_date: {'$gte': datetime.now() - timedelta(minutes=configuration.exp_otp)}}},
            {
                '$lookup': {
                    'from': ObjNames.Candidates,
                    'localField': get_by_key,
                    'foreignField': get_by_key,
                    'as': ObjNames.Candidates
                }
            },
            {
                '$lookup': {
                    'from': ObjNames.Contact,
                    'localField': get_by_key,
                    'foreignField': get_by_key,
                    'as': ObjNames.Contact
                }
            },
            {'$limit': 1},
        ]
        result = self.dal.aggregate_async(ObjNames.OTP, aggregate_array).next()
        return result

    def delete_user(self, username_to_delete=None):
        if username_to_delete is None:
            username_to_delete = current_user.get_id()
        return self.dal.inactivating_async(current_user.get_user_identity(), {UsersFields.id: username_to_delete})

    def update_user(self, new_data, user_identity=None, filter_by_registration_status: RegistrationStatus = None, update_last=True):
        return self._update_user_with_get(new_data, user_identity, filter_by_registration_status,
                                          get_data=False, update_last=update_last)

    def find_one_and_update_user(self, new_data, user_identity=None,
                                 filter_by_registration_status: RegistrationStatus = None, update_last=True):
        return self._update_user_with_get(new_data, user_identity, filter_by_registration_status,
                                          get_data=True, update_last=update_last)

    def set_user_otp(self, otp, username, key, user_identity):
        documents = {
            OtpFields.otp: otp,
            OtpFields.username: username,
            OtpFields.user_identity: user_identity,
            OtpFields.key: key,
            OtpFields.attempts: 0
        }
        result = self.dal.insert_async(ObjNames.OTP, documents)
        return result

    def remove_user_otp(self, username):
        return self.dal.inactivating_async(
            ObjNames.OTP,
            {OtpFields.username: username}, multy=True)

    async def insert_guests(self, email, phone_number, key, value):
        user_name = generate_guid(20)
        set_data = {
            UsersFields.last_login: datetime.now(),
            UsersFields.last_session: datetime.now(),
            UsersFields.is_active: True,
            UsersFields.update_date: datetime.now()
        }
        set_on_insert = {
            UsersFields.id: user_name,
            UsersFields.username: user_name,
            UsersFields.create_date: datetime.now()
        }
        if phone_number is not None:
            set_data[UsersFields.phone_number] = phone_number
        if email is not None:
            set_data[UsersFields.email] = email
        filter_by = {key: value}
        update = {
            "$setOnInsert": set_on_insert,
            "$set": set_data,
        }
        result = await self.dal.find_one_and_update_async(ObjNames.AuthorizedGuests,
                                                          filter_by, update_command=update, upsert=True)
        if result is not None:
            return result
        else:
            return set_on_insert

    def get_dialogue_obj(self):
        filter_by = {DialogueFields.username: current_user.get_id()}
        return self.dal.find_one_async(ObjNames.Dialogues, filter_by)

    def update_dialogue_obj(self, remaining_requirements: [] = None, upload_requirements: [] = None,
                            files_paths: [] = None, scholarships_names: [] = None, upload_attempt: int = None,
                            is_update: bool = True, is_active: bool = True
                            ):
        data = {}
        if not (remaining_requirements is None or upload_requirements is None or files_paths is None or
                upload_attempt is None):
            data[DialogueFields.remaining_requirements] = remaining_requirements
            data[DialogueFields.upload_requirements] = upload_requirements
            data[DialogueFields.files_paths] = files_paths
            data[DialogueFields.upload_attempt] = upload_attempt
            data[DialogueFields.scholarships_names] = scholarships_names
        if is_update:
            filter_by = {DialogueFields.username: current_user.get_id(), "is_active": True}
            if not is_active:
                data["is_active"] = is_active
            ret_val = self.dal.update_async(ObjNames.Dialogues, filter_by, data)
        else:
            data[DialogueFields.username] = current_user.get_id()
            ret_val = self.dal.insert_async(ObjNames.Dialogues, data)
        return ret_val

    def reset_user_login_data(self, user_identity_collection, user_data, action: UpdateUserLoginData):
        filter_by = {UsersFields.id: user_data[UsersFields.id]}
        if action == UpdateUserLoginData.blocked_user:
            update_command = {
                "$set": {UsersFields.last_login_attempt: user_data[UsersFields.last_login_attempt]},
                "$inc": {UsersFields.login_attempt: -1}
            }
        elif action == UpdateUserLoginData.full_reset:
            update_command = {
                "$set": {UsersFields.last_login_attempt: datetime.now() - timedelta(minutes=configuration.block_user_for)},
                "$set": {UsersFields.login_attempt: 0}
            }
        return self.dal.update_async(user_identity_collection, filter_by,
                                     update_command=update_command, update_last_update_date=False)

    @staticmethod
    def add_user_fields(document):
        date = datetime.now()
        document[UsersFields.id] = document[UsersFields.username]
        document[UsersFields.last_login] = date
        document[UsersFields.last_session] = date
        document[UsersFields.login_attempt] = 0
        document[UsersFields.last_login_attempt] = date
        return document

    async def _update_user_with_get(self, new_data, user_identity=None,
                                    filter_by_registration_status: RegistrationStatus = None,
                                    get_data=False, update_last=True):
        if not user_identity:
            user_identity = current_user.get_user_identity()

        filter_by = {UsersFields.id: current_user.get_id()}

        if filter_by_registration_status:
            filter_by[UsersFields.registration_status] = {
                '$gte': filter_by_registration_status.value#,
                #'$lte': RegistrationStatus.step3 restore after dev end --tbd
            }
        if get_data:
            response = await self.dal.find_one_and_update_async(user_identity, filter_by, new_data=new_data,
                                                                return_document=ReturnDocument.AFTER)
            if response is not None:
                ret_val = DatabaseResponse(True, None, response)
            else:  # update failed
                ret_val = DatabaseResponse(False, Responses.UpdateFail, None)
        else:
            ret_val = await self.dal.update_async(user_identity, filter_by, new_data, update_last_update_date=update_last)

        return ret_val
