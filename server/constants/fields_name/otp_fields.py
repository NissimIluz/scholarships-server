from server.constants.fields_name.base_fields import BaseFields
from server.constants.fields_name.users.users_fields import UsersFields


class OtpFields(BaseFields):
    username = UsersFields.username
    otp = 'otp'
    user_identity = UsersFields.user_identity
    attempts = "attempts"
    key = 'key'
