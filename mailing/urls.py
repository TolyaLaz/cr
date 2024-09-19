from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView, \
    ClientListView, ClientCreateView, ClientUpdateView, MessageListView, MessageCreateView, MessageUpdateView, \
    ClientDetailView, ClientDeleteView, MessageDeleteView, MessageDetailView, AttemptsListView, AttemptsDetailView


app_name = MailingConfig.name

urlpatterns = [
    # рассылки
    path('', cache_page(60)(MailingListView.as_view()), name='mailing_list'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_form'),
    path('mailing_update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    # клиенты
    path('clients/', cache_page(60)(ClientListView.as_view()), name='clients_list'),
    path('client_create/', ClientCreateView.as_view(), name='clients_form'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_detail/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    # сообщения
    path('messages/', cache_page(60)(MessageListView.as_view()), name='message_list'),
    path('message_create/', MessageCreateView.as_view(), name='message_form'),
    path('message_update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message_detail/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    # логи
    path('attempts_list/', AttemptsListView.as_view(), name='attempts'),
    path('attempts_detail/<int:pk>/', AttemptsDetailView.as_view(), name='attempt_detail'),
]