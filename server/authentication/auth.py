from functools import wraps
from server.authentication import authorization_service, auth_helper
from server.authentication.enums.authorization_level import AuthorizationLevel


def authorized(authorized_level: AuthorizationLevel = AuthorizationLevel.authorized, authenticate_vs_db=False):
    print('authorized decorator created: ', authorized_level)

    def creator_decorator(func):
        @wraps(func)
        async def call(*args, **kwargs):
            try:
                error = await authorization_service.get_authorization_error(authorized_level, authenticate_vs_db)
                if error is None:  # user is authorized
                    return await func(*args, **kwargs)
                else:
                    return error
            except Exception as ex:
                return auth_helper.error(ex)

        return call

    return creator_decorator
