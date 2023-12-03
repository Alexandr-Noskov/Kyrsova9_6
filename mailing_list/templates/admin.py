from django.contrib import admin
from mailing_list.models import Client, MailingListMessage, MailingList, MailingListLogs


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'created', 'is_active',)


@admin.register(MailingListMessage)
class MailingListMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_time',)


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ('message', 'time', 'periodicity',)


@admin.register(MailingListLogs)
class MailingListLogsAdmin(admin.ModelAdmin):
    list_display = ('sending', 'send_time', 'status',)