from server.constants.database_constants.objnames import ObjNames
from server.constants.fields_name.users.contact_fields import ContactFields
from server.models.users.authorized_user import AuthorizedUser


class OrganizationsUser(AuthorizedUser):
    def __init__(self, user_json):
        self._user_json = user_json

    def get_organization_id(self):
        object_id = self._user_json.get(ContactFields.organization_id)
        return str(object_id)

    def get_organization_name(self):
        object_id = self._user_json.get(ContactFields.organization_name)
        return str(object_id)

    @staticmethod
    def get_user_identity():
        return ObjNames.Contact