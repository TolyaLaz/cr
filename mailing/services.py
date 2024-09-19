# import smtplib
#
# import pytz
# from datetime import datetime, timedelta
# from django.conf import settings
# from django.core.mail import send_mail
# from mailing.models import Mailing, MailingAttempts
# from apscheduler.schedulers.background import BackgroundScheduler
#
# def send_mailing():
#     zone = pytz.timezone(settings.TIME_ZONE)
#     current_datetime = datetime.now(zone)
#     mailings = Mailing.objects.filter(
#         next_send_date_time__lte=current_datetime, status__in=[1]
#     )
#
#     for mailing in mailings:
#         mailing.next_send_date_time += timedelta(seconds=mailing.period)
#         if mailing.last_send_date_time and mailing.next_send_date_time >= mailing.last_send_date_time:
#             mailing.status = 3
#         mailing.save()
#         for client in mailing.clients.all():
#             try:
#                 response = send_mail(subject=mailing.massege.subject,
#                                      message=mailing.massege.message,
#                                      from_email=settings.EMAIL_HOST_USER,
#                                      recipient_list=[client.client_email],
#                                      fail_silently=False)
#                 MailingAttempts.objects.create(response_status=str(response),
#                                               status=True, mailing=mailing,
#                                               client=client)
#             except smtplib.SMTPException as e:
#                 MailingAttempts.objects.create(response_status=str(e),
#                                               mailing=mailing,
#                                               client=client)
#



import smtplib
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail

from mailing.models import Mailing, MailingAttempts


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    print(f'локальное время: {current_datetime}\nзона: {zone}')
    mailings = Mailing.objects.filter(next_send_date_time__lte=current_datetime, status__in=[1, 2])
    print(f'Количество рассылок для отправки автоматически: {mailings.count()}')

    for mailing in mailings:
        print(f'Рассылка ID: {mailing.id}, next_send_time: {mailing.next_send_date_time}')
        mailing.status = 2
        clients = mailing.clients.all()
        try:
            server_response = send_mail(
                subject=mailing.message.subject,
                message=mailing.message.message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email for client in clients],
                fail_silently=False,
            )
            print(mailing.next_send_date_time)
            print(f'ответ сервера: {server_response}')
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

        if mailing.period == 60:
            mailing.next_send_date_time += timedelta(seconds=60)
        elif mailing.period == 300:
            mailing.next_send_date_time += timedelta(seconds=300)
        elif mailing.period == 600:
            mailing.next_send_date_time += timedelta(seconds=600)
        mailing.save()
        print(f'Обновленное next_send_time для рассылки ID: {mailing.id}: {mailing.next_send_date_time}')






def start_scheduler():
    print('Starting scheduler...')
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=10)

    if not scheduler.running:
        scheduler.start()

    print('Scheduler started')
