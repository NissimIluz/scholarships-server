import uuid
from datetime import datetime, timezone
from flask_login import current_user
from werkzeug.security import generate_password_hash
from server import configuration
from server.authentication import login_service, token_service
from server.base_services.base_controller import error_resp, ok
from server.constants.fields_name.users.candidate_fields import CandidateFields, AcceptTerms
from server.constants.database_constants.objnames import ObjNames
from server.constants.fields_name.users.users_fields import UsersFields
from server.constants.error_constants import ErrorCode
from server.constants.requirements_names import RequirementsNames
from server.dal.dal_contracts.interface_resources_dal import IResourcesDal
from server.enums.registration_status import RegistrationStatus
from server.injector.dependency_injector import get_singleton
from server.models.responses import DatabaseResponse
from server.services import scanner_service, resources_service
from server.dal.dal_contracts.interface_users_dal import IUsersDal

user_dal: IUsersDal = get_singleton(IUsersDal)
resources_dal: IResourcesDal = get_singleton(IResourcesDal)


async def register_step1(step1_data, id_file):
    username = step1_data.get(CandidateFields.username, str(uuid.uuid4()))
    requirement_name = RequirementsNames.candidate_id

    id_file_path = resources_service.save_file_locally(id_file, requirement_name, username)
    scan_result = scanner_service.scan(id_file_path, requirement_name)

    if scan_result:
        resources_save_result: DatabaseResponse = await resources_dal.save_or_update_file(username, id_file_path,
                                                                                          scan_result, requirement_name)
        if resources_save_result.status:
            new_candidate = mapping_step1(step1_data, username)
            add_candidate_result: DatabaseResponse = await user_dal.add_candidate(new_candidate)
            if add_candidate_result.status:
                token = token_service.create_token(
                    user=new_candidate, is_registered=False,
                    user_identity=ObjNames.SignedUp
                )
                response = ok(token=token)
            else:  # add_candidate field
                fields = []
                if configuration.return_duplicate_keys:
                    for key in list(add_candidate_result.information.keys()):
                        if key != CandidateFields.is_active:
                            if key != CandidateFields.id:
                                fields.append(key)
                            else:
                                fields.append(CandidateFields.username)
                response = error_resp(add_candidate_result.message, fields)
        else:  # save file failed
            response = error_resp(resources_save_result.message)
    else:  # file not approve
        response = error_resp(ErrorCode.registerFailedFileNotApproved)
    return response


async def register_step2(step2, student_permit):
    username = current_user.get_user_name()
    requirement_name = RequirementsNames.student_certificate
    student_permit_file_path = resources_service.save_file_locally(student_permit, requirement_name, username)
    scan_result = scanner_service.scan(student_permit_file_path, requirement_name)
    if scan_result:
        resources_save_result: DatabaseResponse = await resources_dal.save_or_update_file(username,
                                                                                          student_permit_file_path,
                                                                                          scan_result, requirement_name)
        if resources_save_result.status:
            response = await update_study_details(step2, is_registration=True)
        else:
            response = error_resp(resources_save_result.message)
    else:  # file not approve
        response = error_resp(ErrorCode.registerFailedFileNotApproved)
    return response


def register_step3(step3):
    return update_income(step3, is_registration=True)


async def register_step4(step4):
    if step4[AcceptTerms.accept_terms]:
        step4[AcceptTerms.accept_terms_date] = datetime.now()
        new_data = {
            CandidateFields.accept_terms: step4,
            CandidateFields.registration_status: RegistrationStatus.registered.value
        }
        update_result = await user_dal.find_one_and_update_user(new_data, ObjNames.Candidates, RegistrationStatus.step3, update_last=False)
        if update_result.status:
            ret_val = await login_service.logged_in_user(update_result.information, ObjNames.Candidates)

        else:
            ret_val = error_resp(update_result.message)
    else:  # user doesnt accept terms
        ret_val = error_resp(ErrorCode.registerFailedTermsNotApproved)
    return ret_val


async def update_study_details(update_data, is_registration=False):
    ret_val = None

    if update_data[CandidateFields.national_service]:
        national_service_start_date = update_data.get(CandidateFields.national_service_start_date)
        national_service_end_date = update_data.get(CandidateFields.national_service_end_date)
        now = datetime.now(tz=timezone.utc)
        if not national_service_start_date or national_service_start_date > national_service_end_date \
                or national_service_start_date > now:
            ret_val = error_resp(ErrorCode.registerFailedNationalDateError)
    if update_data[CandidateFields.study_start_year].year > now.year or \
            update_data[CandidateFields.study_current_year] > configuration.max_study_year:
        ret_val = error_resp(ErrorCode.registerFailedStudyDateError)
    if ret_val is None:
        copy_data = {
            CandidateFields.national_service: update_data.get(CandidateFields.national_service),
            CandidateFields.national_service_start_date: update_data.get(CandidateFields.national_service_start_date),
            CandidateFields.national_service_end_date: update_data.get(CandidateFields.national_service_end_date),
            CandidateFields.college_name: update_data.get(CandidateFields.college_name),
            CandidateFields.college_id: update_data.get(CandidateFields.college_id),
            CandidateFields.study_start_year: update_data.get(CandidateFields.study_start_year),
            CandidateFields.study_current_year: update_data.get(CandidateFields.study_current_year),
            CandidateFields.field_of_study: update_data.get(CandidateFields.field_of_study),
            CandidateFields.degree: update_data.get(CandidateFields.degree).value,
            CandidateFields.last_study_update: datetime.now()
        }
        if is_registration:
            copy_data[CandidateFields.registration_status] = RegistrationStatus.step2.value
            registration_status = RegistrationStatus.step1
        else:
            registration_status = RegistrationStatus.registered
        update_result: DatabaseResponse = await user_dal.update_user(copy_data, ObjNames.Candidates,
                                                                     registration_status,
                                                                     update_last=not is_registration)
        if update_result.status:
            return ok()
        else:
            return error_resp(update_result.message)


async def update_income(data, is_registration=False):
    if data[CandidateFields.is_allowance]:
        if not data.get(CandidateFields.allowance_income_monthly):
            return error_resp(ErrorCode.registerFailedAllowanceErrors)

    if data[CandidateFields.is_work]:
        if not data.get(CandidateFields.work_income_monthly):
            return error_resp(ErrorCode.registerFailedWorkErrors)

    copy_data = {
        CandidateFields.is_allowance: data[CandidateFields.is_allowance],
        CandidateFields.is_work: data[CandidateFields.is_work],
        CandidateFields.allowance_income_monthly: data.get(CandidateFields.allowance_income_monthly),
        CandidateFields.work_income_monthly: data.get(CandidateFields.work_income_monthly),
        CandidateFields.last_allowance_update: datetime.now()
    }
    if is_registration:
        registration_status = RegistrationStatus.step2
        copy_data[CandidateFields.registration_status] = RegistrationStatus.step3.value
    else:
        registration_status = RegistrationStatus.registered
    response = await user_dal.update_user(copy_data, ObjNames.Candidates, registration_status,
                                          update_last=not is_registration)
    if response.status:
        return ok()
    else:
        return error_resp(response.message)


async def add_candidate(data):
    data[UsersFields.password] = generate_password_hash(data[UsersFields.password])
    resp: DatabaseResponse = await user_dal.add_candidate(data)
    if resp.status:
        token = token_service.create_token(data)
        ret_val = ok(token=token)
    else:
        ret_val = error_resp(code=resp.message.value)
    return ret_val


def login(json_data):
    return login_service.login(json_data, ObjNames.Candidates)


def login_by_otp_step_1(json_data):
    return login_service.login_by_otp_step_1(json_data, ObjNames.Candidates)


def login_by_otp_step_2(json_data):
    return login_service.login_by_otp_step_2(json_data)


async def delete():
    resp: DatabaseResponse = await user_dal.delete_user()
    if resp.status:
        ret_val = ok(code=resp.message.value)
    else:
        ret_val = error_resp(code=resp.message.value)
    return ret_val


async def update(new_data):
    data_to_update = current_user.get_user_data(all_included=True)

    def update_field(field, allow_none=False):
        new_value = new_data.get(field, None)
        if allow_none or new_value is not None:
            data_to_update[field] = new_value

    update_field(UsersFields.email, allow_none=False)
    update_field(UsersFields.phone_number, allow_none=False)

    new_password = new_data.get(UsersFields.password, None)
    if new_password is not None:
        data_to_update[UsersFields.password] = generate_password_hash(new_password)

    resp: DatabaseResponse = await user_dal.update_user(data_to_update)
    if resp.status:
        if new_password is not None:
            token = token_service.create_token(data_to_update, user_identity=ObjNames.Candidates)
            ret_val = ok(code=resp.message.value, token=token)
        else:
            ret_val = ok(code=resp.message.value)
    else:
        ret_val = error_resp(code=resp.message.value)
    return ret_val


def get_user_data():
    user_json = current_user.get_user_data()
    ret_val = ok(user_json)  # get this user data
    return ret_val


def mapping_step1(step1_data, username=None):
    password = generate_password_hash(step1_data.get(CandidateFields.password, step1_data[CandidateFields.id_number]))
    return {
        CandidateFields.registration_status: RegistrationStatus.step1.value,
        CandidateFields.first_name: step1_data[CandidateFields.first_name],
        CandidateFields.last_name: step1_data[CandidateFields.last_name],
        CandidateFields.id_number: step1_data[CandidateFields.id_number],
        CandidateFields.birth_date: step1_data[CandidateFields.birth_date],
        CandidateFields.username: username,
        CandidateFields.email: step1_data[CandidateFields.email],
        CandidateFields.password: password,
        CandidateFields.phone_number: step1_data[CandidateFields.phone_number],
        CandidateFields.city: step1_data[CandidateFields.city],
        CandidateFields.street: step1_data[CandidateFields.street],
        CandidateFields.street_number: step1_data[CandidateFields.street_number],
        CandidateFields.national_service: None,
        CandidateFields.national_service_start_date: None,
        CandidateFields.national_service_end_date: None,
        CandidateFields.college_name: None,
        CandidateFields.college_id: None,
        CandidateFields.study_start_year: None,
        CandidateFields.study_current_year: None,
        CandidateFields.field_of_study: None,
        CandidateFields.degree: None,
        CandidateFields.is_allowance: None,
        CandidateFields.is_work: None,
        CandidateFields.allowance_income_monthly: None,
        CandidateFields.work_income_monthly: None,
        CandidateFields.last_study_update: None,
        CandidateFields.last_allowance_update: None,
        CandidateFields.accept_terms: {AcceptTerms.accept_terms_date: None, AcceptTerms.accept_terms_date: False}
    }
