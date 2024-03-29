import re
import threading
import phonenumbers
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError
from decouple import config
from twilio.rest import Client

email_regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
phone_number_regex = re.compile(r"(\+[0-9]+\s*)?(\([0-9]+\))?[\s0-9\-]+[0-9]+")
username_regex = re.compile(r"^[a-zA-Z0-9_.-]+$")


def check_email_or_phone_number(input_data):
    if re.fullmatch(email_regex, input_data):
        input_data = "email"

    elif re.fullmatch(phone_number_regex, input_data):
        input_data = "phone_number"

    else:
        data = {
            "request status": "Terrible!",
            "message": "email or phone number wrong!"
        }
        raise ValidationError(data)

    return input_data




def check_login_type(login_type):
    if re.fullmatch(email_regex, login_type):
        login_type = "email"

    elif re.fullmatch(phone_number_regex, login_type):
        login_type = "phone_number"
        
    elif re.fullmatch(username_regex, login_type):
        login_type = "username"

    else:
        data = {
            "request status": "Terrible!",
            "message": "email or phone number wrong!"
        }
        raise ValidationError(data)

    return login_type




class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
        
    def run(self):
        self.email.send()
        
    
class Email:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            to=[data['to_email']],
        )
        if data.get('content_type') == "html":
            email.content_subtype = "html"
        EmailThread(email).start()
        
        
def send_email(email, code):
    html_content = render_to_string('email/authentication/activate_account.html', {"code": code})
    Email.send_email({
            "subject": "Royhatdan otish",
            "to_email": email,
            "body": html_content,
            "content_type": "html"
        }
    )

# pip install twilio
def send_phone_code(phone, code):
    account_sid = config('account_sid')
    auth_token = config('auth_token')
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=f"Salom do'stim! Sizning tasdiqlash kodingiz: {code}\n",
        from_="+99899325242",
        to=f"{phone}"
    )