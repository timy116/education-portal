from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.conf import settings

from .helper import *
from .message import *

NOTIFICATION_EMAIL = f"Education Portal Notification <{settings.EMAIL_ADDR}>"


def send_email(sender: str, recipients: list, subject: str, text_content: str, html_content=None,
               plain_text_template="email.txt", html_template="email.html"):
    # load plain text and html template
    plain_text = loader.get_template(plain_text_template)
    html = loader.get_template(html_template)

    # get rendered plain text and html
    rendered_plain_text = plain_text.render(context={"content": text_content})

    if html_content:
        rendered_html = html.render(context={"content": html_content})
    else:
        rendered_html = html.render(context={"content": text_content})

    message = EmailMultiAlternatives(
        subject=subject, body=rendered_plain_text, from_email=sender, to=recipients
    )
    message.attach_alternative(content=rendered_html, mimetype="text/html")
    message.send()


def send_verification_email(request, user: User, is_changed_email=None):
    """
    :param request: HTTP request
    :param user: User object
    :param is_changed_email: want to update email
    :return: None

    Sending an Email verify user's account.
    """

    if not is_changed_email:
        user.email_verifications.all().delete()
        verification = generate_token(user)
        message = email_verification(request, verification.token)
        send_email(sender=NOTIFICATION_EMAIL, recipients=[user.email], subject=message["subject"],
                   text_content=message["text_content"])
    else:
        ...
