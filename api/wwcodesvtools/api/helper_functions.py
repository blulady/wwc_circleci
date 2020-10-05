from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings
from smtplib import SMTPException
from django.core.validators import validate_email, ValidationError
import logging

logger = logging.getLogger('django')

def send_email_helper(to_email, subject, template_file, context_data):
    logger.debug(f"send_email_helper: to_email: {to_email} subject: {subject} template_file: {template_file} contextData: {context_data}")
    if subject and template_file and to_email and context_data:
        try:
            validate_email(to_email)
            from_email = settings.EMAIL_HOST_USER
            message = get_template(template_file).render(context_data)
            msg = EmailMessage(subject, message, from_email, [to_email])
            msg.content_subtype = "html"
            msg.send()
        except (ValidationError,ValueError, SMTPException) as e:
            logger.error(f"send_email_helper: There was an error sending an email: {e}")
            return False
        else:
            logger.info("send_email_helper: Mail successfully sent")
            return True
    else:
        logger.error("send_email_helper: Make sure all parameters values are passed and valid.")
        return False
