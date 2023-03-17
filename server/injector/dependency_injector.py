from server.dal.dal_contracts.interface_contact_us_dal import IContactUsDal
from server.dal.dal_contracts.interface_data_dal import IDataDal
from server.dal.dal_contracts.interface_helpdesk_dal import IHelpdeskDal
from server.dal.dal_services.helpdesk_dal import HelpdeskDal
from server.dal.infra_dal.interface_database import IDal
from server.dal.dal_contracts.interface_organizations_dal import IOrganizationsDal
from server.dal.dal_contracts.interface_resources_dal import IResourcesDal
from server.dal.dal_contracts.interface_scholarships_dal import IScholarshipsDal
from server.dal.dal_contracts.interface_submission import ISubmissionsDal
from server.dal.dal_contracts.interface_users_dal import IUsersDal
from server.dal.dal_services.contact_us_dal import ContactUsDal
from server.dal.dal_services.data_dal import DataDal
from server.dal.dal_services.organization_dal import OrganizationsDal
from server.dal.dal_services.resources_dal import ResourcesDal
from server.dal.dal_services.scholarships_dal import ScholarshipsDal
from server.dal.dal_services.submissions_dal import SubmissionsDal
from server.dal.dal_services.users_dal import UsersDal
from server.dal.infra_dal.mongodb_dal import MongodbDal
from server.dialogue.dialogue_contracts.dialogue_interface import DialogueInterface
from server.dialogue.dialogue_impl import DialogueImpl
from server.logger import logger_service

services_pointer = {  # interface: instance
}
interface_implementations = {  # interface: impl
    DialogueInterface: DialogueImpl,

    # database
    IDal: MongodbDal,
    IUsersDal: UsersDal,
    IOrganizationsDal: OrganizationsDal,
    IScholarshipsDal: ScholarshipsDal,
    ISubmissionsDal: SubmissionsDal,
    IContactUsDal: ContactUsDal,
    IResourcesDal: ResourcesDal,
    IDataDal: DataDal,
    IHelpdeskDal: HelpdeskDal
}


def get_singleton(interface: any, *params):
    if interface not in services_pointer:
        new = interface_implementations[interface](*params)
        services_pointer.update({interface: new})
        logger_service.info(str(interface_implementations) + " created as singleton")
    return services_pointer[interface]


def get_transient(interface: any, *params):
    retval = interface_implementations[interface](*params)
    logger_service.info(str(interface_implementations) + " created as transient")
    return retval
