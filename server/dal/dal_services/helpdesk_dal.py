import pymongo as pymongo
from server.constants.database_constants.objnames import ObjNames
from server.constants.fields_name.users.candidate_fields import CandidateFields
from server.dal.dal_contracts.interface_helpdesk_dal import IHelpdeskDal
from server.dal.infra_dal.interface_database import IDal


class HelpdeskDal(IHelpdeskDal):

    def __init__(self, dal: IDal):
        self.dal = dal

    async def get_students(self, skip, take, s_phone_number=None, s_email=None, s_first_name=None, s_last_name=None,
                           s_id=None, s_phrase=None, only_active=True, order_by=CandidateFields.last_name,
                           order_direction=pymongo.ASCENDING):
        connection = self.dal.create_async_connection()
        cursor = connection[ObjNames.Candidates]
        filter_by = {}
        if s_phone_number:
            filter_by[CandidateFields.phone_number] = {"$regex": s_phone_number}
        if s_first_name:
            filter_by[CandidateFields.first_name] = {"$regex": s_first_name}
        if s_last_name:
            filter_by[CandidateFields.last_name] = {"$regex": s_last_name}
        if s_email:
            filter_by[CandidateFields.email] = {"$regex": s_email}
        if s_id:
            filter_by[CandidateFields.id] = {"$regex": s_id}
        ret_val = await cursor.find(filter_by).sort(order_by, order_direction).skip(skip).to_list(take)
        for student in ret_val:
            student.pop(CandidateFields.password)
        return ret_val

