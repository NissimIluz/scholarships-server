from abc import abstractmethod, ABC
from server.dal.infra_dal.interface_database import IDal


class ISubmissionsDal(ABC):
    @abstractmethod
    def __init__(self, mongo_db: IDal):
        pass

    @abstractmethod
    def add_submissions(self, submission_data):
        pass

    @abstractmethod
    def get_user_submissions(self, username=None, only_active=True):
        pass

    @abstractmethod
    def update_submission_statuses(self, submission_id, scholarships_id, new_submission, is_open):
        pass

    @abstractmethod
    def get_all_by_key(self, key, value):
        pass
