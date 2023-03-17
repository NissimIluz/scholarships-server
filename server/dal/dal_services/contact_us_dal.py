from server.constants.database_constants.objnames import ObjNames
from server.dal.dal_contracts.interface_contact_us_dal import IContactUsDal
from server.dal.infra_dal.interface_database import IDal


class ContactUsDal(IContactUsDal):
    def __init__(self, dal: IDal):
        self.dal: IDal = dal

    async def add_contact_us(self,data):
        return await self.dal.insert_async(ObjNames.ContactUs, data)

    async def get_contact_us(self, filter_by=None, filter_value=None):
        if filter_by is None or filter_value is None:
            ret_val = self.dal.find_all_async(ObjNames.ContactUs)
        else:
            ret_val = self.dal.find_all_async(ObjNames.ContactUs, {filter_by : filter_value}).to_list(None)
        return await ret_val
