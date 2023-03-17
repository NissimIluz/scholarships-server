from marshmallow import Schema, fields, validate
from server.schemas.regular_expressions import RegularExpression


class GetStudents(Schema):
    skip = fields.Number(required=True, validate=validate.Range(min=1, max=1000))
    take = fields.Number(required=True, validate=validate.Range(min=0, max=1000))
    phoneNumber = fields.String(required=False, allow_none=True, validate=validate.Regexp(RegularExpression.phone))
    email = fields.Email(required=False, allow_none=True)
    firstName = fields.String(required=False, allow_none=True, validate=validate.Regexp(RegularExpression.name))
    lastName = fields.String(required=False, allow_none=True, validate=validate.Regexp(RegularExpression.name))
    idNumber = fields.String(required=False, allow_none=True, validate=validate.Regexp(RegularExpression.id_umber))
    phrase = fields.String(required=False, allow_none=True, validate=validate.Regexp(RegularExpression.name))
    onlyActive = fields.Boolean(required=False, allow_none=True)
    orderBy = fields.String(required=False, allow_none=True, validate=validate.Regexp(RegularExpression.field_name))
    orderDirection = fields.Number(required=False, allow_none=True, validate=validate.Range(min=-1, max=1))
    # orderBy = fields.List([member[1] for member in inspect.getmembers(CandidateFields) if not member[0].startswith('_') and not inspect.ismethod(member[1])])
