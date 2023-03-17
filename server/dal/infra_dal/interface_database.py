from abc import ABC, abstractmethod

from pymongo import MongoClient, ReturnDocument

from server.models.responses import DatabaseResponse


class IDal(ABC):
    @abstractmethod
    def __init__(self, app=None):
        pass

    @abstractmethod
    def create_connection(self) -> MongoClient:
        pass

    @abstractmethod
    def create_async_connection(self) -> MongoClient:
        pass

    @abstractmethod
    def insert_async(self, collection, documents) -> DatabaseResponse:
        pass

    @abstractmethod
    def update_async(self, collection, filter_by, new_data=None, update_command=None,
                     upsert=False, bypass_document_validation=False,
                     collation=None, array_filters=None, hint=None,
                     session=None, multy=False, update_last_update_date=True):
        pass

    @abstractmethod
    def inactivating_async(self, collection, filter_by, multy=False):
        pass

    @abstractmethod
    def find_one_async(self, collection, filter_by, only_active=True, sort: [] = None):
        pass

    @abstractmethod
    def find_all_async(self, collection, filter_by={}, only_active=True):
        pass

    @abstractmethod
    def count_documents_async(self, collection, filter_by={}, only_active=True):
        pass

    @abstractmethod
    def remove_async(self, collection, _id) -> DatabaseResponse:
        pass

    @abstractmethod
    def find_one_and_remove_async(self, collection, filter_by) -> DatabaseResponse:
        pass

    @abstractmethod
    def find_one_and_update_async(self, collection, filter_by, new_data=None, update_command=None, or_rule=False,
                                  only_active=True, sort: [] = [], upsert=False, array_filters=None,
                                  return_document=ReturnDocument.BEFORE):
        pass

    @abstractmethod
    def join(self, left_collection, right_collection, field_left_collection, field_right_collection, filter_by={},
             only_active=True, result_name='joinedResult', nested=False, match=None):
        pass

    @abstractmethod
    def aggregate_async(self, collection, aggregate_array: [], filter_by={}, only_active=True):
        pass
