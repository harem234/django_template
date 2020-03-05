import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from celery.utils.log import get_task_logger

from user.views import account_activation_token
from django_template_proj.celery_app import app as celery_app
# from celery.app.log import TaskFormatter

logger = get_task_logger(__name__)

# logger = logging.getLogger()
# sh = logging.StreamHandler()
# sh.setFormatter(TaskFormatter('%(asctime)s - %(task_id)s - %(task_name)s - %(name)s - %(levelname)s - %(message)s'))
# logger.setLevel(logging.INFO)
# logger.addHandler(sh)


# name="foobar.sample_task"
@celery_app.task()
def sample_task(value):
    logger.info('sample_task returning {0}'.format(value))
    return value


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


# automatic name is: "user.tasks._send_mail"
@celery_app.task(bind=True, default_retry_delay=10 * 60, max_retries=3)
def _send_mail(self, subject, message, email):
    import smtplib
    try:
        send_mail(subject, message, None, [email, ])
        logger.info('email sent to: {0}'.format(email))
    except smtplib.SMTPException as exc:
        raise self.retry(exc=exc)
