from django.contrib import admin
from .models import Client, Message, Mailing, MailingAttempts


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_email', 'client_name', 'pk',)
    list_filter = ('client_name', 'client_email',)
    search_fields = ('client_name', 'client_email', 'description',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subject', 'message',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'mailing_name', 'period', 'first_send_date_time', 'status', 'last_send_date_time',)


@admin.register(MailingAttempts)
class MailingAttemptsAdmin(admin.ModelAdmin):
    list_display = ('mailing',)
