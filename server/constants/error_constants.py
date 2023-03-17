from enum import Enum, IntEnum


class ErrorConstant(Enum):
    ScholarshipsNotFound = "Scholarships not found"
    IncorrectUsername = "user name not found"
    GenericError = "generic error"
    Unauthorized = "unauthorized"
    Incorrect_password = "incorrect password"
    UserNotFound = "reenter required \\ user not found"
    User_is_inactive = "משתמש לא פעיל"
    SubmitError = "התרחשה שגיאה בעת הגשת המלגות, אנא פנה לשירות לקוחות"
    NoOpenChat = "there is no open chat for user"
    InvalidFile = "Invalid File"
    NoUserName = "no username"
    NotFound = "Not Found"
    OtpNotFound = "OTP Not Found"
    OtpLoginAttempts = "Too much attempt to connect to this user"
    UsedOtp = "this otp has been used"
    StolenToken = "Stolen Token / headers not accepted . headers: "
    UserTemporarilyBlocked = "User temporarily blocked."
    UserPermanentlyBlocked = "User permanently locked."
    IncorrectOtp = "incorrect otp code"
    OtpNotSend = "Otp not send"
    ScholarshipNotFound = "scholarship not found"
    SubmissionNotAllowed = "submission not allowed"
    DuplicateSubmission = "duplicate submission"
    NotBelong = "scholarship not belong to this organization"
    InvalidStatus = "Invalid Status"
    SubmissionsNotFound = "Submissions not Found"
    InvalidInput = "InvalidInput"


class ErrorCode(IntEnum):
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
