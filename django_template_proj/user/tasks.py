from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django_template_proj.celery import app as celery_app
from user.views import account_activation_token


@celery_app.task(name="foobar.sample_task")
def sample_task(value):
    print(value)


# @celery_app.task(name="user.before_send")
def send_email_verification(user, site):
    current_site = site
    subject = 'Activate Your Account'
    message = render_to_string('registration/email_verification.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    _send_mail.delay(subject, message, user.email, )


@celery_app.task(name="user._send_mail", bind=True, default_retry_delay=10 * 60, )
def _send_mail(self, subject, message, email):
    import smtplib
    try:
        send_mail(subject, message, None, [email, ])
    except smtplib.SMTPException as ex:
        self.retry(exc=ex)
