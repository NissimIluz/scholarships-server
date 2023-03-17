from abc import ABC, abstractmethod
import dictionary
from server.constants.fields_name.users.users_fields import UsersFields
from server.authentication.enums.enter_action_enum import EnterAction
from server.enums.registration_status import RegistrationStatus
from server.enums.update_user_login_data import UpdateUserLoginData
from server.dal.infra_dal.interface_database import IDal
from server.models.responses import DatabaseResponse


class IUsersDal(ABC):
    @abstractmethod
    def __init__(self, mongo_db: IDal):
        pass

    @abstractmethod
    def add_candidate(self, documents: dictionary) -> DatabaseResponse:
        pass

    @abstractmethod
    def add_contacts(self, documents: dictionary, new_organization=False, organization_name=None,
                     organization_id=None) -> DatabaseResponse:
        pass

    @abstractmethod
    def get_user_information(self, user_identity, user_identity_collection, action=EnterAction.session,
                             get_by=UsersFields.id):
        pass

    @abstractmethod
    def delete_user(self, username_to_delete=None):
        pass

    @abstractmethod
    def update_user(self, new_data, user_identity=None,
                    filter_by_registration_status: RegistrationStatus = None, update_last=True) -> DatabaseResponse:
        pass

    @abstractmethod
    def find_one_and_update_user(self, new_data, user_identity=None,
                                 filter_by_registration_status: RegistrationStatus = None, update_last=True) -> DatabaseResponse:
        pass

    @abstractmethod
    def get_dialogue_obj(self):
        pass

    @abstractmethod
    def update_dialogue_obj(self, remaining_requirements: [] = None, upload_requirements: [] = None,
                            files_paths: [] = None, scholarships_names: [] = None, upload_attempt: int = None,
                            is_update: bool = True, is_active: bool = True
                            ):
        pass

    @abstractmethod
    def set_user_last_login(self, user_identity, username):
        pass

    @abstractmethod
    async def get_user_last_otp(self, get_by_key):
        pass

    @abstractmethod
    def get_user_by_otp(self, otp, get_by_key, get_by_value):
        pass

    @abstractmethod
    def set_user_otp(self, otp, username, key, user_identity):
        pass

    @abstractmethod
    def remove_user_otp(self, username):
        pass

    @abstractmethod
    def insert_guests(self, email, phone_number, key, value):
        pass

    @abstractmethod
    def reset_user_login_data(self, user_identity_collection, user_data, action: UpdateUserLoginData):
        pass
