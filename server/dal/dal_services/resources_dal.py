from server.constants.fields_name.files_fields import FilesFields
from server.constants.database_constants.objnames import ObjNames
from server.dal.infra_dal.interface_database import IDal
from server.dal.dal_contracts.interface_resources_dal import IResourcesDal


class ResourcesDal(IResourcesDal):

    def __init__(self, dal: IDal):
        self.dal: IDal = dal

    def save_or_update_file(self, user_id, file_path, scan_result, file_type):
        filter_by = {FilesFields.user_id: user_id}
        file_to_db = {
            FilesFields.file_path: file_path,
            FilesFields.scan_result: scan_result,
            FilesFields.file_type: file_type
        }
        return self.dal.update_async(ObjNames.Files, filter_by=filter_by,
                                     new_data=file_to_db, upsert=True, multy=False)

