from django import forms

from mailing_list.models import Client, MailingListMessage, MailingList, MailingListLogs


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('created', 'is_active',)


class MailingListMessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingListMessage
        exclude = ('created',)


class MailingListForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingList
        fields = ('message', 'periodicity', 'start', 'finish', 'status', 'time',)


# class MailingListLogsForm(StyleFormMixin, forms.ModelForm):
#     class Meta:
#         model = MailingListLogs
#         fields = '__all__'