from flask_login import current_user
from pymongo import ReturnDocument
from server.constants.database_constants.objnames import ObjNames
from server.constants.fields_name.submitted_scholarships_fields import SubmittedScholarshipsFields
from server.constants.fields_name.users.users_fields import UsersFields
from server.constants.general_constants import generate_guid
from server.dal.infra_dal.interface_database import IDal
from server.dal.dal_contracts.interface_submission import ISubmissionsDal


class SubmissionsDal(ISubmissionsDal):

    def __init__(self, dal: IDal):
        self.dal: IDal = dal

    def add_submissions(self, submission_data):
        submission_data[SubmittedScholarshipsFields.id] = generate_guid(25)
        user = current_user
        submission_data[SubmittedScholarshipsFields.username] = user.get_user_name()
        submission_data[SubmittedScholarshipsFields.is_user_registered] = user.is_registered
        submission_data[SubmittedScholarshipsFields.user_phone] = user.get_property(UsersFields.phone_number)
        submission_data[SubmittedScholarshipsFields.user_email] = user.get_property(UsersFields.email)
        submission_data[SubmittedScholarshipsFields.is_open] = True

        return self.dal.insert_async(ObjNames.SubmittedScholarships, submission_data)

    def get_user_submissions(self, username=None, only_active=True):
        if username is None:
            username = current_user.get_user_name()
        filter_by = {SubmittedScholarshipsFields.username: username}
        result = self.dal.find_all_async(ObjNames.SubmittedScholarships, filter_by,
                                         only_active=only_active)
        return result.to_list(None)

    def update_submission_statuses(self, submission_id, scholarships_id, new_submission, is_open):
        filter_by = {
            SubmittedScholarshipsFields.id: submission_id,
            SubmittedScholarshipsFields.scholarship_id: scholarships_id,
            SubmittedScholarshipsFields.is_open: True
        }
        update_command = {
            '$set': {SubmittedScholarshipsFields.is_open: is_open},
            '$push': {SubmittedScholarshipsFields.submission_statuses: new_submission}
        }
        return self.dal.find_one_and_update_async(collection=ObjNames.SubmittedScholarships,
                                                  filter_by=filter_by, update_command=update_command,
                                                  return_document=ReturnDocument.AFTER)

    def get_all_by_key(self, key, value):
        return self.dal.find_all_async(collection=ObjNames.SubmittedScholarships,
                                       filter_by={key: value}, only_active=False).to_list(None)
