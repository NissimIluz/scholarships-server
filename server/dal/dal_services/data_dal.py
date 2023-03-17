from abc import ABC

from cache import AsyncTTL

from server import configuration
from server.constants.fields_name.base_fields import BaseFields
from server.constants.database_constants.objnames import ObjNames
from server.dal.dal_contracts.interface_data_dal import IDataDal
from server.dal.infra_dal.interface_database import IDal


class DataDal(IDataDal):

    def __init__(self, dal: IDal):
        self.dal: IDal = dal

    @AsyncTTL(time_to_live=configuration.get_data, maxsize=configuration.maxsize)
    def get_data_by_id(self, data_id):
        ret_val = self.dal.find_one_async(collection=ObjNames.Data, filter_by={BaseFields.id: data_id},
                                          only_active=False)
        return ret_val
