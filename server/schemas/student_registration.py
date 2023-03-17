from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField
from server.enums.degree_type import DegreeTypes
from server.schemas.regular_expressions import RegularExpression


class RegistrationStep1(Schema):
    username = fields.String(required=False, allow_none=True, validate=validate.Regexp(RegularExpression.username))
    password = fields.String(required=False, allow_none=True, validate=validate.Regexp(RegularExpression.password))
    firstName = fields.String(required=True, validate=validate.Regexp(RegularExpression.name))
    lastName = fields.String(required=True, validate=validate.Regexp(RegularExpression.name))
    phoneNumber = fields.String(required=True, validate=validate.Regexp(RegularExpression.phone))
    idNumber = fields.String(required=True, validate=validate.Regexp(RegularExpression.id_umber))
    birthDate = fields.DateTime(required=True)
    email = fields.Email(required=True)

    zipCode = fields.String(required=True, validate=validate.Regexp(RegularExpression.zip_code))
    city = fields.String(required=True, validate=validate.Regexp(RegularExpression.name))
    street = fields.String(required=True, validate=validate.Regexp(RegularExpression.name))
    streetNumber = fields.String(required=True, validate=validate.Regexp(RegularExpression.street_number))

    idFile = fields.Raw(type='file')


class RegistrationStep2(Schema):
    # step2
    nationalService = fields.Boolean(required=True)
    nationalServiceStartDate = fields.DateTime(required=False)
    nationalServiceEndDate = fields.DateTime(required=False)
    collegeName = fields.String(required=True, validate=validate.Regexp(RegularExpression.name))
    collegeId = fields.Number(required=False)
    studyStartYear = fields.DateTime(format='%Y', required=True)
    studyCurrentYear = fields.Number(required=True)
    fieldOfStudy = fields.String(required=True, validate=validate.Regexp(RegularExpression.name))
    degree = EnumField(DegreeTypes, by_value=True, load_by=EnumField.VALUE, dump_by=EnumField.VALUE)
    studentPermit = fields.Raw(type='file')


class RegistrationStep3(Schema):
    isAllowance = fields.Boolean(required=True)
    isWork = fields.Boolean(required=True)
    allowanceIncomeMonthly = fields.Number(required=False, allow_none=True, default=None)
    workIncomeMonthly = fields.Number(required=False)


class RegistrationStep4(Schema):
    acceptTerms = fields.Boolean(required=True)