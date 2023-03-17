from marshmallow import Schema, fields, validate
from server.schemas.regular_expressions import RegularExpression


class RegexPatternByName(Schema):
    regexName = fields.String(required=True, validate=validate.Regexp(RegularExpression.field_name))


class GetDataById(Schema):
    dataId = fields.String(required=True, validate=validate.Regexp(RegularExpression.field_name))
