from server.constants.database_constants.objnames import ObjNames
from server.models.users.authorized_user import AuthorizedUser


class HelpDeskUser(AuthorizedUser):
    def __init__(self, user_json):
        self._user_json = user_json

    @staticmethod
    def get_user_identity():
        return ObjNames.HelpDeskUser
