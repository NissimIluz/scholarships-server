from marshmallow import Schema, fields, validate
from server.schemas.regular_expressions import RegularExpression


class LoginSchema(Schema):
    username = fields.String(required=True, validate=validate.Regexp(RegularExpression.username))
    password = fields.String(required=True, validate=validate.Regexp(RegularExpression.password))


class LoginByOtpStep1Schema(Schema):
    phoneNumber = fields.String(required=False, validate=validate.Regexp(RegularExpression.phone), allow_none=True)
    email = fields.Email(required=False,  allow_none=True)


class LoginByOtpStep2Schema(LoginByOtpStep1Schema):
    otp = fields.String(required=True, validate=validate.Regexp(RegularExpression.otp))

# validate=Length(equal=configuration.otp_length))
# default required=False allow_none=False