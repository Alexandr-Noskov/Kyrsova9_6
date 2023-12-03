from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from vlog.models import Record
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from vlog.services import send_email
from django.shortcuts import get_object_or_404, reverse, redirect
from vlog.forms import RecordForm
from django.http import Http404


class RecordListView(LoginRequiredMixin, ListView):
    """Контроллер для отображения блоговых записей"""
    model = Record
    extra_context = {
        'title': 'Все записи'
    }

    def get_queryset(self):
        """Метод благодаря которому отображаются только активные записи"""
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_publication=True)
        return queryset


class RecordDeactivatedListView(LoginRequiredMixin, ListView):
    """Контроллер для отображения блоговых записей"""
    model = Record
    extra_context = {
        'title': 'Деактивированные записи'
    }

    def get_queryset(self):
        """Метод благодаря которому отображаются только неактивные записи"""
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_publication=False)
        return queryset


class RecordDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для отображения одной блоговой записи в подробностях"""
    model = Record

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.get_object()
        object = self.get_object()
        increase = get_object_or_404(Record, pk=object.pk)
        increase.views_count()
        if increase.views == 100:
            send_email(increase)
        return context_data


class RecordCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для создания блоговой записи"""
    model = Record
    form_class = RecordForm
    success_url = reverse_lazy('vlog:records')

    def form_valid(self, form):
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()

        return super().form_valid(form)


class RecordUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для обновления блоговой записи"""
    model = Record
    form_class = RecordForm
    success_url = reverse_lazy('vlog:records')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.author != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class RecordDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Контроллер для удаления блоговой записи"""
    model = Record
    permission_required = 'vlog.delete_record'
    success_url = reverse_lazy('vlog:records')


def toggle_activity(request, slug):
    blog_record_item = get_object_or_404(Record, slug=slug)
    if blog_record_item.sign_of_publication:
        blog_record_item.sign_of_publication = False
    else:
        blog_record_item.sign_of_publication = True
    blog_record_item.save()
    return redirect(reverse('vlog:records'))