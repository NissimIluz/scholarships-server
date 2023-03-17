from server.base_services.base_controller import error_resp, ok_code, ok
from server.constants import error_constants
from server.constants.fields_name.scholarship_fields import ScholarshipFields
from server.dal.dal_contracts.interface_scholarships_dal import IScholarshipsDal
from server.injector.dependency_injector import get_singleton
from server.logger import logger_service
from server.models.responses import DatabaseResponse
from server.services import submissions_service

scholarship_dal: IScholarshipsDal = get_singleton(IScholarshipsDal)


async def get_scholarships():
    data = await scholarship_dal.get_all_scholarships()
    return ok(data)


async def get_organization_scholarships(included_submissions=False):
    scholarships = await scholarship_dal.get_organization_scholarships()
    if included_submissions:
        submissions = await submissions_service.get_all_submissions_to_organization()
        for scholarship in scholarships:
            for submission in submissions:
                if ScholarshipFields.submitted not in scholarship:
                    scholarship[ScholarshipFields.submitted] = [submission]
                else:
                    scholarship[ScholarshipFields.submitted].append(submission)
    return ok(scholarships)


async def add_scholarships(data):
    resp: DatabaseResponse = await scholarship_dal.add_scholarships(data)
    if resp.status:
        ret_val = ok_code(code=resp.message)
    else:
        ret_val = error_resp(code=resp.message)
        logger_service.error(resp.message.name)
    return ret_val


async def delete_scholarships(scholarships_name):
    if scholarships_name is None:
        return error_resp(code=error_constants.ErrorCode.ScholarshipsNotFound)

    resp: DatabaseResponse = await scholarship_dal.delete_scholarships(scholarships_name)
    if resp.status:
        ret_val = ok_code(code=resp.message)
    else:
        ret_val = error_resp(code=resp.message)
        logger_service.error(resp.message.name)
    return ret_val


async def update_scholarships(new_data):
    data_to_update = await scholarship_dal.get_scholarship_details(new_data[ScholarshipFields.id],
                                                                   for_organization=True)
    if data_to_update is None:
        ret_val = error_resp(code=error_constants.ErrorCode.ScholarshipsNotFound,
                             message=error_constants.ErrorConstant.ScholarshipsNotFound)
        logger_service.error(error_constants.ErrorConstant.ScholarshipsNotFound)
    else:
        def update_field(field, allow_none=False):
            new_value = new_data.get(field, None)
            if allow_none or new_value is not None:
                data_to_update[field] = new_value

        update_field(ScholarshipFields.scholarship_type, allow_none=False)
        update_field(ScholarshipFields.conditions, allow_none=False)
        update_field(ScholarshipFields.description, allow_none=True)
        update_field(ScholarshipFields.eligible_type, allow_none=False)
        update_field(ScholarshipFields.final_date_to_confirm, allow_none=False)
        update_field(ScholarshipFields.final_date_to_approval, allow_none=False)
        update_field(ScholarshipFields.documents_required, allow_none=False)

        resp: DatabaseResponse = await scholarship_dal.update_scholarships(data_to_update)
        if resp.status:
            ret_val = ok_code(code=resp.message)
        else:
            ret_val = error_resp(code=resp.message)
            logger_service.error(resp.message.name)
    return ret_val

