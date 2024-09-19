from datetime import timezone

from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    client_email = models.EmailField(max_length=100, verbose_name='email клиента')
    client_name = models.CharField(max_length=150, verbose_name='имя клиента')
    description = models.TextField(verbose_name='комментарий')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)

    def __str__(self):
        return self.client_name

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='тема письма')
    message = models.TextField(verbose_name='сообщение')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)

    def __str__(self):
        return f'Тема сообщения {self.subject}, сообщение: {self.message}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mailing(models.Model):
    mailing_name = models.CharField(max_length=255, verbose_name='имя рассылки')
    first_send_date_time = models.DateTimeField(verbose_name='дата и время первой рассылки', **NULLABLE)
    next_send_date_time = models.DateTimeField(verbose_name='дата и время следующей рассылки', **NULLABLE)
    last_send_date_time = models.DateTimeField(default=None, verbose_name='дата и время последней рассылки', **NULLABLE)

    period_choices = (
        (60, "Раз в минуту"),
        (300, "Раз в 5 минут"),
        (600, "Раз в 10 минут"),
    )
    period = models.IntegerField(choices=period_choices, default=60, verbose_name='периодичность отправки')

    status_choices = (
        (1, "Создана"),
        (2, "Запущена"),
        (3, "Отменена"),
        (4, "Завершена"),
    )
    status = models.IntegerField(choices=status_choices, default=0, verbose_name='статус рассылки')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение')
    clients = models.ManyToManyField(Client, verbose_name='клиенты', blank=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)

    def __str__(self):
        return self.mailing_name

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        permissions = [
            ('deactivate_mailing', 'Can deactivate mailing'),
            ('view_all_mailings', 'Can view all mailings'),
        ]


class MailingAttempts(models.Model):
    """Лог рассылки"""
    SUCCESS = 'successful'
    FAIL = 'failed'
    STATUS_VARIANTS = [
        (SUCCESS, 'успешно'),
        (FAIL, 'неуспешно'),
    ]

    last_attempt_time = models.DateTimeField(auto_now_add=True, **NULLABLE, verbose_name='последняя попытка')
    status = models.CharField(max_length=50, choices=STATUS_VARIANTS, verbose_name='статус рассылки')
    server_response = models.CharField(max_length=150, verbose_name='ответ почтового сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')

    def __str__(self):
        return f"{self.mailing} - {self.status}"

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытки рассылки'
