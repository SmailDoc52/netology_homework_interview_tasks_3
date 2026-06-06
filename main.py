import os

from dotenv import load_dotenv

from tools.email_manager import EmailManager


if __name__ == '__main__':
    
    load_dotenv()

    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")
    
    gmail_smtp = "smtp.gmail.com"
    gmail_imap = "imap.gmail.com"
    
    email_mng = EmailManager(gmail_smtp, gmail_imap, login, password)
    
    subject = 'Subject'
    recipients = ['vasya@email.com', 'petya@email.com']
    message_text = 'Hello'
    header = None
    
    email_mng.send_message(recipients, subject, message_text)
    email_mng.receive_message("INBOX", header=header)
