import copy

from flask_login import UserMixin

from server.constants.fields_name.users.users_fields import UsersFields


class AuthorizedUser(UserMixin):
    def __init__(self, user_json):
        self._user_json = user_json

    def get_id(self):
        result = self._user_json.get(UsersFields.username)
        return str(result)

    def is_active(self):
        is_active = self._user_json.get(UsersFields.is_active)
        return bool(is_active)

    def get_user_name(self):
        result = self._user_json.get(UsersFields.username)
        return str(result)

    def get_property(self, property_name):
        result = self._user_json.get(property_name, None)
        return str(result)

    def get_user_data(self, all_included=False):
        user_json_copy = copy.copy(self._user_json)
        if all_included:
            return user_json_copy
        else:
            return filter_user_data(user_json_copy, all_included)

    @property
    def is_registered(self):
        return bool(self._user_json.get(UsersFields.is_registered, False))

    def get_user_identity(self):
        user_identity = self.get_property(UsersFields.user_identity)
        return user_identity


def filter_user_data(user_json, all_included=False):
    if not all_included:
        user_json.pop(UsersFields.last_session)
        user_json.pop(UsersFields.is_active)
        user_json.pop(UsersFields.login_attempt)
        user_json.pop(UsersFields.last_login_attempt)
        user_json.pop(UsersFields.password)
    return user_json
