from datetime import datetime
import flask_login
from server.base_services.base_controller import ok, error_resp
from server.constants import error_constants
from server.constants.fields_name.scholarship_fields import ScholarshipFields
from server.constants.fields_name.submitted_scholarships_fields import SubmittedScholarshipsFields
from server.enums.submission_status import SubmissionStatusEnum
from server.dal.dal_contracts.interface_scholarships_dal import IScholarshipsDal
from server.dal.dal_contracts.interface_submission import ISubmissionsDal
from server.injector.dependency_injector import get_singleton
from server.logger import logger_service
from server.models.responses import DatabaseResponse
from server.models.users.organizations_user import OrganizationsUser

submissions_dal: ISubmissionsDal = get_singleton(ISubmissionsDal)
scholarship_dal: IScholarshipsDal = get_singleton(IScholarshipsDal)


async def submit(submission_data):
    ret_val = error_resp(code=error_constants.ErrorCode.SubmissionError)
    scholarships_id = submission_data.get(SubmittedScholarshipsFields.scholarship_id, None)

    scholarship_data = await scholarship_dal.get_scholarship_details(scholarships_id)
    if scholarship_data is None:
        logger_service.error(error_constants.ErrorConstant.ScholarshipNotFound)
        return ret_val

    is_allowed: DatabaseResponse = is_submission_allowed(submission_data)
    if not is_allowed.status:
        logger_service.warning(error_constants.ErrorConstant.SubmissionNotAllowed)
        ret_val = is_allowed.information, 400
        return ret_val

    user_submissions = await get_user_submissions()
    if user_submissions is not None and \
            len([x for x in user_submissions if x[SubmittedScholarshipsFields.scholarship_id] == scholarships_id]) > 0:
        logger_service.info(error_constants.ErrorConstant.DuplicateSubmission)
        ret_val = error_resp(code=error_constants.ErrorCode.duplicateSubmission,
                             message=error_constants.ErrorConstant.DuplicateSubmission)
        return ret_val

    submission_data[SubmittedScholarshipsFields.submission_statuses] = [{
        SubmittedScholarshipsFields.SubmissionStatusFields.submission_status:
            SubmissionStatusEnum.submitted.value,
        SubmittedScholarshipsFields.SubmissionStatusFields.date:
            datetime.now(),
        SubmittedScholarshipsFields.SubmissionStatusFields.free_text:
            submission_data.get(SubmittedScholarshipsFields.SubmissionStatusFields.free_text, None),
        SubmittedScholarshipsFields.SubmissionStatusFields.description: None,
        SubmittedScholarshipsFields.SubmissionStatusFields.requirements: None
    }]
    submission_data[SubmittedScholarshipsFields.organization_id] = scholarship_data[ScholarshipFields.organization_id]
    response: DatabaseResponse = await submissions_dal.add_submissions(submission_data)
    if not response.status:
        logger_service.critical(response.message)
        return ret_val

    ret_val = ok(status=response.status)
    return ret_val


async def get_user_submissions():
    submissions = await submissions_dal.get_user_submissions()
    for submission in submissions:
        submission.pop(SubmittedScholarshipsFields.is_active)
    return submissions


async def response_to_submission(response):
    ret_val = error_resp(code=error_constants.ErrorCode.SubmissionError)
    scholarships_id = response.get(SubmittedScholarshipsFields.scholarship_id, None)
    new_status = response.get(SubmittedScholarshipsFields.SubmissionStatusFields.submission_status, None)
    if not SubmissionStatusEnum.has_value(new_status):
        logger_service.error(error_constants.ErrorConstant.InvalidStatus)
        return ret_val

    scholarship_data = await scholarship_dal.get_scholarship_details(scholarships_id)

    if scholarship_data is None:
        logger_service.error(error_constants.ErrorConstant.ScholarshipNotFound)
        return ret_val

    user: OrganizationsUser = flask_login.current_user
    if scholarship_data[ScholarshipFields.organization_id] != user.get_organization_id():
        logger_service.error(error_constants.ErrorConstant.NotBelong)
        return ret_val

    submission_id = response.get(SubmittedScholarshipsFields.submission_id, None)
    new_data = {
        SubmittedScholarshipsFields.SubmissionStatusFields.submission_status:
            new_status,
        SubmittedScholarshipsFields.SubmissionStatusFields.date:
            datetime.now(),
        SubmittedScholarshipsFields.SubmissionStatusFields.free_text:
            response.get(SubmittedScholarshipsFields.SubmissionStatusFields.free_text, None),
        SubmittedScholarshipsFields.SubmissionStatusFields.description:
            response.get(SubmittedScholarshipsFields.SubmissionStatusFields.description,None),
        SubmittedScholarshipsFields.SubmissionStatusFields.requirements:
            response.get(SubmittedScholarshipsFields.SubmissionStatusFields.requirements,None)
    }
    is_open = response.get(SubmittedScholarshipsFields.is_open, True)
    response = await submissions_dal.update_submission_statuses(submission_id, scholarships_id, new_data, is_open)
    if response is None:
        logger_service.error(error_constants.ErrorConstant.SubmissionsNotFound)
        return ret_val
    ret_val = ok(response)
    return ret_val


async def get_all_submissions_to_organization():
    return await submissions_dal.get_all_by_key(
        SubmittedScholarshipsFields.organization_id, flask_login.current_user.get_organization_id()
    )


def is_submission_allowed(submission_data) -> DatabaseResponse:
    user_data = flask_login.current_user
    return DatabaseResponse()


def get_requirements(scholarships_names):
    """
    :param scholarships_names: array of the names of the requested scholarships
    :return: all the requirements for scholarship
    """
    # asdsdf = self.dal_service.get_requirements(scholarships_names)
    # return self.dal_service.get_requirements(scholarships_names)

    return ["candidate_id", "candidate_current_account",
            "father_vehicle_licence"]


async def send_submission(scholarships_names, files_paths):
    pass
