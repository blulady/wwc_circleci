from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings
from smtplib import SMTPException
import logging

logger = logging.getLogger('django')

def sendmail_helper(toEmail, subject, templateFile, contextData):
    logger.debug(f"sendemail: toEmail: {toEmail} subject: {subject} templateFile: {templateFile} contextData: {contextData}")
    if subject and templateFile and toEmail and contextData:
        fromEmail = settings.EMAIL_HOST_USER
        message = get_template(templateFile).render(contextData)
        msg = EmailMessage(subject, message, fromEmail, [toEmail])
        msg.content_subtype = "html"

        try:
            msg.send()
        except (ValueError, SMTPException) as e:
            logger.error('sendemail: There was an error sending an email: %s', e)
            return False
        else:
            logger.info('sendemail: Mail successfully sent')
            return True
    else:
        logger.error('sendemail: Make sure all parameters values are passed and valid.')
        return False
