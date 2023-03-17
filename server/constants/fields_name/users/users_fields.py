from server.constants.fields_name.base_fields import BaseFields


class UsersFields(BaseFields):
    registration_status = 'registrationStatus'
    username = 'username'
    password = 'password'
    email = 'email'
    phone_number = 'phoneNumber'
    last_login = 'lastLogin'
    last_session = 'lastSession'
    last_login_attempt = 'lastLoginAttempt'
    login_attempt = 'loginAttempt'
    is_registered = 'isRegistered'
    user_identity = 'userIdentity'
