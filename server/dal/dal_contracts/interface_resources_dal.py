from abc import abstractmethod, ABC

from server.dal.infra_dal.interface_database import IDal


class IResourcesDal(ABC):
    @abstractmethod
    def __init__(self, mongo_db: IDal):
        pass

    @abstractmethod
    def save_or_update_file(self, user_id, file_path, scan_result, file_type):
        pass
