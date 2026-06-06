import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailManager:
    def __init__(self, mail_smtp, mail_imap, login, password):
        self.mail_smtp = mail_smtp
        self.mail_imap = mail_imap
        self.login = login
        self.password = password
    
    def send_message(self, recipients: list, subject: str, message_text: str):
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message_text))

        try:
            with smtplib.SMTP(self.mail_smtp, 587) as ms:
                ms.ehlo()
                ms.starttls()
                ms.ehlo()
                ms.login(self.login, self.password)
                ms.sendmail(self.login, recipients, msg.as_string())
            print("The email was sent successfully")
        except Exception as e:
            print(f"The email was not sent: {e}")
    
    def receive_message(self, folder: str, header: str = None):
        try:
            with imaplib.IMAP4_SSL(self.mail_imap) as mail:
                mail.login(self.login, self.password)
                mail.list()
                mail.select(folder)
                criterion = f'(HEADER Subject "{header}")' if header else 'ALL'
                result, data = mail.uid('search', None, criterion)
                if not data or not data[0]:
                    print("Letters with this header were not found.")
                    return None
                latest_email_uid = data[0].split()[-1]
                result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
                raw_email = data[0][1]
                email_message = email.message_from_bytes(raw_email)
            return email_message
        except Exception as e:
            print(f"Error on receipt: {e}")
