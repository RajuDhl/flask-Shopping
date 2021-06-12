from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import logging

from app.services.utils import *
import os

domain = os.environ.get("SAME_DAY_DOMAIN")
api_key = os.environ.get("SENDGRID_API_KEY")


def send_verification_email(recipient, uuid):
    # lookup project owners
    if recipient.find('@samedayauto.net') == -1:
        raise AssertionError
    message = Mail(
        from_email=('noreply@samedayauto.net', 'Same Day Auto'),
        to_emails=recipient,
        subject='Please verify your email - Same Day Auto Finance',
        html_content='<p>Please continue the registration process by following the link below.<br/>'
                     f'<a target="_blank" href="{domain}/verify/{uuid}">Verify my email</a><br/>'
                     f'<p>Thank you,<br/>Same Day Auto Finance</p>')
    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        logging.info(f'Email verification email sent to {recipient}. SendGrid response: {response}')
    except Exception as e:
        logging.error(type(e), e)


def send_password_reset_link(email):
    user = lookup_user('email', email)
    if user is not None:
        message = Mail(
            from_email=('noreply@samedayauto.net', 'Same Day Auto'),
            to_emails=email,
            subject='Password reset request',
            html_content="<p>A request was made to reset your password for Same Day Auto Finance's internal "
                         "application.<br/> "
                         "Please follow the link below to reset your password.<br/>"
                         f'<a target="_blank" href="{domain}/verify/{user.uuid}">Reset my password</a><br/><br/>'
            # f'If this request was not made please contact {support_contact}</p>'
                         '<p>Thank you,<br/>Same Day Auto Finance</p>'
        )
        try:
            sg = SendGridAPIClient(api_key)
            response = sg.send(message)
            logging.info(f'password reset message sent to {email}')
        except Exception as e:
            logging.error(type(e), e)
    else:
        raise AssertionError
