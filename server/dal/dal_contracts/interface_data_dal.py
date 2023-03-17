from abc import abstractmethod, ABC
from server.dal.infra_dal.interface_database import IDal


class IDataDal(ABC):
    @abstractmethod
    def __init__(self, mongo_db: IDal):
        pass

    @abstractmethod
    def get_data_by_id(self, data_id):
        pass
