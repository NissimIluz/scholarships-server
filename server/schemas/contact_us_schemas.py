from marshmallow import Schema, fields, validate
from server.schemas.regular_expressions import RegularExpression


class OrganizationRegistration(Schema):
    name = fields.String(required=True, validate=validate.Regexp(RegularExpression.name))
    email = fields.Email(required=True)
    phoneNumber = fields.String(required=True, validate=validate.Regexp(RegularExpression.phone))