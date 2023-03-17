from server.constants.fields_name.base_fields import BaseFields
from server.constants.fields_name.users.users_fields import UsersFields


class CandidateFields(UsersFields):

    # Gannet in the server
    id = BaseFields.id  # in candidate equals to username  # inner
    is_active = BaseFields.is_active  # inner
    create_by = BaseFields.create_by  # inner
    create_date = BaseFields.create_date  # type: dateTime, details: user last logging
    update_date = BaseFields.update_date  # type: dateTime, details: user last logging
    last_login = 'lastLogin'  # type: dateTime, details: user last logging
    last_session = 'lastSession'  # inner
    login_attempt = 'loginAttempt'  # inner
    last_login_attempt = 'lastLoginAttempt'  # inner
    registration_status = UsersFields.registration_status # type: enum,  user registration status
    '''
    enum registrationStatus:
        200 - registered
        1 - step1 (completed)
        2 -  step2 (completed)
        3 -  step3 (completed) 
        44 - blocked
    '''

    # step 1

    ## keys
    username = 'username'  # KEY, unrequired - when empty equals the email address,  type: string, regex_pattern: userName, details: user username
    email = 'email'  # KEY, required, type: email(string) details: user email address
    password = 'password'  # required, type: string, regex_pattern: password, details: user password
    id_number = 'idNumber'  # KEY,required, type: string, regex_pattern: name, details: user first name
    phone_number = 'phoneNumber'  # KEY, required, type: string, regex_pattern: phone, details: user phone number

    ## not key
    first_name = 'firstName'  # KEY, required, type: string, regex_pattern: name, details: user first name
    last_name = 'lastName'  # required, type: string, regex_pattern: name, details: user first name
    birth_date = "birthDate"  # required, type: string, regex_pattern: name, details: user first name

    ## address
    city = 'city'  # Will determine after the decision
    street = 'street'  # Will determine after the decision
    street_number = 'streetNumber'  # Will determine after the decision
    zip_code = 'zipCode'

    id_file = 'idFile'  # required, type: file, details: id file (צילום תעודת זהות)



    # step2
    national_service = 'nationalService'  # required, type: Boolean, details: Has the candidate performed national service?(האם ביצע שירות צבאי/אזרחי)
    national_service_start_date = 'nationalServiceStartDate'  # unrequired (required only if nationalService==true), type: Boolean, regex_pattern: phone, details: national service start Date(תאריל תחילת השירות)
    national_service_end_date = 'nationalServiceEndDate'  # unrequired type: Boolean, regex_pattern: phone, details: national service ent Date(תאריך סיום השירות)
    college_name = 'collegeName'  # required, type: string, regex_pattern: name, details: candidate college name
    college_id = 'collegeId' # for now unrequired
    study_start_year = 'studyStartYear'  # required, type: DateTime, details: study start year
    study_current_year = 'studyCurrentYear'   # required, type: Number, details: study Current Year
    field_of_study = 'fieldOfStudy'  # required, type: string, regex_pattern: name, details: user first name
    degree = 'degree'  # enum(number) - 1:first degree,2: second degree,3: third degree
    student_permit = 'studentPermit'  # required, type: file, details: student_permit
    last_study_update = 'lastStudyUpdate'  # inner last step2 update
    token = 'token'  # Bearer-token required, type: string, details: token

    # step3
    is_allowance = 'isAllowance'  # required, type: Boolean, detail:are receives an allowance (האם מקבל קצבה)
    is_work = 'isWork'  # required, type: Boolean, detail:are working (האם עובד-בתשלום)
    allowance_income_monthly = 'allowanceIncomeMonthly'  # unrequired (required if isAllowance==true) detail:allowance amount (סכום קצבה)
    work_income_monthly = 'workIncomeMonthly'  # unrequired (required if is_work==true), detail:income from work (סכום משכורת מהעבודה)
    last_allowance_update = 'lastAllowanceUpdate' # inner last step3 update
    token = 'token'  # Bearer-token required, type: string, details: token,

    # step4
    token = 'token'  # Bearer-token required, type: string, details: token
    accept_terms = 'acceptTerms'


class AcceptTerms:
    accept_terms = 'acceptTerms'  # required, type: Boolean
    accept_terms_date = 'acceptTermsDate'  # inner
