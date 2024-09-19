import smtplib
from datetime import datetime

import pytz
from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from mailing.models import Mailing, MailingAttempts
from mailing.services import start_scheduler, send_mailing


# @util.close_old_connections
# def delete_old_job_executions(max_age=604_800):
#     """Удалят старые задачи"""
#     DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):

    def handle(self, *args, **options):

        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime = datetime.now(zone)
        mailings = Mailing.objects.filter(status__in=[1])
        print(mailings)
        print(f'Количество рассылок для отправки в ручную командой send_mailings: {mailings.count()}')

        start_scheduler()
        send_mailing()

        for mailing in mailings:
            print(f'Рассылка: {mailing.message.subject}')
            clients = mailing.clients.all()
            try:
                server_response = send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.client_email for client in clients],
                    fail_silently=False,
                )
                MailingAttempts.objects.create(last_attempt_time=current_datetime,
                                               status=MailingAttempts.SUCCESS,
                                               server_response=server_response,
                                               mailing=mailing, )
            except smtplib.SMTPException as e:
                MailingAttempts.objects.create(last_attempt_time=current_datetime,
                                               status=MailingAttempts.FAIL,
                                               server_response=str(e),
                                               mailing=mailing,
                                               )
