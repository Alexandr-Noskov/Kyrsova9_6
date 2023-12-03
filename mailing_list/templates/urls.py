from django.urls import path
from mailing_list.apps import MailingListConfig
from mailing_list.views import IndexView, ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, \
    ClientDeleteView, ClientDeactivatedListView, client_toggle_activity, MailingListMessageListView, \
    MailingListMessageDetailView, MailingListMessageCreateView, MailingListMessageUpdateView, \
    MailingListMessageDeleteView, MailingListListView, MailingListDetailView, MailingListCreateView, \
    MailingListUpdateView, MailingListDeleteView, MailingListLogsListView, MailingListLogsDetailView
from django.views.decorators.cache import cache_page, never_cache

app_name = MailingListConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='homepage'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/deactivated/', ClientDeactivatedListView.as_view(), name='client_deactivated_list'),
    path('client/<int:pk>/', cache_page(60)(ClientDetailView.as_view()), name='client_detail'),
    path('client/create/', never_cache(ClientCreateView.as_view()), name='client_create'),
    path('client/update/<int:pk>/', never_cache(ClientUpdateView.as_view()), name='client_update'),
    path('client/delete/<int:pk>', never_cache(ClientDeleteView.as_view()), name='client_delete'),
    path('client/toggle/<int:pk>', client_toggle_activity, name='client_toggle_activity'),
    path('mailing_list_messages/', MailingListMessageListView.as_view(), name='message_list'),
    path('mailing_list_message/<int:pk>/', cache_page(60)(MailingListMessageDetailView.as_view()),
         name='message_detail'),
    path('mailing_list_message/create/', never_cache(MailingListMessageCreateView.as_view()), name='message_create'),
    path('mailing_list_message/update/<int:pk>/', never_cache(MailingListMessageUpdateView.as_view()),
         name='message_update'),
    path('mailing_list_message/delete/<int:pk>/', never_cache(MailingListMessageDeleteView.as_view()),
         name='message_delete'),
    path('mailing_lists/', MailingListListView.as_view(), name='mailing_lists_list'),
    path('mailing_lists/<int:pk>/', cache_page(60)(MailingListDetailView.as_view()), name='mailing_list_detail'),
    path('mailing_lists/create/', never_cache(MailingListCreateView.as_view()), name='mailing_list_create'),
    path('mailing_lists/update/<int:pk>/', never_cache(MailingListUpdateView.as_view()), name='mailing_list_update'),
    path('mailing_lists/delete/<int:pk>/', never_cache(MailingListDeleteView.as_view()), name='mailing_list_delete'),
    path('mailing_lists_logs/', MailingListLogsListView.as_view(), name='logs_list'),
    path('mailing_lists_logs/<int:pk>/', MailingListLogsDetailView.as_view(), name='logs_detail'),
]