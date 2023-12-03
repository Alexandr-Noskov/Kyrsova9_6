from django.core.mail import send_mail
from django.conf import settings


def send_email(record_object):
    send_mail(
        subject=f'100 просмотров {record_object}',
        message=f'Юху! Уже 100 просмотров записи {record_object}!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['nathovaekaterina@gmail.com', 'nathovaekaterina@yandex.ru']
    )