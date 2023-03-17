from server import configuration
from server.base_services.base_controller import ok, error_resp
from server.constants.fields_name.contact_us_fields import ContactUsFields
from server.enums.enum_contact_us import EContactUsStatus, EContactUsOrigin
from server.constants.general_constants import generate_guid
from server.dal.dal_contracts.interface_contact_us_dal import IContactUsDal
from server.injector.dependency_injector import get_singleton
from server.services import email_service

contact_us_dal: IContactUsDal = get_singleton(IContactUsDal)


async def organization_registration(organization_data):
    contact_us_id = generate_guid(20)
    organization_data[ContactUsFields.id] = contact_us_id
    organization_data[ContactUsFields.origin] = "organization registration"
    organization_data[ContactUsFields.origin_id] = EContactUsOrigin.organization_registration
    organization_data[ContactUsFields.status] = EContactUsStatus.open
    if (await email_service.send_email(configuration.contact_us_organization_registration_email,
                                       configuration.contact_us_organization_registration_subject + " " +
                                       organization_data[ContactUsFields.name],
                                       generate_mail_text(organization_data))):
        organization_data[ContactUsFields.status] = EContactUsStatus.inner_mail_sent
    resp = await contact_us_dal.add_contact_us(organization_data)
    if resp.status:
        ret_val = ok(success=True, contactId=contact_us_id)
    else:
        ret_val = error_resp(code=resp.message, success=False)
    return ret_val


def generate_mail_text(data):
    ret_val = f'{data[ContactUsFields.name]} {configuration.contact_us_text} \n' \
              f'{configuration.contact_us_email}: {data[ContactUsFields.email]} \n' \
              f'{configuration.contact_us_phone_number}: {data[ContactUsFields.phone_number]} \n' \
              f'{configuration.contact_us_id}: {data[ContactUsFields.id]} \n'
    return ret_val
