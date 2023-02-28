from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings
from smtplib import SMTPException
from datetime import datetime, timedelta
from django.core.validators import validate_email, ValidationError
from pathlib import Path
from api.models import User_Team, Role
import logging
import string
import random


logger = logging.getLogger('django')


def send_email_helper(to_email, subject, template_file, context_data):
    logger.debug(f"send_email_helper: to_email: {to_email} subject: {subject} template_file: {template_file} contextData: {context_data}")
    html_file = Path(f"api/templates/{template_file}")
    if subject and html_file.exists() and to_email and isinstance(context_data, dict):
        try:
            validate_email(to_email)
            from_email = settings.EMAIL_SENDER
            message = get_template(template_file).render(context_data)
            msg = EmailMessage(subject, message, from_email, [to_email])
            msg.content_subtype = "html"
            msg.send()
        except (ValidationError, ValueError, SMTPException) as e:
            logger.error(f"send_email_helper: There was an error sending an email: {e}")
            return False
        else:
            logger.info("send_email_helper: Mail successfully sent")
            return True
    else:
        logger.error("send_email_helper: Make sure all parameters values are passed and valid.")
        return False


def generate_random_password(num):
    # generate random pasword string of num chars
    letters_and_digits = string.ascii_letters + string.digits
    password = ''.join((random.choice(letters_and_digits) for i in range(num)))
    return password


def is_director_or_superuser(user_id, is_superuser):
    try:
        highest_user_role = User_Team.highest_role(user_id=user_id)
        return (highest_user_role == Role.DIRECTOR) or is_superuser
    except Exception as e:
        logger.error(f'is_director_or_superuser: Error user not found : {e}')
        return False


# Validate if the token/registration link is expired based on the date (last 14 digits of the token)
# It's expired if it's been more than 72hrs
def is_token_expired(self, registration_token):
    token_datetime = datetime.strptime(registration_token[-14:], '%Y%m%d%H%M%S')
    return (datetime.now() - timedelta(seconds=settings.REGISTRATION_LINK_EXPIRATION) > token_datetime)
