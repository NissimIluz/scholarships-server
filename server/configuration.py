""" app """
development_mode = True
return_duplicate_keys = True
validate_input = True
encryption_key = b'KFUBdKsihWE4TK88_Bv3zQebJDNGsmgpZS9UZ9tkVKg='

""" database """
# https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-5.0.5-signed.msi
# mangoDB_connection = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'
mangoDB_connection = 'mongodb+srv://database1:database1@cluster0.eiw6k.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
# mangoDB_connection = 'mongodb+srv://nissim:kzda8qSWgl6Y3XVa@cluster0.f1r39y7.mongodb.net/?retryWrites=true&w=majority' # nissim
database_name = 'scholarship5Gdatabase'
sql_name = 'SqlDatabase//sqlDatabase.db'
maxPoolSize = 1

''' logger'''
print_from_level = 0  # info = 0, warning = 1, error = 2, critical = 3

""" jwt """
jwt_key = "156sdf#@$fsd#FS+er+a#%^13F"
encryption_algorithm = "HS256"

""" authorization """
exp_token = 120  # minutes
exp_token_for_guests = 3  # hours
exp_session = 30  # minutes (Re-identification requirement)
max_login_attempt = 100
block_after_login_attempt = 5
block_user_for = 5  # minutes

""" otp """
otp_digits = "0123456789"
otp_length = 6
exp_otp = 5  # minutes (time until otp expired)
print_otp = True  # print the OTPs when they are generated
send_otp_to_email = False  # send to otp to the user email
send_otp_to_phone_number = False  # send to otp to the user in sms
otp_max_attempt = 5
return_otp = True  # only when development_mode = True

""" email service """
gmail_user = "scholarshipgo09@gmail.com"
gmail_pwd = "May12@5857335"
email_api_hostname = 'smtp.gmail.com'
email_api_port = 587

""" cache memory """

""" cache memory: maxsize"""
maxsize = 1024

""" cache memory: Time To Live in seconds"""
get_all_scholarships_ttl = 1800  # Time To Live in seconds
get_data = 86400  # Time To Live in seconds


"""   contact_us   """

contact_us_organization_registration_email = "scholarshipgo09@gmail.com"
contact_us_organization_registration_subject = "צור קשר"
contact_us_text = "מבקש ליצור קשר"
contact_us_email = "כתובת מייל"
contact_us_phone_number = "מספר טלפון"
contact_us_id = "מזהה פניה"


''' general '''
max_study_year = 20
