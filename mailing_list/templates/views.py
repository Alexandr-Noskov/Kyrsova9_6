from mailing_list.models import Client, MailingListMessage, MailingList, MailingListLogs
from vlog.models import Record
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, reverse, redirect
from mailing_list.forms import ClientForm, MailingListMessageForm, MailingListForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from mailing_list.services import send_email
import django
from django.http import Http404


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'mailing_list/index.html'
    extra_context = {
        'title_0': 'Наши рассылки',
        'mailing_list_messages': MailingListMessage.objects.all()[:3],
        'title_1': 'Конфигурации рассылок',
        'mailing_lists': MailingList.objects.all()[:3],
        'title_2': 'Наши клиенты',
        'client_list': Client.objects.filter(is_active=True)[:3],
        'title_logs': 'Логи рассылок',
        'logs_list': MailingListLogs.objects.all()[:3],
        'title_records': 'Записи о рассылках',
        'records_list': Record.objects.filter(sign_of_publication=True)[:3],
    }


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    extra_context = {
        'title': 'Список клиентов',
    }

    def get_queryset(self):
        """Метод благодаря которому отображаются только активные клиенты"""
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class ClientDeactivatedListView(LoginRequiredMixin, ListView):
    model = Client
    extra_context = {
        'title': 'Неактивные клиенты',
    }

    def get_queryset(self):
        """Метод благодаря которому отображаются только неактивные клиенты"""
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=False)
        return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing_list:client_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.created = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing_list:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.created != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    permission_required = 'mailing_list.delete_client'
    success_url = reverse_lazy('mailing_list:client_list')


def client_toggle_activity(request, pk):
    client_item = get_object_or_404(Client, pk=pk)
    if client_item.is_active:
        client_item.is_active = False
    else:
        client_item.is_active = True
    client_item.save()
    return redirect(reverse('mailing_list:client_list'))


class MailingListMessageListView(LoginRequiredMixin, ListView):
    model = MailingListMessage
    extra_context = {
        'title': 'Наши рассылки',
        'mailing_lists': MailingListMessage.objects.all(),
    }


class MailingListMessageDetailView(LoginRequiredMixin, DetailView):
    model = MailingListMessage


class MailingListMessageCreateView(LoginRequiredMixin, CreateView):
    model = MailingListMessage
    form_class = MailingListMessageForm
    success_url = reverse_lazy('mailing_list:message_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.created = self.request.user
        self.object.save()

        return super().form_valid(form)


class MailingListMessageUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingListMessage
    form_class = MailingListMessageForm
    success_url = reverse_lazy('mailing_list:message_list')


class MailingListMessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MailingListMessage
    permission_required = 'mailing_list.delete_message'
    success_url = reverse_lazy('mailing_list:message_list')


class MailingListListView(LoginRequiredMixin, ListView):
    model = MailingList
    extra_context = {
        'title': 'Конфигурации рассылок',
        'mailing_lists': MailingList.objects.all(),
    }


class MailingListDetailView(LoginRequiredMixin, DetailView):
    model = MailingList


class MailingListCreateView(LoginRequiredMixin, CreateView):
    model = MailingList
    form_class = MailingListForm
    success_url = reverse_lazy('mailing_list:mailing_lists_list')
    try:
        for mailing in MailingList.objects.all():
            if mailing.status == MailingList.CREATED:
                send_email(MailingList.ONCE)
    except django.db.utils.ProgrammingError:
        print('ProgrammingError')

    def form_valid(self, form):
        self.object = form.save()
        self.object.created = self.request.user
        self.object.save()

        return super().form_valid(form)


class MailingListUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingList
    form_class = MailingListForm
    success_url = reverse_lazy('mailing_list:mailing_lists_list')


class MailingListDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MailingList
    permission_required = 'mailing_list.delete_mailinglist'
    success_url = reverse_lazy('mailing_list:mailing_lists_list')


class MailingListLogsListView(LoginRequiredMixin, ListView):
    model = MailingListLogs
    extra_context = {
        'title': 'Логи рассылок',
        'mailing_lists': MailingListLogs.objects.all(),
    }


class MailingListLogsDetailView(LoginRequiredMixin, DetailView):
    model = MailingListLogs
