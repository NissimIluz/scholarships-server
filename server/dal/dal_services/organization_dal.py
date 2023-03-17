import _asyncio
import dictionary as dictionary
from flask_login import current_user
from server.constants.database_constants.objnames import ObjNames
from server.constants.fields_name.organization_fields import OrganizationFields
from server.constants.fields_name.scholarship_fields import ScholarshipFields
from server.constants.fields_name.users.contact_fields import ContactFields
from server.constants.fields_name.users.users_fields import UsersFields
from server.constants.general_constants import generate_guid
from server.dal.infra_dal.interface_database import IDal
from server.dal.dal_contracts.interface_organizations_dal import IOrganizationsDal
from server.models.responses import DatabaseResponse


class OrganizationsDal(IOrganizationsDal):

    def __init__(self, dal: IDal):
        self.dal: IDal = dal

    def add_organization(self, documents: dictionary) -> DatabaseResponse:
        id = generate_guid(15)
        documents[OrganizationFields.id] = id
        result = self.dal.insert_async(ObjNames.Organizations, documents)
        return result

    def get_organization_data(self) -> _asyncio.Future:
        filter_by = {OrganizationFields.id: current_user.get_organization_id()}
        return self.dal.find_one_async(ObjNames.Organizations, filter_by, only_active=False)

    def get_organization_contact(self, username=None):
        if username is None:
            filter_by = {ContactFields.organization_id: current_user.get_organization_id()}
        else:
            filter_by = {ContactFields.organization_id: current_user.get_organization_id(),
                         UsersFields.username: username}
        response = self.dal.find_all_async(ObjNames.Contact, filter_by).to_list(100)
        return response

    def number_of_organization_contact(self):
        filter_by = {ScholarshipFields.organization_id: current_user.get_organization_id()}
        response = self.dal.count_documents_async(ObjNames.Contact, filter_by)
        return response

    def delete_organization(self):
        return self.dal.inactivating_async(ObjNames.Organizations,
                                           {"_id": current_user.get_organization_id()})

    def delete_organization_contacts(self):
        filter_by = {ContactFields.organization_id: current_user.get_organization_id()}
        return self.dal.inactivating_async(ObjNames.Contact, filter_by, multy=True)

    def update_organization(self, new_data):
        filter_by = {OrganizationFields.id: current_user.get_organization_id()}
        ret_val = self.dal.update_async(ObjNames.Organizations, filter_by, new_data)
        return ret_val

    def remove_organization(self, organization_name):
        return self.dal.remove_async(ObjNames.Organizations, {OrganizationFields.organization_name: organization_name, OrganizationFields.is_active: True})
