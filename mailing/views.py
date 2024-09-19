from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import ClientForm, MailingForm, ModeratorMailingForm, MessageForm
from mailing.models import Mailing, Client, Message, MailingAttempts


class ClientListView(LoginRequiredMixin, ListView):
    """Список всех клиентов"""
    model = Client

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='manager'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='manager') and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Класс для создания клиента"""
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('mailing:clients_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        self.object.owner = user

        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Класс для редактирования клиента"""
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('mailing:clients_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class MailingListView(LoginRequiredMixin, ListView):
    """Класс для отображения списка рассылок"""
    model = Mailing

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='manager'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingDetailView(LoginRequiredMixin, DetailView):
    """Класс для отображения одной рассылки"""
    model = Mailing

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='manager') and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Класс для создания рассылки"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        self.object.owner = user

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Класс для редактирования рассылки"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailingForm
        elif user.groups.filter(name='manager'):
            return ModeratorMailingForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='manager') and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Класс для удаления рассылки"""
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class MessageListView(LoginRequiredMixin, ListView):
    """Список просмотра всех сообщений"""
    model = Message

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='manager'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Класс для создания сообщения"""
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('mailing:message_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        self.object.owner = user

        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Класс для редактирования сообщения"""
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('mailing:message_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='manager') and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class AttemptsListView(LoginRequiredMixin, ListView):
    model = MailingAttempts
    template_name = 'mailing/attempts_list.html'


class AttemptsDetailView(LoginRequiredMixin, DetailView):
    model = MailingAttempts
    template_name = 'mailing/attempts_detail.html'