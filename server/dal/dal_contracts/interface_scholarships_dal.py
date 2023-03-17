from abc import ABC, abstractmethod
import dictionary
from server.dal.infra_dal.interface_database import IDal
from server.models.responses import DatabaseResponse


class IScholarshipsDal(ABC):
    @abstractmethod
    def __init__(self, mongo_db: IDal):
        pass

    @abstractmethod
    def add_scholarships(self, documents: dictionary) -> DatabaseResponse:
        pass

    @abstractmethod
    def get_scholarship_details(self, scholarship_id, for_organization=False, only_active=True):
        pass

    @abstractmethod
    def get_all_scholarships(self):
        pass

    @abstractmethod
    def get_organization_scholarships(self, only_active=True):
        pass

    @abstractmethod
    def delete_organization_scholarships(self):
        pass

    @abstractmethod
    def delete_scholarships(self, scholarship_name):
        pass

    @abstractmethod
    def update_scholarships(self, new_data):
       pass

    @staticmethod
    def create_scholarship_id(scholarship_name):
        pass

