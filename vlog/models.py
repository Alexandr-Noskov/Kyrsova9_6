from django.db import models
from django.conf import settings
from mailing_list.models import NULLABLE
from django.urls import reverse


class Record(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.SlugField(max_length=300, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='images/records/', verbose_name='изображение(превью)', **NULLABLE)
    created = models.DateField(verbose_name='дата создания', auto_now_add=True)
    sign_of_publication = models.BooleanField(default=True, verbose_name='активный')
    views = models.IntegerField(default=0, verbose_name='просмотры')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='автор')

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('vlog:record_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        get_latest_by = 'created'

    def views_count(self):
        self.views += 1
        self.save()