from django import template
from django.core.mail import send_mail
from django.conf import settings
from mailing_list.models import Client, MailingListMessage, MailingList, MailingListLogs

register = template.Library()


def send_email(*args):
    all_email = []
    for client in Client.objects.all():
        all_email.append(str(client.email))

    for mailing in MailingList.objects.all():
        if mailing.status == MailingList.CREATED and mailing.periodicity == (str(*args)):
            filtered_message = mailing.message
            message = MailingListMessage.objects.filter(subject=filtered_message)
            for m in message:
                send_mail(
                    subject=m.subject,
                    message=m.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[*all_email],
                )
                status_list = []
                server_response = {
                    'sending': MailingList.objects.get(pk=mailing.id),
                    'status': MailingListLogs.DELIVERED,
                    'response': [*all_email]}
                status_list.append(MailingListLogs(**server_response))
                MailingListLogs.objects.bulk_create(status_list)
                if mailing.periodicity == MailingList.ONCE:
                    mailing.status = MailingList.COMPLETED
                    mailing.save()
                else:
                    mailing.status = MailingList.LAUNCHED
                    mailing.save()
