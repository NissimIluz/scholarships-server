import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from server import configuration
from server.constants import email_constants
from server.logger import logger_service


async def send_email(to, subject, text):
    try:
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = configuration.gmail_user
        msg['To'] = to
        text = MIMEText(text)
        msg.attach(text)
        server = aiosmtplib.SMTP(hostname=configuration.email_api_hostname, port=configuration.email_api_port)
        await server.connect()
        await server.starttls()
        await server.login(configuration.gmail_user, configuration.gmail_pwd)
        await server.sendmail(configuration.gmail_user, to, msg.as_string())
        await server.quit()
        return True
    except Exception as ex:
        logger_service.critical(ex)
        return False


def send_otp_email(to, otp):
    return send_email(to, email_constants.otp_subject, email_constants.otp_text.replace("{0}", otp))

'''
def sendmail(to:[],SUBJECT,text):
    try:
      gmail_user = "scholarshipgo09@gmail.com"
      gmail_pwd = "May12@5857335"
      server = smtplib.SMTP('smtp.gmail.com', 587)
      server.ehlo()
      server.starttls()
      server.login(gmail_user, gmail_pwd)

      body = '\r\n'.join(['To: %s' % to,
                          'From: %s' % gmail_user,
                          'Subject: %s' % SUBJECT,
                          '', text])
      server.sendmail(gmail_user,to , body)
      server.close()
      return True
    except Exception as ex:
       print(ex)
       return False





async def send_subscribe_email(scholarship_email, candidate_full_name,candidate_details, user_name = -1):
    apply_for_a_scholarship = " הגיש/ה בקשה למלגה"

    gmail_user = "scholarshipgo09@gmail.com"
    gmail_pwd = "May12@5857335"

    relative_path: str = f"Uploaded files\\{user_name}"
    folder_path = os.path.abspath(relative_path)

    msg = MIMEMultipart()
    msg['Subject'] = candidate_full_name + apply_for_a_scholarship
    msg['From'] = gmail_user
    msg['To'] = scholarship_email
    text = MIMEText(candidate_details)
    msg.attach(text)

    for filename in os.listdir(folder_path):

        with open(folder_path +"\\" +filename, 'rb') as f:
            img_data = f.read()
            image = MIMEImage(img_data, name=os.path.basename(filename))
            msg.attach(image)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(gmail_user, scholarship_email, msg.as_string())
    server.quit()



async def send_subscribe_email(scholarship_email, candidate_full_name,candidate_details, user_name = -1):
    apply_for_a_scholarship = " הגיש/ה בקשה למלגה"

    gmail_user = "scholarshipgo09@gmail.com"
    gmail_pwd = "May12@5857335"

    relative_path: str = f"Uploaded files\\{user_name}"
    folder_path = os.path.abspath(relative_path)

    msg = MIMEMultipart()
    msg['Subject'] = candidate_full_name + apply_for_a_scholarship
    msg['From'] = gmail_user
    msg['To'] = scholarship_email
    text = MIMEText(candidate_details)
    msg.attach(text)
    for filename in os.listdir(folder_path):

        with open(folder_path +"\\" +filename, 'rb') as f:
            img_data = f.read()
            image = MIMEImage(img_data, name=os.path.basename(filename))
            msg.attach(image)

    server =  aiosmtplib.SMTP(hostname='smtp.gmail.com', port=587)
    await server.connect()
    await server.starttls()
    await server.login(gmail_user, gmail_pwd)
    await server.sendmail(gmail_user, scholarship_email, msg.as_string())
    await server.quit()

# asyncio.run(send_subscribe_email('eiloz61@gmail.com', "ניסים אילוז", "רווק, 26, חשמונאים, סטודנט למדעי המחשב"))
# SUBJECT = "PumbaParkingAllert"
# text = "Parking spot number 1  available at Shalom-Haliechem 32,Keren Hchayedet"
# sendmail("eiloz61@gmail", SUBJECT, text)
# sendmail('eiloz61@gmail.com',SUBJECT,text)
'''

