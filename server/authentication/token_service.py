from datetime import datetime, timezone, timedelta
import flask
import jwt
from server import configuration
from server.authentication import encryption_service
from server.constants.database_constants.objnames import ObjNames
from server.constants.fields_name.users.users_fields import UsersFields


def create_token(user, is_registered=True, user_identity=ObjNames.Candidates, exp_minutes=configuration.exp_token):
    exp = (datetime.now(tz=timezone.utc) + timedelta(minutes=exp_minutes))
    headers = flask.request.headers
    return jwt.encode(
        {
            UsersFields.id: encryption_service.encrypt(user[UsersFields.id]),
            UsersFields.username: user[UsersFields.username],
            UsersFields.user_identity: encryption_service.encrypt(user_identity),
            UsersFields.is_registered: encryption_service.encrypt(is_registered),
            "User-Agent": headers["User-Agent"],
            "exp": exp
        },
        key=configuration.jwt_key,
        algorithm=configuration.encryption_algorithm)


def decode_token(token):
    token = jwt.decode(jwt=token, key=configuration.jwt_key,
                       algorithms=configuration.encryption_algorithm)
    token[UsersFields.id] = encryption_service.decode(token[UsersFields.id])
    token[UsersFields.is_registered] = encryption_service.decode(token[UsersFields.is_registered])
    token[UsersFields.user_identity] = encryption_service.decode(token[UsersFields.user_identity])
    return token


