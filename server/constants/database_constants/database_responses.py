from enum import Enum


class Responses(Enum):
    Succeeded = 200 # (HTTP response status code 200) # הצלחה

    """ HTTP response status code 400 """
    MultyErrors = 1202
    UnknownError = 1203
    DuplicateKeyError = 1210 # המפתח הנוכחי כבר קיים
    UpdateFail = 1406



    ''' ----------------------------------------- old ------------------------------------------------'''




    DUPLICATE_PRIMARY_KEY = "משתמש זה כבר קיים"
    IntegrityError = "פקודה זה סותרת את המבנה של בסיס הנתונים"
    UniqueConstraintViolation = "טפוס"
    NoReferenceError = "אין מפתח זר"
    ScholarshipNameNotExist = "המלגה אינה קיימת במערכת"
    UsernameTaken = "שם המשתמש תפוס"


    UserNotExist = "משתמש לא קיים"
    NoErrors = "בוצע"
    OrganizationNameNotExist = "הארגון לא קיים במערכת"
    OrganizationNameOrEmailToken = "שם המלגה טפוס או שכתובת המייל קיימת במערכת"
    IncorrectPassword = "סימסה לא נכונה"
    CandidateInsertError = "לא ניתן להניס את המשתמש. יתכן וקיים משתמש אם ת.ז. או מייל זהה."
    EmailExist = "מייל זה קיים במערכת"
    PhoneExist = "מספר פלאפון קיים במערכת"

    PropertyExist = "נכס זה כבר קיים במערכת"