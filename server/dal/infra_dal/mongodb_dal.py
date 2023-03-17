from datetime import datetime
import _asyncio
import pymongo
from motor import motor_asyncio
from pymongo import MongoClient
from server import configuration
from server.constants.database_constants.database_responses import Responses
from server.constants.fields_name.base_fields import BaseFields
from server.dal.infra_dal.interface_database import IDal
from server.models.responses import DatabaseResponse
from server.logger import logger_service
from pymongo.collection import ReturnDocument


class MongodbDal(IDal):
    def __init__(self, app=None):
        self.connection_string = configuration.mangoDB_connection
        self.database = configuration.database_name

    def create_connection(self):
        mongo_db: MongoClient = pymongo.MongoClient(self.connection_string)
        return mongo_db[self.database] #  .next()

    def create_async_connection(self):
        mongo_db: MongoClient = motor_asyncio.AsyncIOMotorClient(self.connection_string,
                                                                 maxPoolSize=configuration.maxPoolSize)
        return mongo_db[self.database]

    async def insert_async(self, collection, documents) -> DatabaseResponse:
        connection = self.create_async_connection()
        cursor = connection[collection]
        if type(documents) is list:
            for document in documents:
                document[BaseFields.is_active] = True
                document[BaseFields.create_date] = datetime.now()
                document[BaseFields.update_date] = None
            result: _asyncio.Future = cursor.insert_many(documents)
        else:
            documents[BaseFields.is_active] = True
            documents[BaseFields.create_date] = datetime.now()
            documents[BaseFields.update_date] = None
            result: _asyncio.Future = cursor.insert_one(documents)
        try:
            response: pymongo.results = await result
            if type(documents) is list:
                ret_val = DatabaseResponse(response.acknowledged)
            else:
                ret_val = DatabaseResponse(response.acknowledged, information=str(response.inserted_id))
        except pymongo.errors.DuplicateKeyError as ex:
            message = Responses.DuplicateKeyError
            ret_val = DatabaseResponse(False, message, ex.details['keyValue'])
            logger_service.info(ex)
        except Exception as ex:

            if (ex.code == 65):  # https://gist.github.com/rluvaton/a97a8da46ab6541a3e5702e83b9d357b
                message = Responses.MultyErrors
                logger_service.info(ex)
            else:
                message = Responses.UnknownError
                logger_service.error(ex)
            ret_val = DatabaseResponse(False, message)
        return ret_val

    async def update_async(self, collection, filter_by, new_data=None, update_command=None, upsert=False,
                           bypass_document_validation=False,
                           collation=None, array_filters=None, hint=None,
                           session=None, multy=False, update_last_update_date=True):
        if update_command is None:
            update_command = {"$set": new_data}
        if update_last_update_date:
            new_data[BaseFields.update_date] = datetime.now()

        connection = self.create_async_connection()
        cursor = connection[collection]
        ret_val = DatabaseResponse()
        try:
            if multy:
                resp = await cursor.update_many(filter_by, update_command, upsert, array_filters,
                                                bypass_document_validation, collation, hint, session)
            else:
                resp = await cursor.update_one(filter_by, update_command, upsert,
                                               bypass_document_validation,
                                               collation, array_filters, hint,
                                               session)
            secsses: bool = bool(resp.raw_result["updatedExisting"] or (upsert and resp.raw_result.get('upserted')))
            ret_val.status = secsses
            if not secsses:
                ret_val.message = Responses.UpdateFail

        except Exception as ex:
            logger_service.error(ex)
            ret_val.status = False
            ret_val.message = Responses.UpdateFail
        return ret_val

    def inactivating_async(self, collection, filter_by, multy=False):
        filter_by[BaseFields.is_active] = True
        update_field = {
            BaseFields.is_active: {BaseFields.active_status: False, BaseFields.update_date: datetime.now()}}
        return self.update_async(collection, filter_by, update_field, multy=multy, update_last_update_date=False)

    def find_one_async(self, collection, filter_by, only_active=True, sort: [] = []):
        connection = self.create_async_connection()
        cursor = connection[collection]
        if only_active:
            filter_by[BaseFields.is_active] = True
        if not sort:
            return cursor.find_one(filter=filter_by)
        else:
            return cursor.find_one(filter=filter_by, sort=sort)

    def find_all_async(self, collection, filter_by={}, only_active=True):
        if only_active:
            filter_by[BaseFields.is_active] = True
        connection = self.create_async_connection()
        cursor = connection[collection]
        return cursor.find(filter_by)

    def count_documents_async(self, collection, filter_by={}, only_active=True):
        if only_active:
            filter_by[BaseFields.is_active] = True
        connection = self.create_async_connection()
        cursor = connection[collection]
        return cursor.count_documents(filter_by)

    async def remove_async(self, collection, filter_by) -> DatabaseResponse:
        connection = self.create_async_connection()
        cursor = connection[collection]
        try:
            result = await cursor.delete_many(filter=filter_by)
            return DatabaseResponse(status=result.deleted_count > 0, information=result.deleted_count)
        except Exception as ex:
            logger_service.error(ex)
            return DatabaseResponse(status=False, message=Responses.UnknownError, information=0)

    def remove(self, collection, filter_by) -> DatabaseResponse:
        connection = self.create_connection()
        cursor = connection[collection]
        try:
            result = cursor.delete_many(filter=filter_by)
            return DatabaseResponse(status=result.deleted_count > 0, information=result.deleted_count)
        except Exception as ex:
            logger_service.error(ex)
            return DatabaseResponse(status=False, message=Responses.UnknownError, information=0)

    def find_one_and_remove_async(self, collection, filter_by) -> DatabaseResponse:
        connection = self.create_async_connection()
        cursor = connection[collection]
        return cursor.find_one_and_delete(filter=filter_by)

    def find_one_and_update_async(self, collection, filter_by, new_data=None, update_command=None, or_rule=False,
                                  only_active=True, sort: [] = [], upsert=False, array_filters=None,
                                  return_document=ReturnDocument.BEFORE):
        if update_command is None:
            update_command = {'$set': new_data}
        if or_rule and only_active:
            for option in filter_by:
                option[BaseFields.is_active] = True
            filter_by = {"$or": filter_by}
        elif only_active:
            filter_by[BaseFields.is_active] = True
        if not sort:
            sort = None
        connection = self.create_async_connection()
        cursor = connection[collection]
        return cursor.find_one_and_update(filter=filter_by, update=update_command, sort=sort, upsert=upsert,
                                          array_filters=array_filters, return_document=return_document)

    def join(self, left_collection, right_collection, field_left_collection, field_right_collection, filter_by={},
             only_active=True, result_name='joinedResult', nested=False, match=None):
        aggregate_array = [
            {
                '$lookup': {
                    'from': right_collection,
                    f'localField': field_left_collection,
                    f'foreignField': field_right_collection,
                    f'as': result_name
                }
            }
        ]
        if nested and match is None:
            aggregate_array.append({"$match": {result_name: {"$ne": []}}})
        elif match is not None:
            aggregate_array.append({"$match": match})
        ret_val = self.aggregate_async(collection=left_collection, aggregate_array=aggregate_array, filter_by=filter_by,
                                       only_active=only_active)
        return ret_val

    def aggregate_async(self, collection, aggregate_array: [], filter_by={}, only_active=True):
        if only_active:
            filter_by[BaseFields.is_active] = True
        connection = self.create_async_connection()
        cursor = connection[collection]
        return cursor.aggregate(aggregate_array)

    def create_index(self, collection, keys, name, unique=True):
        connection = self.create_connection()[collection]
        try:
            results = connection.create_index(keys, unique=unique, name=name)
            print(results)
        except Exception as ex:
            print(ex)


    @staticmethod
    async def _create_response(response) -> DatabaseResponse:
        try:
            result: pymongo.results = await response
            return DatabaseResponse(result.acknowledged)
        except pymongo.errors.DuplicateKeyError as ex:
            message = Responses.DuplicateKeyError
            logger_service.info(ex)
            return DatabaseResponse(False, message, ex.details['keyValue'])

        except Exception as ex:
            logger_service.error(ex)
            message = Responses.UnknownError
            return DatabaseResponse(False, message)

    def create_all_index(self):
        self.create_index("Scholarships", [('isActive', pymongo.ASCENDING), ('organizationId', pymongo.ASCENDING),
                                           ('name', pymongo.ASCENDING)], "scholarships_index")

        self.create_index("Candidates", [('isActive', pymongo.ASCENDING), ('username', pymongo.ASCENDING)],
                          "candidate_username")
        self.create_index("Candidates", [('isActive', pymongo.ASCENDING), ('phoneNumber', pymongo.ASCENDING)],
                          "candidate_phone_number")
        self.create_index("Candidates", [('isActive', pymongo.ASCENDING), ('email', pymongo.ASCENDING)],
                          "candidate_email")
        self.create_index("Candidates", [('isActive', pymongo.ASCENDING), ('idNumber', pymongo.ASCENDING)],
                          "candidate_idNumber")

        self.create_index("OrganizationContact", [('isActive', pymongo.ASCENDING), ('username', pymongo.ASCENDING)],
                          "organization_contact_username")
        self.create_index("OrganizationContact", [('isActive', pymongo.ASCENDING), ('phoneNumber', pymongo.ASCENDING)],
                          "organization_contact_phone_number")
        self.create_index("OrganizationContact", [('isActive', pymongo.ASCENDING), ('email', pymongo.ASCENDING)],
                          "organization_contact_email")

        self.create_index("Organizations", [('isActive', pymongo.ASCENDING), ('organizationName', pymongo.ASCENDING)],
                          "organization_name")
