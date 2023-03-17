from abc import abstractmethod, ABC
import pymongo
from server.constants.fields_name.users.candidate_fields import CandidateFields
from server.dal.infra_dal.interface_database import IDal


class IHelpdeskDal(ABC):
    @abstractmethod
    def __init__(self, mongo_db: IDal):
        pass

    @abstractmethod
    def get_students(self, skip, take, s_phone_number=None, s_email=None, s_first_name=None, s_last_name=None,
                     s_id=None, s_phrase=None, only_active=True, order_by=CandidateFields.last_name,
                     order_direction=pymongo.ASCENDING):
        pass
