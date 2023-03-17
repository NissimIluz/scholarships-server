# scholarships-server


## Setup, Installation and Running The App in AWS

Make sure you have Python 3.10 installed.

### running the server:
```bash
python main_production.py
```
### install requirements
```bash
pip  install -r requirements.txt
```


## Setup, Installation and Running The App in localhost

Make sure you have Python 3.10 installed.

run this command on the server folder:
```bash
pip  install -r requirements.txt
```
for install the requirements packages

### Running The App

```bash
python main.py
```




# HTTPS Requests
## Scholarships
### ``` scholarships``` (get) - open to all
output - json with all Scholarships.

 בקשה המאפשרת לקבל את כול המלגות השמורות במסד נתנונים.



### ```scholarships/add``` (post) - open only for OrganizationContact
input - json with Scholarship details or Scholarships array + authorization token

output - json with status .

מקבלת פרטי מלגה לרישום או מערך של מלגות לרישום. אין צורך לתת מזהה ארגון (נלקח מהנתונים של איש הקשר)


### ```scholarships/delete?scholarshipName=***hereWritescholarshipName***``` (delete) - open only for OrganizationContact
input - json with Scholarship name ***name*** + authorization token

output - json with status .

מקבלת את שם המלגה (ID)

ומבצע מחיקה של המלגה


### ```scholarships/update``` (PUT) - open only for OrganizationContact
input - json with Scholarship details  + authorization token

output - json with status .

מקבלת פרטי מלגה לעידכון (יש שדות שחסומים לעדוכן) 


### ```scholarships/getOrganizationScholarships?includedSubmissions=true``` (GET) - open only for OrganizationContact

includedSubmissions - are all submissions of the scholarships will be included in the scholarship data <br/>
output - json Scholarships List .

מחזיר את רשימת המלגות של ארגון



## candidates


### ```candidates/addCandidates``` (post) - open to HelpDesk
input - json with username and password.

output - json with token .

מחזיר גסון עם טוקן . תקוף הטוקן מוגדר ב

configuration.exp_token = (24 שעות)


ניתוק אוטמטי של המשתמש מתבצע לאחר תום תוקף הפעולה (נמדד מהפעולה האחרונה) תוקף הפעולה מוגדר ב

configuration.exp_session (30 דקות )

(חוסר פעילות)

### ```candidates/login``` (post) -- open to all
input - json with username and password
output - json with token and user details
פתוח לכולם, מקבל שם משתמש וסימה

מחזיר גסון עם טוקן ופרטי המשתמש  . תקוף הטוקן מוגדר ב

configuration.exp_token = (24 שעות)


ניתוק אוטמטי של המשתמש מתבצע לאחר תום תוקף הפעולה (נמדד מהפעולה האחרונה) תוקף הפעולה מוגדר ב

configuration.exp_session (30 דקות )

 (חוסר פעילות)


### ```candidates/loginByOtpStep1``` (post) -- open to all
input - json with email and/or phone number
output - json with otp

פתוח לכולם, מקבל שם מספר טלפון או/ וגם מייל

שולח OTP למייל או לטלפון (בהתאם למי שהוא לא ריק, במידה ושניהם  מתקבלים נשלח רק למיייל)

-- כרגע אין שירות SMS

otp תקף ל 5 דקות 

(exp_otp)

### ```candidates/loginByOtpStep2``` (post) -- open to all
input - json with email and/or phone number and otp
output - json with token and user details

פתוח לכולם, מקבל שם מספר טלפון או/ וגם מייל
יש לוודא שאותם שדות מהבקה הראשונה מגיעים גם לבקשה השניה

מחזיר את פרטי הכניסה

configuration.exp_token = (24 שעות)


ניתוק אוטמטי של המשתמש מתבצע לאחר תום תוקף הפעולה (נמדד מהפעולה האחרונה) תוקף הפעולה מוגדר ב

configuration.exp_session (30 דקות )

 (חוסר פעילות)



### ```candidates/deleteCandidate``` (DELETE) -- open to Candidates

מוחק את המשתמש





### ```candidates/updateCandidate``` (PUT) - open to Candidates
input - json Candidate Details.

output - json with code

מעדכן את פרטי המשתמש (כולל סיסמה)


### ```candidates/getUserData``` (post) - open to Candidates
output -  json with user details

מחזיר את פרטי המשתמש המחבור


## candidates registration:

### ```candidates/registerStep1```  (post) - open to all

input: <br />
   
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
 <br />
output:  <br /> status (= True), token or specific error

 <br />

### ```candidates/registerStep2```  (post) - open to signed_up

input: <br />
    national_service = 'nationalService'  # required, type: Boolean, details: Has the candidate performed national service?(האם ביצע שירות צבאי/אזרחי)
    national_service_start_date = 'nationalServiceStartDate'  # unrequired (required only if nationalService==true), type: Boolean, regex_pattern: phone, details: national service start Date(תאריל תחילת השירות)
    national_service_end_date = 'nationalServiceEndDate'  # unrequired type: Boolean, regex_pattern: phone, details: national service ent Date(תאריך סיום השירות)
    college_name = 'collegeName'  # required, type: string, regex_pattern: name, details: candidate college name <br/>
    college_id = 'collegeId' # for now unrequired
    study_start_year = 'studyStartYear'  # required, type: DateTime, details: study start year
    study_current_year = 'studyCurrentYear'   # required, type: Number, details: study Current Year 
    field_of_study = 'fieldOfStudy'  # required, type: string, regex_pattern: name, details: user first name 
    degree = 'degree'  # enum(number) - 1:first degree,2: second degree,3: third degree
    student_permit = 'studentPermit'  # required, type: file, details: student_permit
    last_study_update = 'lastStudyUpdate'  # inner last step2 update
    token = 'token'  # Bearer-token required, type: string, details: token 
  
 <br />
output:  <br />  status = True or specific error

 <br />

 ### ```candidates/registerStep3```  (post) - open to signed_up candidates

input: <br />

       is_allowance = 'isAllowance'  # required, type: Boolean, detail:are receives an allowance (האם מקבל קצבה)
    is_work = 'isWork'  # required, type: Boolean, detail:are working (האם עובד-בתשלום)
    allowance_income_monthly = 'allowanceIncomeMonthly'  # unrequired (required if isAllowance==true) detail:allowance amount (סכום קצבה)
    work_income_monthly = 'workIncomeMonthly'  # unrequired (required if is_work==true), detail:income from work (סכום משכורת מהעבודה)
    last_allowance_update = 'lastAllowanceUpdate' # inner last step3 update
    token = 'token'  # Bearer-token required, type: string, details: token


 <br />
output:  <br />  status = True or specific error

 <br />


### ```candidates/registerStep4```  (post) - open to signed_up candidates

    token = 'token'  # Bearer-token required, type: string, details: token
    accept_terms = 'acceptTerms'
 <br />
output:  user data with token
 <br />


### ```candidates/registerStep4```  (post) - open to signed_up candidates

input: <br />
 national_service = 'nationalService'  # required, type: Boolean, details: Has the candidate performed national service?(האם ביצע שירות צבאי/אזרחי)
    national_service_start_date = 'nationalServiceStartDate'  # unrequired (required only if nationalService==true), type: Boolean, regex_pattern: phone, details: national service start Date(תאריל תחילת השירות)
    national_service_end_date = 'nationalServiceEndDate'  # unrequired (required only if nationalService==true), type: Boolean, regex_pattern: phone, details: national service ent Date(תאריך סיום השירות)
    college_name = 'collegeName'  # required, type: string, regex_pattern: name, details: candidate college name
    college_id = 'collegeId' # for now unrequired
    study_start_year = 'studyStartYear'  # required, type: DateTime, details: study start year
    study_current_year = 'studyCurrentYear'   # required, type: Number, details: study Current Year
    field_of_study = 'fieldOfStudy'  # required, type: string, regex_pattern: name, details: user first name
    degree = 'degree'  # enum(number) - 1:first degree,2: second degree,3: third degree
    student_permit = 'studentPermit'  # required, type: file, details: student_permit
    token = 'token'  # required, type: string, details: token
 <br />
output:  <br />  statues = True or specific error

 <br />


## organization

### ```organization/login``` (post) -- open to all
input - json with username and password
output - json with token and user details
פתוח לכולם, מקבל שם משתמש וסימה

מחזיר גסון עם טוקן ופרטי המשתמש. תקוף הטוקן מוגדר ב

configuration.exp_token = (24 שעות)


ניתוק אוטמטי של המשתמש מתבצע לאחר תום תוקף הפעולה (נמדד מהפעולה האחרונה) תוקף הפעולה מוגדר ב

configuration.exp_session (30 דקות )

 (חוסר פעילות)


### ```organization/getOrganizationContacts``` (GET) -- open to OrganizationContact

output - json with get organization contact 

מחזיר את אנשי הקשר של הארגון


### ```organization/getOrganizationData``` (GET) -- open to OrganizationContact

output - json with get organization data 

מחזיר את פרטי הארגון

### ```organization/addOrganization``` (post) -- open to all
input - json with organization details included ***contacts*** info
output - json with token 

פתוח לכולם, מקבל את פרטי הארגון שפבנים שדה:

***contacts***

המכיל את **מערך** של אנשי קשר  (לא ניתן לרשום ארגון ללא רישום של איש קשר אחד לפחות)

מוחזר תוקן (של השמשתמש הראשון) בדומה לרישום משתמש


### ```organization/updateOrganization``` (PUT) -- open to OrganizationContact
input - json with organization details included ***contacts*** info

output - json with token 

מקבל את פרטי הארגון לעדכון (ישנם שדות החסומים לעדכון)

### ```organization/addContacts``` (post) -- open to OrganizationContact
input - json with contact info

output - json with token 

פתוח לארגונים (אנשי קשר) בלבד, מקבל את פרטי אנשי הקשר החדשים (מערך) (אין צורך לכלול את פרטי הארגון)

מוחזר תוקן בדומה לרישום משתמש

### ```organization/updateContactupdateContact``` (PUT) -- open to OrganizationContact
input - json with contact info
output - status code

מעדכן את איש הקשר המחובר


### ```organization/deleteContact?usernameToDelete=***here user name here***``` (DELETE) -- open to OrganizationContact
output - status code

מוחק את המשתמש המופיע שניתן בפרמטר (איש קשר יכול למחוק איש קשר אחר באותו ארגון)


### ```organization/deleteContact``` (DELETE) -- open to OrganizationContact
output - status code

מוחק את המשתמש המחובר


### ```organization/deleteOrganization***``` (DELETE) -- open to OrganizationContact
output - status code 



### ``organization/getUserData?usernameToGet=username111``' (GET) --open to OrganizationContact
input - *******optional******* username to get if empty return this user


מחזיר את פרטי המשתמש. כולל שני אןפציות 1. החזרת המשתמש המחובר

(שליחת  ריק או ללאusernameToGet) 

2 קבלת פרטי משתמש אחר יש לשולח את שם המשתמש בפרמטר


### ```organization/loginByOtpStep1``` (post) -- open to all
input - json with email and/or phone number

output - json with otp

פתוח לכולם, מקבל שם מספר טלפון או/ וגם מייל

שולח OTP למייל או לטלפון (בהתאם למי שהוא לא ריק, במידה ושניהם  מתקבלים נשלח רק למיייל)

-- כרגע אין שירות SMS

otp תקף ל 5 דקות 

(exp_otp)

### ```organization/loginByOtpStep2``` (post) -- open to all
input - json with email and/or phone number and otp

output - json with token and user details

פתוח לכולם, מקבל שם מספר טלפון או/ וגם מייל
יש לוודא שאותם שדות מהבקה הראשונה מגיעים גם לבקשה השניה

מחזיר את פרטי הכניסה

configuration.exp_token = (24 שעות)


ניתוק אוטמטי של המשתמש מתבצע לאחר תום תוקף הפעולה (נמדד מהפעולה האחרונה) תוקף הפעולה מוגדר ב

configuration.exp_session (30 דקות )

 (חוסר פעילות)


## submissions

###  ```submit``` (post) -- authorized (candidates only) 
input - json with scholarshipId <br />
output - json with the response


### ```responseToSubmission``` (put) --organization contact

input - json { <br />
{
 scholarshipId, <br />
&ensp; SubmissionStatus, <br />
&ensp; submissionId, <br />
&ensp; isOpen:boolean - optional boolean default true,<br />
&ensp; description - optional <br />
&ensp; freeText - optional<br />
&ensp; requirements - optional<br />
  }

output - json with the submissions detiels

SubmissionStatus:
    submitted = 0,
    approved = 10,
    denied = 20


### ```getUserSubmissions``` (get) --candidates
output - json with all user submissions

### ```getAllSubmissionsToOrganization``` (get) --organization contact 
output - json with all submissions to organization

## contactUs

### ```organizationRegistration``` (post) - open to all
input - name, email, phoneNumber
output - success, contactId

## data

### ```data/regexPattern``` (GET) - open to all

output - response dto with all regexPattern


### ```data/regexPatternByName?regexName=name``` (GET) - open to all
input - regexName
output - regex

### ```data/filesType``` (GET) - open to all

output - response dto with all filesType

### ```data/areaCode``` (GET) - open to all

output - response dto with all areaCodes


# Errors and Errors Code

if error error code return in json with errorCode filed

בשגיאה מוחזר גסון עם תוקן המכיל את קוד השגיאה.
## ErrorCode
    GenericError = 0  # (HTTP response status code 400)
    SessionExpired = 1  # (HTTP response status code 401)
    Unauthorized = 2  # (HTTP response status code 401)
    UserLoginError = 401  # "שם משתמש או סיסמא לא נוכונים או שנדרשת כניסה מחדש"
    OtpNotFound = 403
    OtpLoginAttempts = 40100  # יותר מידי ניסיונות התחברות עם ה OTP
    UsedOtp = 40101
    UserTemporarilyBlocked = 40102  # משתמש נחסם זמנית
    UserPermanentlyBlocked = 40103  # משתמש נחסם בשל ריבוי כניסות (יש צורך לשחרר את החסימה)
    ContactExists = 3  # (HTTP response status code 400)
    AtLeastOneContactIsRequired = 4  # (HTTP response status code 400)
    ScholarshipsNotFound = 5  # (HTTP response status code 400)
    UnknownError = 23  # (HTTP response status code 400)
    UserNotFound = 6  # (HTTP response status code 401)
    OtpNotSent = 7  # (HTTP response status code 400)
    SubmissionError = 712  # (HTTP response status code 400)
    duplicateSubmission = 713  # (HTTP response status code 400)
    invalidFile = 12
    invalidData = 13
    registerFailed = 500
    registerFailedFileNotApproved = 501
    registerFailedNationalDateError = 502
    registerFailedStudyDateError = 503
    registerFailedWorkErrors = 504
    registerFailedScholarshipReceive = 505
    registerFailedTermsNotApproved = 506
    registerFailedAllowanceErrors = 507

## Database Responses
      Succeeded = 200 # (HTTP response status code 200) # הצלחה

    """ HTTP response status code 400 """
    MultyErrors = 1202
    UnknownError = 1203
    DuplicateKeyError = 1210 # המפתח הנוכחי כבר קיים
    UpdateFail = 1406


## Helpdesk

.בינתיים פתוח לכולם

שליחת הבקשה להצגת הסטודנטים במערכת נעשית ע"י: 
### ```getStudents``` (get)

הפונקציה מאפשרת לבצע חיפוש עפ"י שדות(רק סטודנטים פעילים כברירת מחדל)-
1. take - מאפשר לבחור כמה סטודנטים יחזיר השירות.
ערך חובה גדול מ 0 וקטן או שווה ל1000
2. skip - מאפשר לבחור מאיזה סטודנט להתחיל את הבאת הסטודנטים.
ערך חובה, גדול או שווה ל 0 וקטן או שווה ל1000
3. שם פרטי של הסטודנט(firstName)
2. שם משפחה של הסטודנט(lastName)
3. מספר תעודת הזהות של הסטודנט(idNumber)
4. האימייל של הסטודנט(email)
5. שדה חופשי לבחירת המשתמש(phrase)
5. אפשרות בחירה להצגת המשתמשים הפעילים בלבד או כל המשתמשים הרשומים במערכת שעונים על הדרישות(onlyActive)
6. אפשרות לבחירת השדה על פיו אנו רוצים למיין את התוצאות(orderBy)- שם משפחה כברירת מחדל
7. אפשרות לבחירת סדר המיון(עולה או יורד) לפי שדה 6 שנבחר(orderDirection)-סדר עולה כברירת מחדל 
