from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from datetime import datetime


# Organization list
ORGANIZATION = (('--', 'Select Organization'), ('AMFB', 'Alert MFB'), ('ABL', 'AutoBucks'))

# Role list
ROLE = (('--', 'Select Role'), ('Upload Officer', 'Upload Officer'), ('HOP', 'HOP'), ('Credit', 'Credit'), ('IT', 'IT'), ('Others', 'Others'))

# Branch list
BRANCH = (('--', 'Select Branch'), ('Head Office', 'Head Office'), ('Ebute Metta', 'Ebute Metta'), ('Idumagbo', 'Idumagbo'), ('Idumota', 'Idumota'), ('Sango', 'Sango'), ('Ikeja', 'Ikeja'), ('Agege', 'Agege'), ('Ikorodu', 'Ikorodu'), ('Mushin', 'Mushin'), ('Trade Fair', 'Trade Fair'), ('Ikotun', 'Ikotun'), ('Abeokuta', 'Abeokuta'), ('Ibandan', 'Ibandan'))

# Bank code list
BANK_CODE = [('0342', 'AMFB Code')]

# Mandate type list
MANDATE_TYPE = ((1, 'Direct Debit'), (2, 'Balance Enquiry'))

# Frequency list
FREQUENCY = ((0, 'Variable'), (1, 'Weekly'), (2, 'Every 2 Weeks'), (4, 'Monthly'))

# Mandate status
MANDATE_STATUS = ((1, 'Active'), (2, 'Suspended'))


def loan_file_size(value):
    limit = 10 * 1024 * 1024
    if value.size > limit:
        raise ValidationError("File too large. Size should not exceed 10mb.")


# Asynchronous email sending
def send_async_email(subject, message, recipient_list):
    try:
        email = EmailMultiAlternatives(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        email.send()
    except Exception as e:
        print(f"Error sending email: {e}")


# Format date
def format_date(date):
    return date.isoformat() if isinstance(date, datetime) else date


# API functions
base_url = "https://apitest.nibss-plc.com.ng/"
headers = {
    "Authorization": f"Bearer {settings.API_KEY}",
}
