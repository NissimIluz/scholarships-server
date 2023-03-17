import dictionary as dictionary
from cache import AsyncTTL
from flask_login import current_user
from server import configuration
from server.constants.database_constants.objnames import ObjNames
from server.constants.fields_name.scholarship_fields import ScholarshipFields
from server.constants.fields_name.submitted_scholarships_fields import SubmittedScholarshipsFields
from server.constants.general_constants import generate_guid
from server.dal.infra_dal.interface_database import IDal
from server.dal.dal_contracts.interface_scholarships_dal import IScholarshipsDal
from server.models.responses import DatabaseResponse


class ScholarshipsDal(IScholarshipsDal):

    def __init__(self, dal: IDal):
        self.dal: IDal = dal

    def add_scholarships(self, documents: dictionary) -> DatabaseResponse:
        organization_id = current_user.get_organization_id()
        organization_name = current_user.get_organization_name()
        current_user_name = current_user.get_user_name()
        if type(documents) is list:
            for document in documents:
                document[ScholarshipFields.id] = generate_guid(15)
                document[ScholarshipFields.organization_id] = organization_id
                document[ScholarshipFields.create_by] = current_user_name
                document[ScholarshipFields.organization_name] = organization_name
        else:
            documents[ScholarshipFields.id] = generate_guid(15)
            documents[ScholarshipFields.organization_id] = organization_id
            documents[ScholarshipFields.create_by] = current_user_name
            documents[ScholarshipFields.organization_name] = organization_name
        result = self.dal.insert_async(ObjNames.Scholarships, documents)
        return result

    def get_scholarship_details(self, scholarship_id, for_organization=False, only_active=True):
        filter_by = {ScholarshipFields.id: scholarship_id}
        if for_organization:
            filter_by[ScholarshipFields.organization_id] = current_user.get_organization_id()
        return self.dal.find_one_async(ObjNames.Scholarships, filter_by, only_active=only_active)

    @AsyncTTL(time_to_live=configuration.get_all_scholarships_ttl, maxsize=configuration.maxsize)
    async def get_all_scholarships(self):
        all_scholarships: [] = await self.dal.find_all_async(ObjNames.Scholarships).to_list(None)
        aggregate = [
            {"$group": {"_id": "$"+SubmittedScholarshipsFields.scholarship_id,
                        ScholarshipFields.number_of_submissions: {"$sum": 1}}}
        ]
        number_of_submissions: [] = await self.dal.aggregate_async(ObjNames.SubmittedScholarships,
                                                                   aggregate).to_list(None)

        for scholarship in all_scholarships:
            number = 0
            for x in number_of_submissions:
                if x[ScholarshipFields.id] == scholarship[ScholarshipFields.id]:
                    number = x[ScholarshipFields.number_of_submissions]
            scholarship[ScholarshipFields.number_of_submissions] = number
        return all_scholarships

    def get_organization_scholarships(self, only_active=True):
        filer_by = {ScholarshipFields.organization_id: current_user.get_organization_id()}
        response = self.dal.find_all_async(ObjNames.Scholarships, filer_by, only_active).to_list(None)
        return response

    def delete_organization_scholarships(self):
        filter_by = {ScholarshipFields.organization_id: current_user.get_organization_id()}
        return self.dal.inactivating_async(ObjNames.Scholarships, filter_by, multy=True)

    def delete_scholarships(self, scholarship_name):
        filter_by = {ScholarshipFields.name: scholarship_name,
                     ScholarshipFields.organization_id: current_user.get_organization_id()}
        return self.dal.inactivating_async(ObjNames.Scholarships, filter_by)

    def update_scholarships(self, new_data):
        filter_by = {
            ScholarshipFields.id: new_data[ScholarshipFields.id],
            ScholarshipFields.name: new_data[ScholarshipFields.name],
            ScholarshipFields.organization_id: current_user.get_organization_id()
        }
        ret_val = self.dal.update_async(ObjNames.Scholarships, filter_by, new_data)
        return ret_val
