from django.conf import settings
from django.core.mail import send_mail
import os


def get_url_from_hostname(hostname):
    if settings.DEBUG or settings.TEST:
        scheme = "http"
    else:
        scheme = "https"
    url = "{}://{}".format(scheme, hostname)
    return url


def EmailService(subject, message, recipient_list, from_email=None, html_message=None):
    from_email = from_email or settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)


def get_file_content(file_path, mode):
    if os.path.isfile(file_path):
        with open(file_path, mode) as file_content:
            return file_content.read()
    else:
        raise FileNotFoundError
