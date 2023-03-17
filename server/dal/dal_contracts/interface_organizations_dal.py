import _asyncio
from abc import ABC, abstractmethod
import dictionary
from server.dal.infra_dal.interface_database import IDal
from server.models.responses import DatabaseResponse


class IOrganizationsDal(ABC):
    @abstractmethod
    def __init__(self, mongo_db: IDal):
        pass

    @abstractmethod
    def add_organization(self, documents: dictionary) -> DatabaseResponse:
        pass

    @abstractmethod
    def get_organization_data(self) -> _asyncio.Future:
        pass

    @abstractmethod
    def get_organization_contact(self, username=None):
        pass

    @abstractmethod
    def number_of_organization_contact(self):
        pass

    @abstractmethod
    def delete_organization(self):
        pass

    @abstractmethod
    def delete_organization_contacts(self):
        pass

    @abstractmethod
    def update_organization(self, new_data):
        pass

    @abstractmethod
    def remove_organization(self, organization_name):
        pass
