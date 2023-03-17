from server.constants.fields_name.base_fields import BaseFields


class SubmittedScholarshipsFields(BaseFields):
    scholarship_id = 'scholarshipId'
    username = 'username'
    is_user_registered = 'isUserRegistered'
    user_email = 'userEmail'
    user_phone = 'userPhone'
    submission_statuses = 'SubmissionStatuses'
    is_open = "isOpen"
    submission_id = "submissionId"
    organization_id = 'organizationId'

    class SubmissionStatusFields:
        submission_status = 'SubmissionStatus'
        description = "description"
        free_text = "freeText"
        requirements = "requirements"
        date = "date"