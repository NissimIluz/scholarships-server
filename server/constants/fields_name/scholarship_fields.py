from server.constants.fields_name.base_fields import BaseFields


class ScholarshipFields(BaseFields):
    name = 'name'
    organization_id = 'organizationId'
    organization_name = 'organizationName'
    create_by = "createBy"
    scholarship_type = 'scholarshipType'
    conditions = 'conditions'
    description = 'description'
    eligible_type = 'eligibleType'
    final_date_to_confirm = 'finalDateToConfirm'
    final_date_to_approval = 'finalDateToApproval'
    documents_required = 'documentsRequired'
    number_of_submissions = "numberOfSubmissions"
    submitted = "submitted"
