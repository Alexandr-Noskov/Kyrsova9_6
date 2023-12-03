from django.db import models
from datetime import date, datetime
from django.conf import settings

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='фамилия', **NULLABLE)
    surname = models.CharField(max_length=150, verbose_name='отчество', **NULLABLE)
    email = models.EmailField(max_length=150, verbose_name='почта')
    created = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='создан')
    is_active = models.BooleanField(default=True, verbose_name='активный')

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('last_name',)


class MailingListMessage(models.Model):
    subject = models.CharField(max_length=200, verbose_name='тема письма')
    body = models.TextField(verbose_name='сообщение')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='создано')
    created = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='создана')

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MailingList(models.Model):
    ONCE = 'разовая'
    DAILY = 'ежедневно'
    WEEKLY = 'еженедельно'
    MONTHLY = 'ежемесячно'

    PERIODICITY = [
        (ONCE, 'разовая'),
        (DAILY, 'ежедневно'),
        (WEEKLY, 'еженедельно'),
        (MONTHLY, 'ежемесячно'),
    ]

    CREATED = 'создана'
    COMPLETED = 'завершена'
    LAUNCHED = 'запущена'

    SELECT_STATUS = [
        (CREATED, 'создана'),
        (COMPLETED, 'завершена'),
        (LAUNCHED, 'запущена'),
    ]

    message = models.ForeignKey(MailingListMessage, on_delete=models.CASCADE, verbose_name='сообщение')
    time = models.TimeField(default=datetime.now, verbose_name='время')
    start = models.DateTimeField(default=datetime.now, verbose_name='начало рассылки')
    finish = models.DateTimeField(default=datetime.now, verbose_name='окончание рассылки')
    periodicity = models.CharField(max_length=150, choices=PERIODICITY, verbose_name='периодичность')
    status = models.CharField(max_length=100, default='начало рассылки', choices=SELECT_STATUS, verbose_name='статус')
    created = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='создана')

    def __str__(self):
        return self.message.subject

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingListLogs(models.Model):
    DELIVERED = 'delivered'
    NOT_DELIVERED = 'not_delivered'

    STATUS = (
        (DELIVERED, 'доставлено'),
        (NOT_DELIVERED, 'не доставлено'),
    )

    sending = models.ForeignKey(MailingList, on_delete=models.CASCADE, verbose_name='рассылка')
    send_time = models.DateTimeField(auto_now_add=True, verbose_name='время отправки')
    status = models.CharField(choices=STATUS, verbose_name='статус рассылки')
    response = models.TextField(**NULLABLE, verbose_name='ответ почтового сервера')

    def __str__(self):
        return f'{self.sending.message.subject}: {self.send_time}'

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'
