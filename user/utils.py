from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv
load_dotenv()
import os

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')


def send_verification_code(phone_number, code):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f'Hello, Your FACEVENT verification code is {code}',
        from_=TWILIO_NUMBER,  # Replace with your Twilio number
        to=phone_number
    )

    return message.sid


def verify_phone_number(phone_number):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        phone_number = client.lookups.phone_numbers(phone_number).fetch(type='carrier')
    except TwilioRestException as e:
        if e.code == 20404:
            return False
        else:
            raise e
    return True