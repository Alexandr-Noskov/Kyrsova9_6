from django.urls import path
from vlog.apps import VlogConfig
from vlog.views import RecordListView, RecordDeactivatedListView, RecordDetailView, RecordCreateView, RecordUpdateView, \
    RecordDeleteView, toggle_activity

app_name = VlogConfig.name

urlpatterns = [
    path('records/', RecordListView.as_view(), name='records'),
    path('records_deactivated/', RecordDeactivatedListView.as_view(), name='records_deactivated'),
    path('record/create/', RecordCreateView.as_view(), name='record_create'),
    path('record/<slug:slug>/', RecordDetailView.as_view(), name='record_detail'),
    path('record/update/<slug:slug>/', RecordUpdateView.as_view(), name='record_update'),
    path('record/delete/<slug:slug>/', RecordDeleteView.as_view(), name='record_delete'),
    path('record/toggle/<slug:slug>/', toggle_activity, name='toggle_activity'),
]